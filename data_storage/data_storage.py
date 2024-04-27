from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Define the paths to the JSON storage files
CREDENTIALS_FILE = 'data_storage/credentials.json'
PREDICTIONS_FILE = 'data_storage/pred_storage.json'
HISTORICAL_DATA_FILE = 'data_storage/historical_data_storage.json'

# Helper function to read data from a JSON file
def read_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Helper function to write data to a JSON file
def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Register a new user
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

# Store new historical data
@app.route('/store_historical', methods=['POST'])
def store_historical_data():
    data = request.json
    historical_data = read_json(HISTORICAL_DATA_FILE)
    username = data['username']
    if username not in historical_data:
        historical_data[username] = []
    historical_data[username].append(data)
    write_json(historical_data, HISTORICAL_DATA_FILE)
    return jsonify({'success': True}), 201

# Get historical data for a specific user
@app.route('/historical/<username>', methods=['GET'])
def get_historical_data(username):
    historical_data = read_json(HISTORICAL_DATA_FILE)
    user_data = historical_data.get(username, [])
    return jsonify(user_data), 200

# Store new prediction data
@app.route('/predictions', methods=['POST'])
def add_prediction():
    data = request.json
    predictions = read_json(PREDICTIONS_FILE)
    username = data['username']
    if username not in predictions:
        predictions[username] = []
    predictions[username].append(data)
    write_json(predictions, PREDICTIONS_FILE)
    return jsonify({'success': True}), 201

# Get predictions for a specific user
@app.route('/predictions/<username>', methods=['GET'])
def get_predictions(username):
    predictions = read_json(PREDICTIONS_FILE)
    user_data = predictions.get(username, [])
    return jsonify(user_data), 200

if __name__ == '__main__':
    app.run(debug=True)
