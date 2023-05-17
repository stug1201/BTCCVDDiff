import matplotlib.pyplot as plt
from BTCSpotCVD import getBTCSpotCVD
from BTCPerpCVD import getBTCPerpCVD
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import time
import requests

# Function to get BTC price data for the specified interval
def getBTCPrice():

    # Construct the API endpoint URL
    url = f'https://data.binance.com/api/v3/klines'
    params = {
        'symbol': 'BTCUSDT',
        'interval': '5m',
    }

    # Set the API key as a header
    headers = {
        'X-MBX-APIKEY': '' # Insert Binance read-only API key here
    }
    
    # Make the API request
    response = requests.get(url, params=params)
    data = response.json()

    # Extract the price data from the response
    price_data = [float(entry[1]) for entry in data]
    return price_data

# Get BTC spot CVD data
btc_spot_cvd_data = getBTCSpotCVD()

# Get BTC perpetual CVD data
btc_perp_cvd_data = getBTCPerpCVD()

# Get BTC price data
btc_price_data = getBTCPrice()

# Ensure the length of BTC price data matches the CVD data
btc_price_data = btc_price_data[:len(btc_spot_cvd_data)]

# Create an instance of MinMaxScaler
scaler = MinMaxScaler()

# Reshape the BTC Spot CVD and BTC Perp CVD values to a 2D array (required by the scaler)
btc_spot_cvd_values = btc_spot_cvd_data.values.reshape(-1, 1)
btc_perp_cvd_values = btc_perp_cvd_data.values.reshape(-1, 1)

# Normalize the BTC Spot CVD and BTC Perp CVD values using min-max scaling
normalized_btc_spot_cvd = scaler.fit_transform(btc_spot_cvd_values)
normalized_btc_perp_cvd = scaler.fit_transform(btc_perp_cvd_values)

# Convert the normalized values back to Series
normalized_btc_spot_cvd = pd.Series(normalized_btc_spot_cvd.flatten(), index=btc_spot_cvd_data.index)
normalized_btc_perp_cvd = pd.Series(normalized_btc_perp_cvd.flatten(), index=btc_perp_cvd_data.index)

# Calculate the difference between normalized BTC Spot CVD and BTC Perp CVD
cvd_difference = normalized_btc_spot_cvd - normalized_btc_perp_cvd

# Ensure the length of CVD difference matches the BTC price data
cvd_difference = cvd_difference[:len(btc_price_data)]

# Increase the figure size and adjust font sizes
plt.rcParams['figure.figsize'] = (16, 8)
plt.rcParams['font.size'] = 14

# Create the figure and axes
fig, ax1 = plt.subplots(figsize=(16, 8))

# Plot the difference
ax1.plot(cvd_difference, label='Difference', color='purple')
ax1.set_ylabel('Difference')
ax1.tick_params(axis='y')

# Create a twin y-axis for BTC price
ax2 = ax1.twinx()
ax2.plot(btc_price_data, color='blue', label='BTC Price')
ax2.set_ylabel('BTC Price')

# Set the x-axis label and title
ax1.set_xlabel('Timestamp')
ax1.set_title('BTC Price vs CVD Difference')

# Show the legend
ax1.legend()

# Display the plot
plt.tight_layout()
plt.show()
