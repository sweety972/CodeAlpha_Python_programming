# test_stock_data.py
import requests

def get_stock_data(symbol):
    api_key = 'W3CA8MQROGUHWN3V'
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Test the API connection with a stock symbol
if __name__ == '__main__':
    symbol = 'AAPL'  # Apple stock
    stock_data = get_stock_data(symbol)
    if 'Time Series (Daily)' in stock_data:
        print("Stock data fetched successfully")
    else:
        print("Failed to fetch stock data:", stock_data)
