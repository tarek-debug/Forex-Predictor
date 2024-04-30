from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define URLs for each service
PREDICTION_SERVICE_URL = 'http://localhost:5002'
DATA_STORAGE_SERVICE_URL = 'http://localhost:5003'

@app.route('/login', methods=['POST'])
def login():
    user_data = request.json
    response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/validate_login", json=user_data)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Login failed"}), response.status_code

@app.route('/register', methods=['POST'])
def register():
    user_data = request.json
    response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/register", json=user_data)
    if response.status_code == 201:
        return jsonify({"message": "Registration successful"}), 201
    else:
        return jsonify({"error": "Registration failed"}), response.status_code

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction_response = requests.post(f"{PREDICTION_SERVICE_URL}/predict", json=data)
    if prediction_response.status_code in [200, 201]:
        predictions = prediction_response.json()
        print(predictions)
        store_response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/predictions", json={"username": data.get('username'), "predictions": predictions})
        if store_response.status_code in [200, 201]:
            return jsonify(predictions), 200
        else:
            print(f"Failed to store predictions: {store_response.text}")  # Log the error message from storage service
            return jsonify({"error": "Failed to store predictions"}), store_response.status_code
    else:
        return jsonify({"error": "Prediction service failed"}), prediction_response.status_code

@app.route('/store_historical_data', methods=['POST'])
def store_historical_data():
    data = request.json
    response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/store_historical", json=data)
    if response.status_code == 200:
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Failed to store data'}), response.status_code
@app.route('/fetch_historical_data', methods=['POST'])
def fetch_historical_data():
    user_data = request.json
    response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/get_historical_data", json=user_data)
    return jsonify(response.json()), response.status_code


@app.route('/fetch_predictions', methods=['POST'])
def fetch_predictions():
    user_data = request.json
    try:
        response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/get_predictions", json=user_data)
        response.raise_for_status()  # This will raise an exception for HTTP error responses
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as e:
        return jsonify({'error': 'Prediction service failed', 'details': str(e)}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Network or connection error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)