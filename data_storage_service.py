# Import necessary modules from Flask, sqlite3 for database operations, and requests for making HTTP requests
from flask import Flask, request, jsonify
import sqlite3
import requests

# Create a Flask application instance
app = Flask(__name__)

# Define the database file name
DATABASE_NAME = 'currency_exchange_insights.db'

# Function to get a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)  # Connect to the SQLite database
    conn.row_factory = sqlite3.Row  # Configure connection to return rows that behave like dictionaries
    return conn

# Function to create necessary tables in the database
def create_tables():
    conn = get_db_connection()  # Get a database connection
    # SQL to create a table for storing historical data if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS historical_data (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            currency TEXT NOT NULL,
            rate REAL NOT NULL
        )
    ''')
    # SQL to create a table for storing predictions if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            prediction_date TEXT NOT NULL,
            currency TEXT NOT NULL,
            predicted_rate REAL NOT NULL
        )
    ''')
    conn.commit()  # Commit changes to the database
    conn.close()  # Close the database connection

# Define a new route '/store_historical' that listens for POST requests
@app.route('/store_historical', methods=['POST'])
def store_historical_data():
    data = request.json # Retrieve JSON data from the POST request
    conn = get_db_connection() # Establish a database connection using a helper function
    # Execute an SQL INSERT command to store the received data into the 'historical_data' table
    conn.execute('INSERT INTO historical_data (user_id, date, currency, rate) VALUES (?, ?, ?, ?)',
                 (data['user_id'], data['date'], data['currency'], data['rate']))
    conn.commit() # Commit the transaction to make sure that the changes are saved to the database
    conn.close() # Close the database connection after the operation is complete
    return jsonify({'success': True}), 201

# Define a route to get historical data for a specific user, to send to front end
@app.route('/historical/user/<user_id>', methods=['GET'])
def get_historical_data_by_user(user_id):
    conn = get_db_connection()  # Get a database connection
    # Retrieve all historical records for the specified user ID
    historical_data = conn.execute('SELECT * FROM historical_data WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()  # Close the database connection
    return jsonify([dict(ix) for ix in historical_data])  # Convert each row to a dictionary and return as JSON

# Define a route to store new prediction via a POST request, data recieved by predictions model
@app.route('/predictions', methods=['POST'])
def add_prediction():
    prediction_data = request.json  # Get JSON data sent with the POST request
    conn = get_db_connection()  # Get a database connection
    # Insert prediction data into the predictions table
    conn.execute('INSERT INTO predictions (user_id, prediction_date, currency, predicted_rate) VALUES (?, ?, ?, ?)',
                 (prediction_data['user_id'], prediction_data['prediction_date'], prediction_data['currency'], prediction_data['predicted_rate']))
    conn.commit()  # Commit changes to the database
    conn.close()  # Close the database connection
    return jsonify({'success': True}), 201

# Define a route to get predictions for a specific user, to send to front end
@app.route('/predictions/<user_id>', methods=['GET'])
def get_predictions(user_id):
    conn = get_db_connection()  # Get a database connection
    # Retrieve all prediction records for the specified user ID
    predictions = conn.execute('SELECT * FROM predictions WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()  # Close the database connection
    return jsonify([dict(ix) for ix in predictions])  # Convert each row to a dictionary and return as JSON

# Users will send their registration data, stored in the users table
@app.route('/register', methods=['POST'])
def register_user():
    # Get the JSON data sent with the POST request. This typically contains the username and password.
    data = request.json
    username = data['username']  # Extract the 'username' from the JSON data.
    password = data['password']  # Extract the 'password' from the JSON data. 
    # Hash the password using SHA-256, converting the password to bytes before hashing. This is a basic form of password security.
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # Try to execute the database operation within a try block to handle exceptions.
    try:
        conn = get_db_connection()  # Establish a connection to the database using a previously defined function.
        # Insert the new username and the hashed password into the 'users' table.
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                     (username, password_hash))
        conn.commit()  # Commit the transaction to save the changes to the database.
    except sqlite3.IntegrityError:
        # If an IntegrityError occurs (e.g., the username already exists due to a UNIQUE constraint), return an error message.
        return jsonify({'error': 'Username already exists'}), 409
    finally:
        # Ensure that the database connection is closed regardless of whether the try block succeeds or an exception occurs.
        conn.close()
    # If everything is successful, return a JSON response indicating success and a 201 status code (Created).
    return jsonify({'success': True}), 201

# Main block to create tables and run the Flask application if this script is executed as the main program
if __name__ == '__main__':
    create_tables()  # Ensure necessary tables are created
    app.run(debug=True)  # Start the Flask application in debug mode