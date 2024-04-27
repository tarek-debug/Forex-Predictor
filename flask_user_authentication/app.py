from flask import Flask, jsonify, request
from accounts import create_app

app = create_app()

# Add API route for fetching data
@app.route('/api/data', methods=['POST'])
def get_data():
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    base_currency = request.json['base_currency']
    target_currency = request.json['target_currency']

    # This would ideally call your data fetching logic or an external API
    data = {
        "start_date": start_date,
        "end_date": end_date,
        "base_currency": base_currency,
        "target_currency": target_currency,
        "rates": {
            "2021-01-01": 1.234,
            "2021-01-02": 1.235
        }
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
