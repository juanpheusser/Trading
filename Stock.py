import numpy as np
import pandas as pd
from datetime import datetime, date


class Stock:

    def __init__(self, ticker):
        self.ticker = ticker
        self.stock_data_dataframe_intraday = pd.DataFrame(columns=['open',
                                                                   'high',
                                                                   'low',
                                                                   'last',
                                                                   'close',
                                                                   'volume',
                                                                   'exchange'])

        self.open_prices_intraday = []
        self.high_prices_intraday = []
        self.low_prices_intraday = []
        self.last_prices_intraday = []
        self.close_prices_intraday = []
        self.volume_intraday = []
        self.RSI_intraday = []


        self.stock_data_dataframe_eod = pd.DataFrame(columns=['open',
                                                              'high',
                                                              'low',
                                                              'close',
                                                              'volume',
                                                              'adj_high',
                                                              'adj_low',
                                                              'adj_close',
                                                              'adj_open',
                                                              'adj_volume',
                                                              'split_factor',
                                                              'exchange'])
        self.open_prices_eod = []
        self.high_prices_eod = []
        self.low_prices_eod = []
        self.close_prices_eod = []
        self.volume_eod = []
        self.adj_open_prices_eod = []
        self.adj_high_prices_eod = []
        self.adj_low_prices_eod = []
        self.adj_close_prices_eod = []
        self.adj_volume_eod = []
        self.split_factor_eod = []
        self.RSI_eod = []

    ## Append Methods

    def append_intraday_data(self, data):
        self.append_dataframe_intraday(data)
        self.append_open_intraday(data)
        self.append_high_intraday(data)
        self.append_close_intraday(data)
        self.append_low_intraday(data)
        self.append_last_intraday(data)
        self.append_volume_intraday(data)
        self.stock_data_dataframe_intraday.dropna()

    def append_eod_data(self, data):
        self.append_dataframe_eod(data)
        self.append_open_eod(data)
        self.append_high_eod(data)
        self.append_low_eod(data)
        self.append_close_eod(data)
        self.append_volume_eod(data)
        self.append_adj_open_eod(data)
        self.append_adj_high_eod(data)
        self.append_adj_low_eod(data)
        self.append_adj_close_eod(data)
        self.append_adj_volume_eod(data)
        self.append_split_eod(data)

    def append_dataframe_intraday(self, data):
        data_dict = {field: data[field] for field in self.stock_data_dataframe_intraday.columns}
        index = self.time_to_datetime(data['date'])
        self.stock_data_dataframe_intraday.loc[index] = data_dict

    def append_open_intraday(self, data):
        self.open_prices_intraday.append((self.time_to_datetime(data['date']),
                                          data['open']))

    def append_high_intraday(self, data):
        self.high_prices_intraday.append((self.time_to_datetime(data['date']),
                                          data['high']))
    def append_low_intraday(self, data):
        self.low_prices_intraday.append((self.time_to_datetime(data['date']),
                                          data['low']))

    def append_last_intraday(self, data):
        self.last_prices_intraday.append((self.time_to_datetime(data['date']),
                                          data['last']))

    def append_close_intraday(self, data):
        self.close_prices_intraday.append((self.time_to_datetime(data['date']),
                                          data['close']))

    def append_volume_intraday(self, data):
        self.volume_intraday.append((self.time_to_datetime(data['date']),
                                          data['volume']))

    def time_to_datetime(self, time):
        time_obj = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S+%f")
        # time_obj = time_obj.replace(year=date.today().year, month=date.today().month)
        return time_obj

    def append_dataframe_eod(self, data):
        data_dict = {field: data[field] for field in self.stock_data_dataframe_eod.columns}
        index = self.time_to_datetime(data['date'])
        self.stock_data_dataframe_eod.loc[index] = data_dict

    def append_open_eod(self, data):
        self.open_prices_eod.append((self.time_to_datetime(data['date']),
                                          data['open']))

    def append_high_eod(self, data):
        self.high_prices_eod.append((self.time_to_datetime(data['date']),
                                          data['high']))

    def append_low_eod(self, data):
        self.low_prices_eod.append((self.time_to_datetime(data['date']),
                                          data['low']))

    def append_close_eod(self, data):
        self.close_prices_eod.append((self.time_to_datetime(data['date']),
                                          data['close']))

    def append_volume_eod(self, data):
        self.volume_eod.append((self.time_to_datetime(data['date']),
                                          data['volume']))

    def append_adj_open_eod(self, data):
        self.adj_open_prices_eod.append((self.time_to_datetime(data['date']),
                                          data['adj_open']))

    def append_adj_high_eod(self, data):
        self.adj_high_prices_eod.append((self.time_to_datetime(data['date']),
                                          data['adj_high']))

    def append_adj_low_eod(self, data):
        self.adj_low_prices_eod.append((self.time_to_datetime(data['date']),
                                          data['adj_low']))

    def append_adj_close_eod(self, data):
        self.adj_close_prices_eod.append((self.time_to_datetime(data['date']),
                                          data['adj_close']))

    def append_adj_volume_eod(self, data):
        self.adj_volume_eod.append((self.time_to_datetime(data['date']),
                                          data['adj_volume']))

    def append_split_eod(self, data):
        self.split_factor_eod.append((self.time_to_datetime(data['date']),
                                          data['split_factor']))

    ## Index Methods

    def compute_RSI(self, length, method='linear', type='intraday'):

        if type == 'intraday':
            price_vect = self.stock_data_dataframe_intraday['last'].to_numpy()
            date = self.stock_data_dataframe_intraday.index[-1]
        elif type == 'eod':
            price_vect = self.stock_data_dataframe_eod['close'].to_numpy()
            date = self.stock_data_dataframe_eod.index[-1]

        if price_vect.shape[0] >= length:
            price_vect = price_vect[-length-1:]
            diff = price_vect - np.append(0, price_vect[:-1])
            diff = diff[1:]
            ups = diff[diff > 0]
            downs = np.abs(diff[diff < 0])

            if method == 'linear':
                ups_mean = np.sum(ups) / length
                downs_mean = np.sum(downs)/length

                if downs_mean == 0.0:
                    RSI = 100.0
                else:
                    RS = ups_mean/downs_mean
                    RSI = 100.0 - (100.0/(1 + RS))

            elif method == 'exponential':
                weights = np.exp(np.linspace(-1., 0., length))
                weights /= weights.sum()

                ups_mean = np.convolve(ups, weights)[:len(ups)]
                ups_mean[:length] = ups_mean[length]

                downs_mean = np.convolve(downs, weights)[:len(ups)]
                downs_mean[:length] = downs_mean[length]

            if type == 'intraday':
                pass










