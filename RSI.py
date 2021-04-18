import requests
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class RSI:

    def __init__(self, tickers: list, frequency: int, sample_periods: int):

        '''
        :param tickers: list of tickers to analyze
        :param frequency: request frequency
        :param sample_periods: how many periods to use for RSI calculation
        '''

        self.sample_periods = sample_periods
        self.frequency = frequency
        self.tickers = tickers
        self.ticker_latest_price_dict = {tick: [] for tick in tickers}
        self.request_datetime = None
        self.RSI_dict = {tick: [] for tick in tickers}

    def request_api_data(self):

        self.request_datetime = datetime.now()

        params = {
            'access_key': 'e55c6599b2fddba05caaec9976eeb003',
            'symbols': ','.join(self.tickers),
            'interval': str(self.frequency) + 'min'
        }

        while True:
            if self.request_datetime <= datetime.now():
                api_result = requests.get('https://api.marketstack.com/v1/intraday/latest', params)
                # api_result = requests.get('https://api.marketstack.com/v1/exchanges/XTKS/intraday/latest', params)
                api_response = dict(api_result.json())

                ticker_data = api_response['data']

                for data in ticker_data:
                    if data['symbol'] in self.ticker_latest_price_dict:
                        self.ticker_latest_price_dict[
                            data['symbol']].append((self.request_datetime, data['last']))

                self.compute_RSI()
                self.plot_prices_and_RSI()
                self.request_datetime += timedelta(minutes=self.frequency)
                print('Data Request Done')
                print(self.ticker_latest_price_dict)
                print(self.RSI_dict)

    def compute_RSI(self):

        def compute_single_RSI(vector_of_prices):

            shifted_vector_of_prices = np.append(0, vector_of_prices[:-1])
            diff = vector_of_prices - shifted_vector_of_prices
            diff = diff[1:]
            ups = diff[diff > 0]
            downs = diff[diff < 0]
            RS = np.mean(ups) / np.abs(np.mean(downs))
            RSI = 100.0 - (100.0 / (1 + RS))

            return RSI

        if len(self.ticker_latest_price_dict[self.tickers[0]]) >= self.sample_periods:

            for ticker, time_price_tuple in self.ticker_latest_price_dict.items():
                vector_of_prices = np.array(list(map(lambda x: x[1], time_price_tuple)))
                RSI = compute_single_RSI(vector_of_prices[-self.sample_periods:])
                self.RSI_dict[ticker].append((self.request_datetime, RSI))

    def plot_prices_and_RSI(self):

        fig, ax = plt.subplots(2)
        fig.suptitle('Stocks Prices and RSI')

        price_lines = []
        RSI_lines = []

        try:
            for ticker, time_price_tuple in self.ticker_latest_price_dict.items():
                dates = list(map(lambda x: x[0], time_price_tuple))
                prices = list(map(lambda x: x[1], time_price_tuple))
                line, = ax[0].plot(dates, prices, label=ticker)
                price_lines.append(line)
        except Exception as e:
            print(e)

        try:
            for ticker, time_RSI_tuple in self.RSI_dict.items():
                dates = list(map(lambda x: x[0], time_RSI_tuple))
                RSI = list(map(lambda x: x[1], time_RSI_tuple))
                line, = ax[1].plot(dates, RSI, label=ticker)
                RSI_lines.append(line)
        except Exception as e:
            print(e)

        ax[0].set_title('Stock Prices')
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Price [USD]')
        ax[0].grid()

        ax[1].set_title('Stock RSI')
        ax[1].set_xlabel('Time')
        ax[1].set_ylabel('RSI')
        ax[1].grid()

        plt.legend(price_lines, self.tickers, loc=7)
        plt.show()

    def data_as_df(self):

        price_index = [val[0] for val in self.ticker_latest_price_dict[self.tickers[0]].values()]
        rsi_index = [val[0] for val in self.RSI_dict[self.tickers[0]].values()]
        prices_dict = {ticker: val[1] for ticker, val in self.ticker_latest_price_dict.items()}
        rsi_dict = {ticker: val[1] for ticker, val in self.RSI_dict.items()}
        prices_df = pd.DataFrame(data=prices_dict, index=price_index)
        rsi_df = pd.DataFrame(data=rsi_dict, index=rsi_index)

        return prices_df, rsi_df

if __name__ == '__main__':
    rsi = RSI(tickers=['BCS', 'AMC'],
              frequency=1,
              sample_periods=14)

    rsi.request_api_data()
