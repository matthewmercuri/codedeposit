# import pandas as pd
from .yfin import YFin


class Data:
    def __init__(self, data_source="yfinance"):
        self.data_source = data_source
        self.YFin = YFin()

    def adj_close_series(self, symbol, start=None, end=None):
        symbol = symbol.upper()
        if self.data_source == "yfinance":
            data = self.YFin.adj_close_series(symbol, start, end)

        return data
