import requests
import numpy as np

params = {
    'access_key': 'e55c6599b2fddba05caaec9976eeb003'
}

api_result = requests.get('https://api.marketstack.com/v1/tickers/aapl/eod', params)

api_response = api_result.json()

print(api_response)



