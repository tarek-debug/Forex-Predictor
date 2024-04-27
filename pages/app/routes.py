from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests

app = Flask(__name__)

GATEWAY_API_URL = "http://localhost:5001"  # Adjust if your gateway API is hosted differently

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        response = requests.post(f"{GATEWAY_API_URL}/ui/login", json=user_data)
        if response.status_code == 200:
            return redirect(url_for('dashboard'))  # Redirect to a dashboard if login is successful
        else:
            return render_template('login.html', error="Login failed.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        response = requests.post(f"{GATEWAY_API_URL}/ui/register", json=user_data)
        if response.status_code == 201:
            return redirect(url_for('login'))  # Redirect to login page after registration
        else:
            return render_template('register.html', error="Registration failed or username already exists.")
    return render_template('register.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        prediction_data = request.form.to_dict()
        response = requests.post(f"{GATEWAY_API_URL}/ui/predict", json=prediction_data)
        return jsonify(response.json()), response.status_code
    return render_template('predict.html')

@app.route('/historical_data', methods=['GET', 'POST'])
def historical_data():
    if request.method == 'POST':
        data = request.form.to_dict()
        response = requests.post(f"{GATEWAY_API_URL}/ui/historical_data_history", json=data)
        return jsonify(response.json()), response.status_code
    else:
        base_currency = request.args.get('base_currency', 'EUR')
        target_currency = request.args.get('target_currency', 'USD')
        response = requests.get(f"https://api.frankfurter.app/latest?from={base_currency}&to={target_currency}")
        return jsonify(response.json()), response.status_code

@app.route('/prediction_history', methods=['GET', 'POST'])
def prediction_history():
    if request.method == 'POST':
        username = request.form['username']
        # Assuming the API has a method to clear history
        response = requests.post(f"{GATEWAY_API_URL}/ui/prediction_history", json={'username': username})
        return jsonify(response.json()), response.status_code
    else:
        username = request.args.get('username')
        response = requests.get(f"{GATEWAY_API_URL}/ui/prediction_history/{username}")
        return jsonify(response.json()), response.status_code

@app.route('/historical_data_history', methods=['GET', 'POST'])
def historical_data_history():
    if request.method == 'POST':
        username = request.form['username']
        # Assuming the API has a method to clear history
        response = requests.post(f"{GATEWAY_API_URL}/ui/historical_data_history", json={'username': username})
        return jsonify(response.json()), response.status_code
    else:
        username = request.args.get('username')
        response = requests.get(f"{GATEWAY_API_URL}/ui/historical_data_history/{username}")
        return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5003)  # Set to a different port if your gateway is running on the same machine
