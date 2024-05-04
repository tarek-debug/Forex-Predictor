from datetime import datetime
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Define the paths to the JSON storage files
CREDENTIALS_FILE = 'storage/credentials.json'
PREDICTIONS_FILE = 'storage/pred_storage.json'
HISTORICAL_DATA_FILE = 'storage/historical_data_storage.json'

def read_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/health')
def health_check():
    # Add your custom health check logic here
    print("checking health")
    if all_required_services_are_running():
        return 'OK', 200
    else:
        return 'Service Unavailable', 500
# Example health check logic, replace it with your actual logic
def all_required_services_are_running():
    # Replace this with your logic to check the health of your services
    # For example, check if the required processes are running
    return True

@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.json
    users = read_json(CREDENTIALS_FILE)
    username = user_data['username']
    if username in users:
        return jsonify({'error': 'Username already exists'}), 409
    users[username] = user_data
    write_json(users, CREDENTIALS_FILE)
    return jsonify({'success': True}), 201

@app.route('/validate_login', methods=['POST'])
def validate_login():
    credentials = request.json
    users = read_json(CREDENTIALS_FILE)
    username = credentials['username']
    password = credentials['password']
    if username in users and users[username]['password'] == password:
        return jsonify({'success': True, 'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/store_historical', methods=['POST'])
def store_historical():
    data = request.json
    historical_data = read_json(HISTORICAL_DATA_FILE)
    username = data['username']
    if username not in historical_data:
        historical_data[username] = []

    # Create a new entry including both the request and the response
    historical_entry = {
        'timestamp': datetime.now().isoformat(),
        'request_data': {
            'base_currency': data['base_currency'],
            'target_currency': data['target_currency'],
            'date': data['date']
        },
        'response_data': data['response']  # Assuming 'response' contains the historical data fetched
    }
    historical_data[username].append(historical_entry)
    write_json(historical_data, HISTORICAL_DATA_FILE)
    return jsonify({'success': True}), 201




@app.route('/log_predictions', methods=['POST'])
def add_prediction():
    data = request.json
    predictions = read_json(PREDICTIONS_FILE)
    username = data['username']

    if username not in predictions:
        predictions[username] = []

    current_time = datetime.now().isoformat()

    prediction_entry = {
        "timestamp": current_time,
        "data": data
    }
    # Function to check for duplicates based on key prediction details
    def is_duplicate(new_data, existing_entries):
        new_pred = new_data['data']['predictions']
        for entry in existing_entries:
            if entry['data']['predictions'] == new_pred:
                return True
        return False

    # Check for duplicates before appending
    if not is_duplicate(prediction_entry, predictions[username]):
        predictions[username].append(prediction_entry)
        write_json(predictions, PREDICTIONS_FILE)
        return jsonify({'success': True}), 201
    else:
        return jsonify({'message': 'Duplicate prediction, not added'}), 200
    
@app.route('/get_historical_data', methods=['POST'])
def get_historical_data():
    username = request.json.get('username')
    historical_data = read_json(HISTORICAL_DATA_FILE)
    user_data = historical_data.get(username, [])
    return jsonify(user_data), 200

@app.route('/get_predictions', methods=['POST'])
def get_predictions():
    username = request.json.get('username')
    predictions = read_json(PREDICTIONS_FILE)
    user_data = predictions.get(username, [])
    return jsonify(user_data), 200

@app.route('/delete_prediction/<username>/<int:index>', methods=['DELETE'])
def delete_prediction(username, index):
    predictions = read_json(PREDICTIONS_FILE)
    if username in predictions and len(predictions[username]) > index:
        del predictions[username][index]
        write_json(predictions, PREDICTIONS_FILE)
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route('/clear_predictions/<username>', methods=['DELETE'])
def clear_predictions(username):
    predictions = read_json(PREDICTIONS_FILE)
    if username in predictions:
        predictions[username] = []
        write_json(predictions, PREDICTIONS_FILE)
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route('/delete_historical_data/<username>/<int:index>', methods=['DELETE'])
def delete_historical_data(username, index):
    historical_data = read_json(HISTORICAL_DATA_FILE)
    if username in historical_data and len(historical_data[username]) > index:
        del historical_data[username][index]
        write_json(historical_data, HISTORICAL_DATA_FILE)
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route('/clear_historical_data/<username>', methods=['DELETE'])
def clear_historical_data(username):
    historical_data = read_json(HISTORICAL_DATA_FILE)
    if username in historical_data:
        historical_data[username] = []
        write_json(historical_data, HISTORICAL_DATA_FILE)
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
