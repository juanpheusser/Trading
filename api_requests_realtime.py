import requests
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import math

request_frequency_minutes = 1
sample_periods = 14
datetime_change = timedelta(minutes=request_frequency_minutes)

params = {
    'access_key': 'e55c6599b2fddba05caaec9976eeb003',
    'interval': str(request_frequency_minutes) + 'min'
}

last_trade_price = np.array([])

ups = np.array([])
downs = np.array([])

RSI_vect = np.array([])

request_datetime = datetime(year=2021,
                            month=4,
                            day=13,
                            hour=10,
                            minute=20,
                            second=0,
                            microsecond=0)

datetime_vect = []

while True:

    if request_datetime <= datetime.now():
        api_result = requests.get('https://api.marketstack.com/v1/tickers/aapl/intraday/latest', params)
        api_response = api_result.json()
        last_trade_price= np.append(last_trade_price, api_response['last'])
        datetime_vect.append(request_datetime)

        if sample_periods > last_trade_price.shape[0] >= 2:
            difference = last_trade_price[-1] - last_trade_price[-2]

            if difference > 0:
                ups = np.append(ups, difference)
            elif difference < 0:
                downs = np.append(downs, difference)

            try:
                RS = np.mean(ups)/np.abs(np.mean(downs))
                if math.isnan(RS):
                    RS = 0
            except:
                RS = 0

            RSI = 100.0 - 100.0 / (1 + RS)

            RSI_vect = np.append(RSI_vect, RSI)

        elif sample_periods <= last_trade_price.shape[0]:
            considered_prices = last_trade_price[-sample_periods:]
            shifted_trade_prices = np.append(considered_prices[1:], 0)
            diff_vec = considered_prices - shifted_trade_prices
            ups = list(filter(lambda x: x > 0, diff_vec))
            downs = list(filter(lambda x: x < 0, diff_vec))

            RS = np.mean(ups)/np.abs(np.mean(downs))
            RSI = 100.0 - (100.0 / (1 + RS))
            RSI_vect = np.append(RSI_vect, RSI)

        else:
            RS = None
            RSI = None

        print('Mean UPS: ', np.mean(ups), 'total: ', len(ups))
        print('Mean DOWNS: ', np.mean(downs), 'total', len(downs))

        print('RS: ', RS)
        print('RSI: ', RSI)


        fig, axis = plt.subplots(2)
        fig.suptitle('AAPL RSI')
        axis[0].plot(datetime_vect, last_trade_price)
        axis[1].plot(datetime_vect[1:], RSI_vect)
        plt.show()

        request_datetime += datetime_change









