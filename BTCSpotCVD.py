import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

api_key_var = '' # Insert Coinalyze API key here
symbols = ['BTCUSD.A', 'BTCUSDT.F', 'BTCUSDT.K', 'BTCUSDT.C', 'sBTCUSDT.6', 'XBT_USDT.0', 'BTCUSDT.B']
symbol_names = ['Binance', 'Bitfinex', 'Kraken', 'Coinbase', 'Bybit', 'BitMEX', 'Bitstamp']
interval = '5min'  # Replace with the desired interval (e.g., 1min, 5min, 15min, 30min, 1hour)
limit = 100  # Replace with the number of data points you want to retrieve

# Convert the interval to seconds
interval_mapping = {
    '1min': 60,
    '5min': 300,
    '15min': 900,
    '30min': 1800,
    '1hour': 3600
}
    
interval_seconds = interval_mapping.get(interval)

# Calculate the start and end timestamps
end_timestamp = int(time.time())
start_timestamp = end_timestamp - (limit * interval_seconds)

# Construct the API endpoint URL with start and end timestamps
url = f'https://api.coinalyze.net/v1/ohlcv-history'
params = {
    'api_key': api_key_var,
    'symbols': ','.join(symbols),  # Join the symbols with comma separator
    'interval': interval,
    'from': start_timestamp,
    'to': end_timestamp
}   

# Set the API key as a header
headers = {
    'api_key': f'{api_key_var}'
}

# Make the API request
response = requests.get(url, params)

# Check if the request was successful
    
if response.status_code == 200:
    # Parse the response JSON data
    data = response.json()

    # Create empty lists to store the extracted data
    timestamps = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    volumes = []
    buy_volumes = []
    trade_count = []
    buy_trade_count = []
    symbols_list = []

    # Iterate over each symbol's history and extract the values
    for symbol_data in data:
        symbol = symbol_data['symbol']
        history = symbol_data['history']

        for item in history:
            timestamps.append(item['t'])
            open_prices.append(item['o'])
            high_prices.append(item['h'])
            low_prices.append(item['l'])
            close_prices.append(item['c'])
            volumes.append(item['v'])
            buy_volumes.append(item['bv'])
            trade_count.append(item['tx'])
            buy_trade_count.append(item['btx'])
            symbols_list.append(symbol)

    # Create a dictionary with the extracted data
    data_dict = {
        'Symbol': symbols_list,
        'Timestamp': timestamps,
        'Open': open_prices,
        'High': high_prices,
        'Low': low_prices,
        'Close': close_prices,
        'Volume': volumes,
        'Buy Volume': buy_volumes,
        'Trade Count': trade_count,
        'Buy Trade Count': buy_trade_count
    }

    # Create a pandas DataFrame from the dictionary
    df = pd.DataFrame(data_dict)

    # Rename symbols in the DataFrame
    symbol_mapping = dict(zip(symbols, symbol_names))
    df['Symbol'] = df['Symbol'].map(symbol_mapping)
    
    # Calculate CVD
    df['CVD'] = df.groupby('Timestamp')['Buy Volume'].transform('sum') - df.groupby('Timestamp')['Volume'].transform('sum')
    
    # Normalize CVD
    df['CVD'] = df['CVD'] - df['CVD'].iloc[0]
    
# Error handling
else:
    print('Error occurred while fetching data:', response.text)
    
def getBTCSpotCVD(): 
    return df['CVD']
