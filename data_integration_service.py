"""
Fetches and stores currency exchange rates from the Frankfurter API.
"""

import requests
import psycopg2
from datetime import datetime
import schedule
import time

# Database configuration - Replace with your actual database credentials
DATABASE_CONFIG = {
    'user': 'postgres',
    'password': 'scomac211',
    'host': 'localhost',
    'port': '5432', #default port for PostgreSQL
    'database': 'currency_db'
}

def fetch_exchange_rates(base_currency="EUR", symbols=None):
    """
    Fetches the latest exchange rates for the given base currency and target symbols.
    """
    url = "https://api.frankfurter.app/latest"
    params = {"from": base_currency}
    if symbols:
        params["symbols"] = ','.join(symbols)
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        return data
    else:
        raise Exception(f"Failed to fetch data: {data.get('error', 'Unknown error')}")

def insert_exchange_rate(date, base_currency, target_currency, rate):
    """
    Inserts an exchange rate into the database, updating the entry if it already exists.
    """
    rate = round(rate, 6) #rate has no more than 6 digits after the decimal point before attempting to insert it into the database
    connection = psycopg2.connect(**DATABASE_CONFIG)
    cursor = connection.cursor()
    
    insert_query = """INSERT INTO exchange_rates (date, base_currency, target_currency, rate)
                      VALUES (%s, %s, %s, %s)
                      ON CONFLICT (date, base_currency, target_currency) DO UPDATE
                      SET rate = EXCLUDED.rate;"""
    cursor.execute(insert_query, (date, base_currency, target_currency, rate))
    
    connection.commit()
    cursor.close()
    connection.close()

def job():
    """
    Scheduled job to fetch and store exchange rates daily.
    """
    print(f"Fetching and storing exchange rates at {datetime.now()}...")
    data = fetch_exchange_rates()  # Fetch exchange rates for the default base currency (EUR)
    
    # Insert each exchange rate into the database
    for target_currency, rate in data['rates'].items():
        insert_exchange_rate(data['date'], data['base'], target_currency, rate)

# Schedule the job to run every minute
schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)  # Wait for 1 second before checking again
