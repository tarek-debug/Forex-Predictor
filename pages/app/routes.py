from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_swagger_ui import get_swaggerui_blueprint
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_random_secret_key_here'  # Keep this really secret!
GATEWAY_API_URL = os.environ.get('GATEWAY_API_URL', 'http://localhost:5001')

# Swagger UI configuration
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can be a static file or dynamically generated)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Your Application API"
    },
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/enable-swagger')
def enable_swagger():
    session['enable_swagger'] = True
    return redirect(SWAGGER_URL)

@app.route('/')
def home():
    # Check if the user is logged in
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/health')
def health_check():
    # Add your custom health check logic here
    if all_required_services_are_running():
        return 'OK', 200
    else:
        return 'Service Unavailable', 500

def all_required_services_are_running():
    # Replace this with your actual logic to check the health of your services
    return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.json
        response = requests.post(f"{GATEWAY_API_URL}/login", json=user_data)
        if response.status_code == 200:
            session['username'] = user_data['username']
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
        # Include 'username' from session into the data being sent to the gateway
        user_data['username'] = session['username']
        print(user_data)
        response = requests.post(f"{GATEWAY_API_URL}/predict", json=user_data)
        if response.status_code == 200:
            try:
                return jsonify(response.json()), 200
            except ValueError:
                return jsonify({'error': 'Invalid JSON response'}), 500
        else:
            return jsonify({'error': 'Failed to predict'}), response.status_code
    else:
        return jsonify({'error': 'User not logged in'}), 401

@app.route('/learnmore')
def learn_more():
    if 'username' in session:
        return render_template('learnmore.html')
    else:
        return redirect(url_for('login'))

@app.route('/history')
def history():
    if 'username' in session:
        return render_template('history.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/log_historical_data', methods=['POST'])
def log_historical_data():
    if 'username' in session:
        data = request.get_json()
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
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError:
        return jsonify({'error': 'Failed to fetch predictions from gateway'}), 500
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Network or connection issue'}), 500
    except ValueError:
        return jsonify({'error': 'Invalid JSON received'}), 500

@app.route('/delete_prediction/<int:index>', methods=['DELETE'])
def delete_prediction(index):
    if 'username' in session:
        response = requests.delete(f"{GATEWAY_API_URL}/delete_prediction/{session['username']}/{index}")
        return jsonify(response.json()), response.status_code
    return jsonify({'error': 'User not logged in'}), 401

@app.route('/clear_predictions', methods=['DELETE'])
def clear_predictions():
    if 'username' in session:
        response = requests.delete(f"{GATEWAY_API_URL}/clear_predictions/{session['username']}")
        return jsonify(response.json()), response.status_code
    return jsonify({'error': 'User not logged in'}), 401

@app.route('/delete_historical_data/<int:index>', methods=['DELETE'])
def delete_historical_data(index):
    if 'username' in session:
        response = requests.delete(f"{GATEWAY_API_URL}/delete_historical_data/{session['username']}/{index}")
        return jsonify(response.json()), response.status_code
    return jsonify({'error': 'User not logged in'}), 401

@app.route('/clear_historical_data', methods=['DELETE'])
def clear_historical_data():
    if 'username' in session:
        response = requests.delete(f"{GATEWAY_API_URL}/clear_historical_data/{session['username']}")
        return jsonify(response.json()), response.status_code
    return jsonify({'error': 'User not logged in'}), 401

if __name__ == '__main__':
    app.run(debug=True)  # Run the application on port 5000
