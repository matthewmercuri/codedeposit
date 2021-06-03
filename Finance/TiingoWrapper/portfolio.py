import numpy as np
import pandas as pd


class Portfolio:
    def __init__(self, portfolio=None):
        if portfolio:
            self.positions = portfolio
        else:
            self.positions = {}

    def add_equity(self, symbol, quantity):
        self.positions[symbol] = {"shares": quantity,
                                  "currency": "USD-PLACEHOLDER"}

    def del_equity(self, symbol):
        pass

    def graph(self):
        pass


Port = Portfolio()
Port.add_equity("AAPL", 10)
print(Port.positions)