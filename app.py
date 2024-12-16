from flask import Flask, jsonify, render_template, request
import requests
import os

app = Flask(__name__)
API_URL = "https://www.alphavantage.co/query"
API_KEY = os.getenv("API_KEY", "No API Key Provided")


# @app.route("/")
# def index():
#     return render_template("index.html")  # Serve the HTML form


@app.route("/", methods=["GET", "POST"])
def import_symbol():
    # Get the symbol from the form
    symbol = request.form.get("symbol")
    stock_data = None
    error_message = None
    if symbol:
        # Handle the import logic here
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': '1min',
            'apikey': API_KEY,
        }
        response = requests.get(API_URL, params=params)
        data = response.json()

    # Check if response contains valid data
        if 'Time Series (1min)' in data:
            latest_time = list(data['Time Series (1min)'])[0]
            latest_data = data['Time Series (1min)'][latest_time]
            stock_data = {
                'symbol': symbol,
                'price': latest_data['1. open'],
                'time': latest_time
            }
        else:
            error_message = f"Error fetching data for symbol: {symbol}. Details: {str(e)}"
        # return f"Import logic for symbol: {symbol}"
    else:
        error_message = "Please provide a valid symbol."
    print(stock_data)
    return render_template("index.html", stock_data=stock_data, error_message=error_message)


@app.route('/stock/<string:symbol>', methods=['GET'])
def get_stock_price(symbol):
    print("Hello")
    """Fetch real-time stock price for the given symbol."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY,
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    # Check if response contains valid data
    if 'Time Series (1min)' in data:
        latest_time = list(data['Time Series (1min)'])[0]
        latest_data = data['Time Series (1min)'][latest_time]
        return jsonify({
            'symbol': symbol,
            'price': latest_data['1. open'],
            'time': latest_time
        })
    else:
        return jsonify({'error': 'Could not fetch data'}), 400


if __name__ == '__main__':
    app.run(debug=True)
