from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from scipy.interpolate import make_interp_spline
import os  # Import os module to handle file directory operations
from joblib import dump

# Ensure the prediction_models directory exists
model_save_dir = "prediction_models"
if not os.path.exists(model_save_dir):
    os.makedirs(model_save_dir)

def interpolate_data_with_spline(data, num_points):
    # Original indices
    original_indices = np.arange(len(data))

    # New indices with increased resolution
    new_indices = np.linspace(0, len(data) - 1, num=len(data) + (len(data) - 1) * num_points)

    # Creating a B-spline representation of the data
    spline_function = make_interp_spline(original_indices, data, k=3)  # k is the degree of the spline

    # Using the spline function to interpolate the new data points
    new_data = spline_function(new_indices)

    return new_data
'''
def interpolate_data(data):
    new_data = []
    for i in range(len(data) - 1):
        current_point = data[i]
        next_point = data[i + 1]
        midpoint = (current_point + next_point) / 2.0
        new_data.append(current_point)
        new_data.append(midpoint)
    new_data.append(data[-1])
    return np.array(new_data)
'''

def fetch_and_preprocess_data(base_currency, target_currencies, start_date, end_date):
    data_frames = []
    scaler_dict = {}

    for target_currency in target_currencies:
        # Fetch data
        url = f'https://api.frankfurter.app/{start_date}..{end_date}?from={base_currency}&to={target_currency}'
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data['rates']).T
        df.columns = [target_currency]
        df['date'] = pd.to_datetime(df.index)

        # Convert currency values to numpy array for interpolation
        currency_values = df[[target_currency]].values.flatten()

        # Interpolate data to increase dataset size
        interpolated_values = interpolate_data_with_spline(currency_values, 2)

        # After interpolation, reshape the data back to the original format
        df_interpolated = pd.DataFrame(interpolated_values, columns=[target_currency])

        # Assign dates to interpolated data if necessary or handle date column accordingly
        # Assuming your script already creates and fits a MinMaxScaler instance for each currency pair as shown:
        scaler = MinMaxScaler()
        currency_values_scaled = scaler.fit_transform(df_interpolated)
        # Save the fitted scaler
        scaler_filename = f'{model_save_dir}/scalers/{base_currency}_to_{target_currency}_scaler.joblib'
        if not os.path.exists(f'{model_save_dir}/scalers'):
            os.makedirs(f'{model_save_dir}/scalers')
        dump(scaler, scaler_filename)

        scaler_dict[target_currency] = scaler

        df_scaled = df_interpolated.copy()
        df_scaled[target_currency] = currency_values_scaled

        data_frames.append(df_scaled)

    return data_frames, scaler_dict

def create_sequences_multi(data_frames, n_steps):
    sequences = []
    for df in data_frames:
        if 'date' in df.columns:
            df = df.drop(columns=['date'])
        df = df.astype(np.float32)

        X, y = [], []
        data = df.values
        for i in range(n_steps, len(data)):
            X.append(data[i-n_steps:i])
            y.append(data[i, 0])
        sequences.append((np.array(X), np.array(y)))
    return sequences

from tensorflow.keras.layers import Bidirectional

def build_and_train_models(sequences, input_shape, target_currencies, epochs=50, batch_size=32):
    models = []
    for i, (X_train, y_train) in enumerate(sequences):
        model = Sequential([
          LSTM(50, activation='relu', input_shape=input_shape),
          Dense(1)
        ])
        optimizer = Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mean_absolute_error'])

        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        
        # Ensure the model checkpoint uses the currency code to create a unique filename
        # Note the change to .keras extension below
        model_filename = f'{model_save_dir}/{base_currency}_to_{target_currencies[i]}.keras'
        model_checkpoint = ModelCheckpoint(filepath=model_filename, monitor='val_loss', save_best_only=True, save_weights_only=False)
        
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)

        print(f"Training model for {base_currency} to {target_currencies[i]}")
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1, validation_split=0.2, callbacks=[early_stopping, model_checkpoint, reduce_lr])
        models.append(model)
    return models



def predict_and_evaluate(models, sequences, scaler_dict, target_currencies):
    for i, model in enumerate(models):
        X_test, y_test = sequences[i]
        predictions = model.predict(X_test)
        target_currency = target_currencies[i]
        scaler = scaler_dict[target_currency]

        predictions = scaler.inverse_transform(predictions)
        actual = scaler.inverse_transform(y_test.reshape(-1, 1))

        # Calculate RMSE
        rmse = sqrt(mean_squared_error(actual, predictions))
        ''''
        plt.figure(figsize=(10, 6))
        plt.plot(actual, label='Actual ' + target_currency)
        plt.plot(predictions, label='Predicted ' + target_currency, alpha=0.7)
        plt.title(f'Actual vs Predicted Exchange Rates for {target_currency}\nRMSE: {rmse:.4f}')
        plt.xlabel('Time')
        plt.ylabel('Exchange Rate')
        plt.legend()
        plt.show()
        
        '''


if __name__ == "__main__":
    base_currency = "EUR"
    target_currencies = ["GBP", "USD"]
    # target_currencies = ["USD", "GBP", "JPY", "CNY"]

    start_date = "1995-01-01"
    end_date = "2024-04-06"

    data_frames, scaler_dict = fetch_and_preprocess_data(base_currency, target_currencies, start_date, end_date)
    sequences = create_sequences_multi(data_frames, n_steps=60)
    input_shape = (sequences[0][0].shape[1], sequences[0][0].shape[2])

    models = build_and_train_models(sequences, input_shape, target_currencies)
    predict_and_evaluate(models, sequences, scaler_dict, target_currencies)
