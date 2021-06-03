import yfinance as yf


class YFin:
    def __init__(self):
        pass

    def adj_close_series(self, symbol, start, end):
        sym = yf.Ticker(symbol)
        data = sym.history(period='max', start=start, end=end)
        data = data['Close']
        data.rename('Adjusted Close', inplace=True)

        return data
