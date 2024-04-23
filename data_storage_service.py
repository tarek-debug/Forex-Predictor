from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

DATABASE_NAME = 'currency_exchange_insights.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS historical_data (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            currency TEXT NOT NULL,
            rate REAL NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            prediction_date TEXT NOT NULL,
            currency TEXT NOT NULL,
            predicted_rate REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/historical/<user_id>/<date>/<currency>', methods=['GET'])
def get_user_historical_data(user_id, date, currency):
    # Fetch historical data from Frankfurter API and filter by user_id
    response = requests.get(f'https://api.frankfurter.app/{date}?from={currency[:3]}&to={currency[3:]}')
    if response.status_code == 200:
        data = response.json()
        rate = data['rates'][currency[3:]]
        # Store fetched data in the database with user_id
        conn = get_db_connection()
        conn.execute('INSERT INTO historical_data (user_id, date, currency, rate) VALUES (?, ?, ?, ?)',
                     (user_id, date, currency, rate))
        conn.commit()
        conn.close()
        return jsonify({'user_id': user_id, 'date': date, 'currency': currency, 'rate': rate})
    else:
        return jsonify({'error': 'Failed to fetch data from Frankfurter API'}), 500

@app.route('/historical/user/<user_id>', methods=['GET'])
def get_historical_data_by_user(user_id):
    # Retrieve historical data for a specific user
    conn = get_db_connection()
    historical_data = conn.execute('SELECT * FROM historical_data WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in historical_data])

@app.route('/predictions', methods=['POST'])
def add_prediction():
    prediction_data = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO predictions (user_id, prediction_date, currency, predicted_rate) VALUES (?, ?, ?, ?)',
                 (prediction_data['user_id'], prediction_data['prediction_date'], prediction_data['currency'], prediction_data['predicted_rate']))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 201

@app.route('/predictions/<user_id>', methods=['GET'])
def get_predictions(user_id):
    conn = get_db_connection()
    predictions = conn.execute('SELECT * FROM predictions WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in predictions])

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)