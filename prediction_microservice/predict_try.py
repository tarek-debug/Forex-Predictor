import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from joblib import load
import requests
import os

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

def load_scaler_and_model(target_currency, base_currency="EUR", model_save_dir="prediction_models"):
    scaler_filename = f'{model_save_dir}/scalers/{base_currency}_to_{target_currency}_scaler.joblib'
    if not os.path.exists(scaler_filename):
        raise FileNotFoundError(f"Scaler file {scaler_filename} not found.")
    scaler = load(scaler_filename)
    model_path = f'{model_save_dir}/{base_currency}_to_{target_currency}.keras'
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file not found.")
    model = load_model(model_path)
    return scaler, model

def scale_data(df, scaler):
    values_scaled = scaler.transform(df)
    return values_scaled

def inverse_scale_data(predicted_scaled, scaler):
    predictions = scaler.inverse_transform(predicted_scaled).flatten()
    return predictions

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

def main(base_currency, target_currency, n_steps=60):
    future_date_str = input("Enter future date (YYYY-MM-DD): ")
    future_date = pd.to_datetime(future_date_str)
    
    model_save_dir = "prediction_models"
    df_recent_rates = fetch_recent_exchange_rates(base_currency, target_currency, n_steps)
    
    last_date = df_recent_rates.index[-1]  # Use the last date from fetched data
    
    # Calculate n_future as the number of days from last_date to future_date
    n_future = (future_date - last_date).days
    
    if n_future < 1:
        print("The future date must be at least 1 day after the last data point available.")
        return
    
    scaler, model = load_scaler_and_model(target_currency, base_currency, model_save_dir)
    scaled_recent_rates = scale_data(df_recent_rates, scaler)
    
    predictions_scaled = rolling_forecast(scaler, model, scaled_recent_rates, n_steps, n_future)
    future_predictions = inverse_scale_data(predictions_scaled, scaler)
    
    future_dates = [last_date + pd.Timedelta(days=i+1) for i in range(n_future)]
    
    print(f"Future predictions for {base_currency} to {target_currency}:")
    for date, prediction in zip(future_dates, future_predictions):
        print(f"{date.strftime('%Y-%m-%d')}: {prediction}")


if __name__ == "__main__":
    base_currency = input("Enter base currency (e.g., EUR): ").upper()
    target_currency = input("Enter target currency (e.g., CNY): ").upper()
    n_steps = 60  # This should match your training configuration
    main(base_currency, target_currency, n_steps)
