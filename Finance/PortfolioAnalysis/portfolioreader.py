import json
import pandas as pd


START_DATE = "2015-01-02"
END_DATE = "2020-03-20"

with open('Portfolio/holdings.json') as f:
    port_data = json.load(f)

holdings_df = pd.DataFrame(port_data['holdings'])
cash_df = pd.DataFrame(port_data['cash'], index=[0])

held_securities = holdings_df.columns.values.tolist()

ticker_df_list = []
for ticker in held_securities:
    temp_df = pd.read_csv(f'TickerData/{ticker}.csv', index_col=0)

    temp_df = temp_df[temp_df.index <= END_DATE]
    temp_df = temp_df[temp_df.index >= START_DATE]
    temp_df = temp_df['Close']

    ticker_df_list.append(temp_df)


ticker_df = pd.concat(ticker_df_list, axis=1, verify_integrity=True)
ticker_df.columns = held_securities


def find_corr_martix(ticker_df=ticker_df, days=250):
    ticker_df = ticker_df.tail(days)
    corr_matrix = ticker_df.corr()
    print(corr_matrix)


def find_cov_martix(ticker_df=ticker_df, days=250):
    ticker_df = ticker_df.tail(days)
    cov_matrix = ticker_df.cov()
    print(cov_matrix)


find_corr_martix(days=100)
find_cov_martix(days=50)
