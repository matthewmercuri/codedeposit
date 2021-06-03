from dotenv import load_dotenv
import io
import json
import os
import pandas as pd
import requests
import zipfile

load_dotenv()

HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': os.getenv("TNGO_API_KEY")
        }
requestResponse = requests.get("https://api.tiingo.com/api/test/",
                               headers=HEADERS)

BASE_URL = 'https://api.tiingo.com/'
SUPP_SYMBOLS = 'https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip'


class Tiingo:
    def __init__(self):
        self.valid_symbols()

    def _req(self, req_str):
        r = requests.get(BASE_URL + req_str, headers=HEADERS)
        return r.json()

    def valid_symbols(self):
        request = requests.get(SUPP_SYMBOLS)
        _file = zipfile.ZipFile(io.BytesIO(request.content))
        tickers = _file.open('supported_tickers.csv')
        df = pd.read_csv(tickers, index_col='ticker')
        self.tickers = df.index.tolist()
        self.asset_types = list(set(df['assetType'].tolist()))
        return df

    def is_valid(self, symbol):
        if symbol in self.tickers:
            return True
        else:
            return False

    def symbol_meta(self, symbol):
        req_str = f'tiingo/daily/{symbol}'
        response = self._req(req_str)
        return response

    def data_length(self, symbol):
        req_str = f'tiingo/daily/{symbol}'
        response = self._req(req_str)
        start = response['startDate']
        end = response['endDate']
        return start, end

    def hist_data(self, symbol, full=True, start_date=None,
                  end_date=None, save_locally=False):
        if full is True:
            start, end = self.data_length(symbol)
        else:
            start = start_date
            end = end_date

        req_str = f'tiingo/daily/{symbol}/prices?startDate={start}&endDate={end}'
        response = self._req(req_str)
        response = json.dumps(response)

        df = pd.read_json(response, orient='record')
        df.set_index('date', inplace=True)
        print(df)

        return df

    def snap_quote(self, symbol):
        req_str = f'iex/{symbol}'
        response = self._req(req_str)
        return response[0]['tngoLast']


# tiingo = Tiingo()
# print(tiingo.symbol_meta('AAPL'))
# tiingo.hist_data('AAPL')
# tiingo.valid_symbols()
# print(tiingo.snap_quote('AAPL'))
