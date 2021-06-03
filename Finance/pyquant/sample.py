import pyquant as pq

Data = pq.Data(data_source="yfinance")
df = Data.adj_close_series('AAPL')
print(df)
df['Log Returns'] = pq.risk.log_returns(df['Adjusted Close'])
print(df)
