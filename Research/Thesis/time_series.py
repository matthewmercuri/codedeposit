import pandas as pd


LAST_UPDATED = '05-12-2020'


def daily_returns(ticker: str, path: str = None):
    ticker = ticker.upper()

    if path is None:
        path = f'pricedata/{ticker}_{LAST_UPDATED}.csv'

    df = pd.read_csv(path, index_col=0)
    df.index = pd.to_datetime(df.index)
    df['Pct Return'] = df['Close'].pct_change()
    df.dropna(subset=['Pct Return'], inplace=True)

    return df


def index_returns(index: str, path: str = None):
    index = index.upper()
    valid_indexes = ['SP500']

    assert index in valid_indexes, f"{index} is not a valid index!"

    if path is None:
        path = f'indexdata/{index}.csv'

    df = pd.read_csv(path, index_col=0)
    df.index = pd.to_datetime(df.index)
    df['Pct Return'] = df['Adj Close'].pct_change()
    df.dropna(subset=['Pct Return'], inplace=True)

    return df


def factors(factor_type: int, path: str = None):
    valid_factors = [3, 5]
    assert factor_type in valid_factors, (f"{factor_type} is not a valid " +
                                          "factor type!")

    if factor_type == 5:
        df = pd.read_csv('ffdata/F-F_Research_Data_5_Factors_2x3_daily.CSV',
                         skiprows=2)
        df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], format='%Y%m%d')
        df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
        df.set_index('Date', inplace=True)

    elif factor_type == 3:
        df = pd.read_csv('ffdata/F-F_Research_Data_Factors_daily.CSV',
                         skiprows=3)
        df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], format='%Y%m%d')
        df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
        df.set_index('Date', inplace=True)
    else:
        df = None

    return df


def pcr():
    df = pd.read_csv('pcdata/equitypc.csv', skiprows=2)
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
    df.rename(columns={'DATE': 'Date'}, inplace=True)
    df.set_index('Date', inplace=True)

    return df
