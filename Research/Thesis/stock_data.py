from datetime import date
import pandas as pd
import yfinance as yf

today = date.today()
today = today.strftime("%d-%m-%Y")

df = pd.read_csv('metadata/sp-500-index-12-05-2020.csv')
df.drop(df.tail(1).index, inplace=True)
symbols_list = df['Symbol'].tolist()
print(symbols_list)

TOTAL_SYMBOLS = len(df)
i = 0
bad_symbol = []
for symbol in symbols_list:
    try:
        data = yf.Ticker(symbol)
        _df = data.history(period="max")
        _df.to_csv(f'pricedata/{symbol}_{today}.csv')
    except Exception as e:
        bad_symbol.append(symbol)
        print(e, symbol)

    i += 1
    _progress = round((i/TOTAL_SYMBOLS)*100, 2)
    print(f'{_progress}% complete')
