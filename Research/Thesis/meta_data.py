import pandas as pd


LAST_SP500_UPDATE = '12-05-2020'


def get_sp500_tickers():
    df = pd.read_csv(f'metadata/sp-500-index-{LAST_SP500_UPDATE}.csv')
    df.drop(df.tail(1).index, inplace=True)

    return df['Symbol'].to_list()
