import requests
import json
from flask import Flask, jsonify

app = Flask(__name__)

portfolio = {
    'AAPL': {'quantity': 10, 'weight': 0.2},
    'MSFT': {'quantity': 15, 'weight': 0.25},
    'GOOGL': {'quantity': 8, 'weight': 0.2},
    'AMZN': {'quantity': 5, 'weight': 0.15},
    'FB': {'quantity': 12, 'weight': 0.2}
}

@app.route('/')
def home():
    return "Welcome to WealthWise - your trusted portfolio building buddy!"

@app.route('/stock/<symbol>')
def stock(symbol):
    api_key = "OMLTKM3U67PVKJVJ"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        return "Error: Unable to fetch stock data."

    data = json.loads(response.text)

    if "Error Message" in data:
        return jsonify({"error": data["Error Message"]}), 400

    return jsonify(data)

@app.route('/portfolio')
def get_portfolio():
    results = {}
    for symbol in portfolio:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=OMLTKM3U67PVKJVJ"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            results[symbol] = data
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)