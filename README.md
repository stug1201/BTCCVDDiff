# BTCCVDDiff
Calculates and charts the difference in CVD across exchanges for BTC spot and perp markets against the price of BTC for that period.

## Calculation code
The BTCSpotCVD.py and BTCPerpCVD.py calculate CVD for each exchange in a preset list and add them all up. This is taken to be a measure of net buying or selling in the specific instrument across the market. All of the data is pulled for the BTC/USDT pair, but this code could easily be adapted to work for ETH/USDT or other pairs.

### Presets
Exchange list for spot: Binance, Bitfinex, Kraken, Coinbase, Bybit, BitMEX, Bitstamp
<br> Exchange list for perp: Bybit, Binance, Huobi, Bitfinex, BitMEX, OKX </br>

#### Variables
'limit' - refers to the number of datapoints taken per exchange, set to 100 but can be increased to 500 
<br> 'interval' - refers to the time interval that each datapoint represents, best use has been on the 5 minute interval </br>

## Graphing code
When Main.py is run, it runs BTCSpotCVD.py and BTCPerpCVD.py, uses the CVD data from both to calculate the difference in CVD from the spot market and the perp market. This is then normalised using a standard min-max function, and then graphed against the price of BTC in that same interval. This can be used to spot aggression of spot or perp traders that can help indicate the strength of price action.
