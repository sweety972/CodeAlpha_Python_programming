import requests

def get_stock_data(symbol):
    api_key = 'W3CA8MQROGUHWN3V'  # Replace with your Alpha Vantage API key
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check if request was successful
        data = response.json()
        if 'Time Series (Daily)' in data:
            return data
        else:
            print(f"Error fetching data for {symbol}: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed for {symbol}: {e}")
        return None

