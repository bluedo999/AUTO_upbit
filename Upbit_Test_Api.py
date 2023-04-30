# Import necessary libraries
import requests
import json

# Define API endpoint URLs
BASE_URL = 'https://api.upbit.com/v1'
MARKET_URL = BASE_URL + '/ticker?markets=KRW-BTC'
TRADE_URL = BASE_URL + '/orders'
ACCOUNT_URL = BASE_URL + '/accounts'

# Make HTTP requests to API endpoints
response = requests.get(MARKET_URL)

# Parse JSON response
data = json.loads(response.text)

# Print market data
print(data)