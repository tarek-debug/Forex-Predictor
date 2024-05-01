from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from joblib import load as joblib_load
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Directory where your models and scalers are saved
model_save_dir = "prediction_models"
DATA_STORAGE_SERVICE_URL = os.environ.get('DATA_STORAGE_SERVICE_URL', 'http://localhost:5003')

def fetch_recent_exchange_rates(base_currency, target_currency, num_days=60):
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.Timedelta(days=num_days)
    url = f"https://api.frankfurter.app/{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')}?from={base_currency}&to={target_currency}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['rates']).T
    df.columns = [target_currency]
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

def load_scaler_and_model(base_currency, target_currency):
    scaler_filename = os.path.join(model_save_dir, 'scalers', f'{base_currency}_to_{target_currency}_scaler.joblib')
    model_path = os.path.join(model_save_dir, f'{base_currency}_to_{target_currency}.keras')
    scaler = joblib_load(scaler_filename)
    model = load_model(model_path)
    return scaler, model

def scale_data(df, scaler):
    values_scaled = scaler.transform(df)
    return values_scaled

def rolling_forecast(scaler, model, scaled_data, n_steps, n_future):
    predictions_scaled = []
    if scaled_data.shape[0] < n_steps:
        padding_needed = n_steps - scaled_data.shape[0]
        padding = np.tile(scaled_data[0], (padding_needed, 1))
        scaled_data_padded = np.vstack([padding, scaled_data])
    else:
        scaled_data_padded = scaled_data
    
    input_seq = scaled_data_padded[-n_steps:]
    for _ in range(n_future):
        input_seq_reshaped = input_seq.reshape((1, n_steps, -1))
        predicted_scaled = model.predict(input_seq_reshaped)
        predictions_scaled.append(predicted_scaled[0])
        input_seq = np.append(input_seq[1:], predicted_scaled, axis=0)
    
    return np.array(predictions_scaled)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    username = data.get('username')
    base_currency = data.get('base_currency', '').upper()
    target_currency = data.get('target_currency', '').upper()
    future_date_str = data.get('future_date')
    n_steps = 60  # This should match your training configuration

    if not base_currency or not target_currency or not future_date_str:
        return jsonify({"error": "Missing required parameters."}), 400

    future_date = pd.to_datetime(future_date_str)
    df_recent_rates = fetch_recent_exchange_rates(base_currency, target_currency, 90)
    scaler, model = load_scaler_and_model(base_currency, target_currency)
    scaled_recent_rates = scale_data(df_recent_rates[[target_currency]], scaler)
    n_future = (future_date - df_recent_rates.index[-1]).days + 1
    predictions_scaled = rolling_forecast(scaler, model, scaled_recent_rates, n_steps, n_future)
    future_predictions = scaler.inverse_transform(predictions_scaled)[:n_future]

    future_dates = [df_recent_rates.index[-1] + pd.Timedelta(days=i) for i in range(1, n_future+1)]
    predictions = [{"date": date.strftime('%Y-%m-%d'), "prediction": float(prediction)} for date, prediction in zip(future_dates, future_predictions.flatten())]
    '''
       # Include initial request details in the data sent to data storage
    post_data = {
        "username": username,
        "base_currency": base_currency,
        "target_currency": target_currency,
        "future_date": future_date_str,
        "predictions": predictions
    }
    response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/predictions", json=post_data)
    print(predictions)
    print(response )
    

    if response.status_code in [200, 201]:
        return jsonify(predictions)
    else:
        return jsonify({"error": "Failed to store predictions"}), response.status_code

'''
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)