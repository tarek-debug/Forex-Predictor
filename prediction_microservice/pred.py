from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

# Dictionary to cache loaded models
models_cache = {}

def get_model_path(base_currency, target_currency):
    # Path where your models are saved
    return f'saved_models/model_{base_currency}_to_{target_currency}.h5'

def load_model_from_cache(base_currency, target_currency):
    model_key = f"{base_currency}_to_{target_currency}"
    if model_key not in models_cache:
        model_path = get_model_path(base_currency, target_currency)
        try:
            # Load the model and add it to the cache
            model = tf.keras.models.load_model(model_path)
            models_cache[model_key] = model
        except IOError as e:
            # If the model could not be found, raise an error
            raise BadRequest(f"Model for {base_currency} to {target_currency} not found. Error: {e}")
    return models_cache[model_key]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    
    # Validate input
    if 'base_currency' not in data or 'target_currency' not in data or 'sequence' not in data:
        raise BadRequest("Request must contain base_currency, target_currency, and sequence.")
    
    base_currency = data['base_currency']
    target_currency = data['target_currency']
    sequence = data['sequence']
    
    # Load model for the specified currencies
    model = load_model_from_cache(base_currency, target_currency)
    
    # Make prediction
    prediction = model.predict(np.array([sequence]))
    return jsonify(prediction.tolist())

if __name__ == '__main__':
    # Running on port 5001 to avoid conflicts with the main application
    app.run(debug=True, port=5001)
