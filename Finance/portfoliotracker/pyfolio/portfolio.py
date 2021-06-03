import data


class Portfolio:

    def __init__(self, usd_cash: int = 0, cad_cash: int = 0):
        self.portfolio = {}
        self.portfolio['Cash'] = {'USD': usd_cash, 'CAD': cad_cash}
        self.portfolio['Positions'] = {}

    def add_position(self, ticker: str, quantity: int):
        ticker_price = data.price(ticker)
        self.portfolio['Positions'][ticker] = {'Value': ticker_price*quantity,
                                               'Shares': quantity,
                                               'Price': ticker_price}

    def clear_position(self, ticker: str):
        pass
