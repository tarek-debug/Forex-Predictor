from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define URLs for each service
DATA_STORAGE_SERVICE_URL = 'http://localhost:5000'
PREDICTION_SERVICE_URL = 'http://localhost:5002'

# Login Functionality
@app.route('/ui/login', methods=['POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    user_data = request.json if request.method == 'POST' else request.args
    response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/validate_login", json=user_data)
    return jsonify(response.json()), response.status_code

# Register Functionality
@app.route('/ui/register', methods=['POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    user_data = request.json if request.method == 'POST' else request.args
    response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/register", json=user_data)
    return jsonify(response.json()), response.status_code

# Predict Functionality
@app.route('/ui/predict', methods=['POST'])
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    data = request.json if request.method == 'POST' else request.args
    username = data.get('username')
    response = requests.post(f"{PREDICTION_SERVICE_URL}/predict", json=data)
    # Store prediction results in data storage
    if response.status_code == 200:
        store_response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/predictions", json={"username": username, "predictions": response.json()})
        return jsonify(store_response.json()), store_response.status_code
    return jsonify(response.json()), response.status_code

# Historical Data History Functionality
@app.route('/ui/historical_data_history', methods=['GET', 'POST'])
@app.route('/historical_data_history/<username>', methods=['GET', 'POST'])
def historical_data_history(username):
    if request.method == 'POST':
        response = requests.post(f"{DATA_STORAGE_SERVICE_URL}/store_historical", json={'username': username})
    else:
        response = requests.get(f"{DATA_STORAGE_SERVICE_URL}/historical/{username}")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=5001, debug=True)
