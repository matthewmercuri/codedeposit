import os
from datetime import datetime, timedelta
import pandas as pd
from portfolio import Portfolio


class Backtest:

    def __init__(self, start_cash, tickers, benchmark, start_date, end_date):
        ''' We're going to have to eventually have instance variables
        that allow shortselling or options trading
        '''
        self.benchmark = benchmark
        self.tradeables = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.trade_date = start_date
        self.buy_stock_com = 5
        self.sell_stock_com = 5
        self.closed_pnl = 0
        self.Portfolio = Portfolio(start_cash)
        self._validate()

    def _validate(self):
        tradeables = self.tradeables
        tradeables.append(self.benchmark)

        for tradeable in tradeables:
            if os.path.exists(f'stockdata/{tradeable}.csv') is False:
                ''' Should go and get file if it does not already exist
                '''
                raise NameError(f'{tradeable} does not have a file!')

            df = pd.read_csv(f'stockdata/{tradeable}.csv', index_col='Date')
            if self.start_date not in df.index or self.end_date not in df.index:
                print(f'The start or end date is not available for {tradeable}.')

        print('All downloaded data has been validated!')

    def _check_day(self):
        ''' Going to have to fix this when it comes time to trade tickers
        that may or may not have been listed
        '''
        for tradeable in self.tradeables:
            df = pd.read_csv(f'stockdata/{tradeable}.csv', index_col='Date')
            if self.trade_date not in df.index:
                self.advance_day()
                print(f'{self.trade_date} is not in {tradeable} data. Advancing...')

    def _check_current_positions(self, symbol, quantity):
        ''' Checks current positions to see if it currently exists in the portolio
        '''
        df = self.Portfolio.stock_positions
        if df.index == symbol:
            return True
        else:
            return False

    def _check_valid_buy(self, price, quantity):
        ''' should be different in certain situaitons. E.g. allowing
        short-selling or options. Certain procedures must be excecuted
        regardless. Might be different if trading percentages instead
        of dollar amounts.
        '''
        total_price = quantity * price
        if total_price > self.Portfolio.cash:
            return False
        else:
            return True
        pass

    def set_commissions(self):
        pass

    def advance_day(self):
        self.trade_date = datetime.strptime(self.trade_date, '%Y-%m-%d') + timedelta(days=1)
        self.trade_date = str(self.trade_date.strftime('%Y-%m-%d'))
        self._check_day()

    def get_todays_df(self):
        ''' We need to construct a temporary df that combines all the stock
        data for any given day. We also need to add a symbol column. This could
        be made more efficient possibly. For some reason, we can't call this twice.
        THIS HAPPENED BECAUSE I USE THE SAME NAME FOR METHOD AND ATRIBUTE.
        '''
        stock_dfs_list = []

        for tradeable in self.tradeables:
            df = pd.read_csv(f'stockdata/{tradeable}.csv', index_col='Date')
            df['Symbol'] = tradeable
            df = df.loc[[self.trade_date]]
            stock_dfs_list.append(df)
        self._todays_df = pd.concat(stock_dfs_list, axis=0, sort=True)
        return self._todays_df

    def buy(self, symbol, quantity):
        '''  Need to work in commissions with cost basis. Have to be
        adding a 'Closed PnL' to each holding in stock_positions df
        '''
        stock_port_df = self.Portfolio.stock_positions

        _todays_df = self.get_todays_df()
        _todays_df = _todays_df[_todays_df['Symbol'] == symbol]
        price = _todays_df['Adjusted Close'].iloc[0]

        if self._check_valid_buy(price, quantity) is True:
            if self._check_current_positions(symbol, quantity) is True:
                stock_port_df = stock_port_df.loc[symbol]
                if stock_port_df['Quantity'] + quantity == 0:
                    df = self.Portfolio.stock_positions
                    df.drop(symbol, inplace=True)
                    self.Portfolio.stock_positions = df
                else:
                    stock_port_df['Quantity'] = stock_port_df['Quantity'] + quantity
                    stock_port_df['Cost Basis'] = (stock_port_df['Quantity'] * price) / stock_port_df['Quantity']
                    self.Portfolio.stock_positions.loc[symbol] = stock_port_df
            else:
                addition = {'Quantity': quantity, 'Cost Basis': price}
                stock_port_df.loc[symbol] = addition
                self.Portfolio.stock_positions = stock_port_df
        else:
            pass

    def sell(self, symbol, quantity):
        pass
