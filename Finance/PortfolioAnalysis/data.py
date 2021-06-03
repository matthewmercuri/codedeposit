import os
import pandas as pd
import requests

'''
-Put helper functions and variables in class?
-donwload required data (benchmark and tradeables)
-load required data
-clean data
-save locally

'''


APIKEY = 'F3DH8T01FS30SCIB'
BASESTRING = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&"
COLRENAMEDICT = {'open': 'Open', 'high': 'High',
                 'low': 'Low', 'close': 'Close',
                 'adjusted_close': 'Adjusted Close', 'volume': 'Volume',
                 'dividend_amount': 'Dividend Amount',
                 'split_coefficient': 'Split Coefficient'}


def _complete_api_url(ticker):
    return BASESTRING + f'symbol={ticker}&apikey={APIKEY}&datatype=csv&outputsize=full'


class Data:
    def __init__(self):
        pass

    def _ticker_validation(self, symbol):
        if not isinstance(symbol, str):
            raise TypeError(f'{symbol} is not a string!')

    def _need_file(self, ticker):
        ''' Looks to see if the ticker already exists locally and how up to
        date it is. To do:
        - deletes if too old and returns true
        - deletes and returns true if testing
        '''
        if os.path.exists(f'TickerData/{ticker}.csv') is True:
            return False
        else:
            return True

    def _save_data(self, ticker):
        if self._need_file(ticker) is True:
            r = requests.get(_complete_api_url(ticker))
            open(f'TickerData/{ticker}.csv', 'wb').write(r.content)
            self._clean_data(ticker)
        else:
            print(f'Already have {ticker}. No need to download.')

    def _clean_data(self, ticker):
        df = pd.read_csv(f'TickerData/{ticker}.csv', index_col='timestamp')
        df.rename(columns=COLRENAMEDICT, inplace=True)
        df.rename_axis('Date', inplace=True)
        df = df.iloc[::-1]
        df.to_csv(f'TickerData/{ticker}.csv')

    def gather_data(self, tickers):
        print('Initializing data collection!')
        if isinstance(tickers, list):
            i = 0
            for ticker in tickers:
                self._ticker_validation(ticker)
                self._save_data(ticker)
                i += 1
                progress = (round((i / len(tickers)), 4))*100
                print(f'{progress}% complete ({ticker} downloaded!)')
        elif isinstance(tickers, str):
            self._ticker_validation(tickers)
            self._save_data(tickers)
        else:
            print('There was an error hanlding ticker(s).')


Data = Data()
Data.gather_data(['AAPL', 'AMD'])
