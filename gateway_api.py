from flask import Flask, request, jsonify, redirect
import requests

app = Flask(__name__)
DATA_STORAGE_SERVICE_URL = 'http://localhost:5000'  # URL of the data storage service

@app.route('/login', methods=['POST'])
def login():
    # Receives user credentials and validates them with the data storage service
    user_data = request.json  # Extract JSON data from request
    response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/validate_login", json=user_data)
    # Responds based on the validation result
    if response.status_code == 200:
        return jsonify({'success': True, 'message': 'Login successful'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    # Registers a new user by sending their data to the data storage service
    user_data = request.json
    response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/register", json=user_data)
    # Returns the response from the data storage service
    return jsonify(response.json()), response.status_code

@app.route('/get_data', methods=['GET'])
def get_data():
    # Fetches historical and predictive data for a specific user
    user_id = request.args.get('user_id')  # Get user ID from query parameters
    historical_response = requests.get(f"{DATA_STORAGE_SERVICE_URL}/get_historical", params={'user_id': user_id})
    predictions_response = requests.get(f"{DATA_STORAGE_SERVICE_URL}/get_predictions", params={'user_id': user_id})
    data = {
        'historical_data': historical_response.json(),
        'predictions_data': predictions_response.json()
    }
    # Combines and returns the data for the user
    return jsonify(data), 200

if __name__ == '__main__':
    # Runs the Flask application on port 5001 in debug mode
    app.run(port=5001, debug=True)