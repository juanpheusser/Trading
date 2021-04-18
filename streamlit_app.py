import streamlit as st
import pandas as pd
import requests
from Stock_Engine import Engine
import mplfinance as mpf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class DataGui:
    def __init__(self, tickers):
        st.title('InnerCore Trading Application')
        option = self.sidebar()
        self.setup_engine(tickers)
        self.compute_all_stock_RSI(tickers)

        self.engine.request_intraday_data()
        self.engine.request_eod_data()
        if option == 'RSI':
            self.RSI_Dashboard()
        elif option == 'AI Detector':
            self.AI_detector_Dashboard()
        elif option == 'Stock Tweets':
            self.Stock_Twits_Dashboard()

    def compute_all_stock_RSI(self, tickers):
        pass

    def setup_engine(self, tickers):
        self.engine = Engine()
        self.engine.add_list_stocks(tickers)

    def run_data_request(self):
        self.engine.request_intraday_data()

    def sidebar(self):
        st.sidebar.title('Dashboards')
        option = st.sidebar.selectbox('Select Dashboard', ('RSI', 'AI Detector', 'Stock Tweets'))
        return option

    def RSI_Dashboard(self):
        def plot_candle_line_volume(dataframe, ticker):
            line_trace = go.Scatter(x=dataframe.index, y=dataframe[price],
                                    name=' '.join([price.capitalize(), 'Price Line']))
            candle_trace = go.Candlestick(x=dataframe.index,
                                          open=dataframe['open'],
                                          high=dataframe['high'],
                                          low=dataframe['low'],
                                          close=dataframe['close'],
                                          name='OHLC Prices')
            fig = make_subplots(specs=[[{'secondary_y': True}]])
            volume_trace = go.Bar(x=dataframe.index, y=dataframe.volume, name='Volume', opacity=0.15, marker_color='#00CC96')
            fig.add_trace(line_trace, secondary_y=True)
            fig.add_trace(candle_trace, secondary_y=True)
            fig.add_trace(volume_trace, secondary_y=False)
            fig.update_layout(title=price.capitalize() + ' Price Line Plot: ' + ticker,
                              xaxis_title='Date - Time',
                              yaxis_title= price.capitalize() + ' Price USD',
                              yaxis=dict(side='left'),
                              yaxis2=dict(side='right',
                                          title_text='Volume'))
            fig['layout'].update(height=600, width=1000)


            st.write(fig)

        def plot_RSI(ticker, method, data_type, RSI_Length):

            if data_type == 'Intraday':
                price_data = self.engine.dict_of_stocks[ticker].stock_data_dataframe_intraday['last']
                delta = price_data.diff()
                dUp = delta.clip(lower=0)
                dDown = -1*delta.clip(upper=0)

                if method == 'linear':
                    rolUp = pd.rolling_mean(dUp, RSI_Length)
                    rolDown = pd.rolling_mean(dDown, RSI_Length)

                elif method == 'exponential':
                    rolUp = dUp.ewm(com=RSI_Length, adjust=False).mean()
                    rolDown = dDown.ewm(com=RSI_Length, adjust=False).mean()

                RS = rolUp/rolDown
                RSI = 100 - (100/ (1 + RS))
                RSI = pd.DataFrame(RSI.dropna())

                return go.Scatter(x=RSI.index, y=RSI['last'], name=ticker)

            elif data_type == 'End of Day':
                price_data = self.engine.dict_of_stocks[ticker].stock_data_dataframe_eod['close']
                delta = price_data.diff()
                dUp = delta.clip(lower=0)
                dDown = -1*delta.clip(upper=0)

                if method == 'Linear':
                    rolUp = pd.rolling_mean(dUp, RSI_Length)
                    rolDown = pd.rolling_mean(dDown, RSI_Length)

                else:
                    rolUp = dUp.ewm(com=RSI_Length, adjust=False).mean()
                    rolDown = dDown.ewm(com=RSI_Length, adjust=False).mean()

                RS = rolUp / rolDown
                RSI = 100 - (100 / (1 + RS))
                RSI = pd.DataFrame(RSI.dropna())

                return go.Scatter(x=RSI.index, y=RSI['close'], name=ticker)



        st.header('RSI Dashboard')
        st.subheader('Dashboard presenting RSI index for stocks')
        ticker1 = st.sidebar.selectbox('Select Stock Nº1 Ticker', tuple(self.engine.dict_of_stocks.keys()))
        RSI_plot1 = st.sidebar.checkbox(''.join(['Plot RSI of ', ticker1]), value=True, key='1')
        ticker2 = st.sidebar.selectbox('Select Stock Nº2 Ticker', tuple(self.engine.dict_of_stocks.keys()))
        RSI_plot2 = st.sidebar.checkbox(''.join(['Plot RSI of ', ticker2]), value=True, key='2')
        ticker3 = st.sidebar.selectbox('Select Stock Nº3 Ticker', tuple(self.engine.dict_of_stocks.keys()))
        RSI_plot3 = st.sidebar.checkbox(''.join(['Plot RSI of ', ticker3]), value=True, key='3')
        data_type = st.sidebar.selectbox('Select Type of Data', ('Intraday', 'End of Day'))
        if data_type == 'Intraday':
            price = st.sidebar.selectbox('Select Price to View', ('open', 'high', 'low', 'close', 'last'))
        else:
            price = st.sidebar.selectbox('Select Price to View', ('open', 'high', 'low', 'close'))
        RSI_Length = st.sidebar.number_input('Input RSI Sample Periods', min_value=5, max_value=99, value=9)
        RSI_Method = st.sidebar.selectbox('Select RSI Method', ('Linear', 'Exponential'))
        RSI_Method = RSI_Method.lower()

        if data_type == 'Intraday':
            dataframe1 = self.engine.dict_of_stocks[ticker1].stock_data_dataframe_intraday
            plot_candle_line_volume(dataframe1, ticker1)

            dataframe2 = self.engine.dict_of_stocks[ticker2].stock_data_dataframe_intraday
            plot_candle_line_volume(dataframe2, ticker2)

            dataframe3 = self.engine.dict_of_stocks[ticker3].stock_data_dataframe_intraday
            plot_candle_line_volume(dataframe3, ticker3)

        else:
            dataframe1 = self.engine.dict_of_stocks[ticker1].stock_data_dataframe_eod
            plot_candle_line_volume(dataframe1, ticker1)

            dataframe2 = self.engine.dict_of_stocks[ticker2].stock_data_dataframe_eod
            plot_candle_line_volume(dataframe2, ticker2)

            dataframe3 = self.engine.dict_of_stocks[ticker3].stock_data_dataframe_eod
            plot_candle_line_volume(dataframe3, ticker3)


        fig = make_subplots()
        if RSI_plot1:
            trace1 = plot_RSI(ticker1, RSI_Method, data_type,RSI_Length)
            fig.add_trace(trace1)

        if RSI_plot2:
            trace2 = plot_RSI(ticker2, RSI_Method, data_type, RSI_Length)
            fig.add_trace(trace2)

        if RSI_plot3:
            trace3 = plot_RSI(ticker3, RSI_Method, data_type, RSI_Length)
            fig.add_trace(trace3)

        fig.update_layout(title= ''.join(['RSI Line Plot']),
                          xaxis_title='Date - Time',
                          yaxis_title='RSI',
                          yaxis=dict(side='left'),
)
        fig['layout'].update(height=600, width=900)
        st.write(fig)

        st.write('Data Table: ' + ticker1)
        st.write(dataframe1)


    def AI_detector_Dashboard(self):
        st.header('AI Detector Dashboard')
        st.subheader('AI for detecting stock market anomallies')

    def Stock_Twits_Dashboard(self):
        st.header('Twitter Stock Dashboard')
        st.subheader('Displays Stock Twitter Data')

        ticker = st.sidebar.selectbox('Select Stock Ticker', tuple(self.engine.dict_of_stocks.keys()))

        r = requests.get("https://api.stocktwits.com/api/2/streams/symbol/" + ticker + ".json")
        data = r.json()

        for message in data['messages']:

            st.write(message['body'])
            st.write(message['created_at'])
            st.write(message['user']['username'])
            st.image(message['user']['avatar_url'])


if __name__=='__main__':
    gui = DataGui(['AAPL', 'AMC'])


