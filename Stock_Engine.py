import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from Stock import Stock
import requests

class Engine:

    def __init__(self):
        self.dict_of_stocks = {}
        self.request_frequency = 1
        self.request_datetime = None

    def add_stock(self, ticker):

        self.dict_of_stocks[ticker] = Stock(ticker)

    def add_list_stocks(self, lot):

        for ticker in lot:
            self.add_stock(ticker)

    def request_intraday_loop(self):
        while True:
            self.request_intraday_data()

    def request_intraday_data(self):
        if self.request_datetime:
            pass
        else:
            self.request_datetime = datetime.now()

        params = {
            'access_key': 'e55c6599b2fddba05caaec9976eeb003',
            'symbols': ','.join(self.dict_of_stocks.keys()),
            'interval': str(self.request_frequency) + 'min'
        }

        if self.request_datetime <= datetime.now():
            api_result = requests.get('https://api.marketstack.com/v1/intraday', params)
            api_response = dict(api_result.json())

            ticker_data = api_response['data']

            for data in ticker_data:
                if data['symbol'] in self.dict_of_stocks:
                    self.dict_of_stocks[data['symbol']].append_intraday_data(data)

                else:
                    self.dict_of_stocks[data['symbol']] = Stock(data['symbol'])
                    self.dict_of_stocks[data['symbol']].append_intraday_data(data)

            self.request_datetime += timedelta(minutes=self.request_frequency)

    def request_eod_data(self):

        params = {
            'access_key': 'e55c6599b2fddba05caaec9976eeb003',
            'symbols': ','.join(self.dict_of_stocks.keys()),
        }

        api_result = requests.get('https://api.marketstack.com/v1/eod', params)
        api_response = dict(api_result.json())
        ticker_data = api_response['data']

        for data in ticker_data:
            if data['symbol'] in self.dict_of_stocks:
                self.dict_of_stocks[data['symbol']].append_eod_data(data)

            else:
                self.dict_of_stocks[data['symbol']] = Stock(data['symbol'])
                self.dict_of_stocks[data['symbol']].append_eod_data(data)






