import pandas as pd
import fix_yahoo_finance as yf 
from pandas_datareader import data as pdr

VALID__DATATYPES = ['close', 'high', 'low', 'open', 't', 'volume', 'adj close']
yf.pdr_override() 


class StockData():
    def __init__(self, stocks, start='2014-01-01', end='2019-01-01'):
        self.stocks = stocks
        self.start = pd.to_datetime(start)
        self.end = pd.to_datetime(end)
        self._data = self.fetch_data() 

    @property
    def log_returns(self):
        close_data = self.get('Adj Close') 
        return close_data / close_data.shift(1)

    def fetch_data(self):
        try:
            data = pdr.get_data_yahoo(self.stocks, self.start, self.end)
        except:
            raise Exception("Couldn't fetch the stock data.")
        return data

    def get(self, key):
        if key.lower() in VALID__DATATYPES:
            data = self._data[key.title()]
            data.columns = self.stocks
            return data
        else: 
            raise ValueError(f'Invalid data type. Please choose from one of {VALID__DATATYPES}')
    
