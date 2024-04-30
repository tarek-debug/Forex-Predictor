from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your_random_secret_key_here'  # Keep this really secret!
GATEWAY_API_URL = "http://localhost:5001"

@app.route('/')
def home():
    # Check if the user is logged in
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.json
        response = requests.post(f"{GATEWAY_API_URL}/login", json=user_data)
        if response.status_code == 200:
            session['username'] = user_data['username']  # Save username in session
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'error': 'Login failed'}), response.status_code
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register():
    user_data = request.json
    response = requests.post(f"{GATEWAY_API_URL}/register", json=user_data)
    if response.status_code == 201:
        return jsonify({'success': True, 'message': 'Registration successful'})
    else:
        return jsonify({'error': 'Registration failed or username already exists'}), response.status_code

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' in session:
        user_data = request.get_json()
        user_data['username'] = session['username']  # Append username from session
        print(user_data)  # Debugging output
        response = requests.post(f"{GATEWAY_API_URL}/predict", json=user_data)
        print(response.status_code)  # Check status code
        print(response.text)  # Check raw response text
        if response.status_code == 200:
            try:
                return jsonify(response.json()), 200
            except ValueError:
                return jsonify({'error': 'Invalid JSON response'}), 500
        else:
            return jsonify({'error': 'Failed to predict'}), response.status_code
    else:
        return jsonify({'error': 'User not logged in'}), 401

@app.route('/history')
def history():
    if 'username' in session:
        username = session['username']
        return render_template('history.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/log_historical_data', methods=['POST'])
def log_historical_data():
    if 'username' in session:
        data = request.get_json()
        # Send data to gateway to be logged
        response = requests.post(f"{GATEWAY_API_URL}/store_historical_data", json=data)
        return jsonify(response.json()), response.status_code
    return jsonify({'error': 'User not logged in'}), 401
@app.route('/historical_data_history/<username>')
def historical_data_history(username):
    response = requests.post(f"{GATEWAY_API_URL}/fetch_historical_data", json={"username": username})
    return jsonify(response.json()), response.status_code

@app.route('/prediction_history/<username>')
def prediction_history(username):
    try:
        response = requests.post(f"{GATEWAY_API_URL}/fetch_predictions", json={"username": username})
        response.raise_for_status()  # Check for HTTP errors
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError:
        return jsonify({'error': 'Failed to fetch predictions from gateway'}), 500
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Network or connection issue'}), 500
    except ValueError:
        return jsonify({'error': 'Invalid JSON received'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the application on port 5000





''''

@app.route('/historical_data', methods=['GET', 'POST'])
def historical_data():
    if request.method == 'POST':
        data = request.form.to_dict()
        response = requests.post(f"{GATEWAY_API_URL}/historical_data_history", json=data)
        return jsonify(response.json()), response.status_code
    else:
        base_currency = request.args.get('base_currency', 'EUR')
        target_currency = request.args.get('target_currency', 'USD')
        response = requests.get(f"https://api.frankfurter.app/latest?from={base_currency}&to={target_currency}")
        return jsonify(response.json()), response.status_code

@app.route('/prediction_history/<username>', methods=['GET', 'POST'])
def prediction_history(username):
    if request.method == 'POST':
        response = requests.post(f"{GATEWAY_API_URL}/prediction_history", json={'username': username})
        return jsonify(response.json()), response.status_code
    else:
        response = requests.get(f"{GATEWAY_API_URL}/prediction_history/{username}")
        return jsonify(response.json()), response.status_code


@app.route('/historical_data_history', methods=['GET', 'POST'])
def historical_data_history():
    if request.method == 'POST':
        username = request.form['username']
        response = requests.post(f"{GATEWAY_API_URL}/historical_data_history", json={'username': username})
        return jsonify(response.json()), response.status_code
    else:
        username = request.args.get('username')
        response = requests.get(f"{GATEWAY_API_URL}/historical_data_history/{username}")
        return jsonify(response.json()), response.status_code

'''