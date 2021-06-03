import meta_data
import time_series
import pandas as pd
import statsmodels.api as sm
from typing import Union


SP500_SYMS = meta_data.get_sp500_tickers()
DAYS = 5 * 252


def _combine_data(price_data, factor_data, pcr_data):
    df = pd.concat([factor_data, price_data['Pct Return'],
                   pcr_data['P/C Ratio']], axis=1)
    df['R-Rf'] = df['Pct Return']*100 - df['RF']
    df.drop(columns=['RF', 'Pct Return'], inplace=True)
    df.dropna(subset=['Mkt-RF'], inplace=True)
    df.dropna(subset=['P/C Ratio'], inplace=True)
    df.drop(df.head(len(df)-DAYS).index, inplace=True)

    df['CONST'] = 1

    return df


def _mlr(factor_type, method, next_day, ticker, print_summary):
    price_data = time_series.daily_returns(ticker)
    factor_data = time_series.factors(factor_type)
    pcr_data = time_series.pcr()

    train_df = _combine_data(price_data, factor_data, pcr_data)

    if next_day is True:
        train_df['R-Rf'] = train_df['R-Rf'].shift(-1)
        train_df.drop(train_df.tail(1).index, inplace=True)

    train_cols = train_df.columns.values.tolist()
    train_cols.remove('R-Rf')
    label = train_df['R-Rf']

    X = train_df[train_cols]
    y = label

    model = sm.OLS(y, X)

    if method == 'RIDGE':
        results = model.fit_regularized(L1_wt=0)
    else:
        results = model.fit()

    print(results.summary()) if print_summary is True else None

    pvals = results.pvalues
    params = results.params

    start_date = train_df.index[0]
    end_date = train_df.index[len(train_df)-1]
    data_points = len(train_df)

    data = {'ticker': ticker, 'params': params, 'pvals': pvals,
            'meta': [start_date, end_date, data_points]}

    return data


def _data_handler(data):
    ticker = data['ticker']

    meta = data['meta']

    coefs = data['params']
    coefs = coefs.to_frame().transpose()

    pvals = data['pvals']
    pvals = pvals.add_prefix('pval_')
    pvals = pvals.to_frame().transpose()

    data_df = pd.concat([coefs, pvals], axis=1)
    data_df.rename(index={0: ticker.upper()}, inplace=True)

    data_df['Start'] = meta[0]
    data_df['End'] = meta[1]
    data_df['DataPoints'] = meta[2]

    return data_df


def perform_mlr(tickers: Union[str, list], method: str = None,
                next_day: bool = False, factor_type: int = 5,
                print_summary: bool = False):

    if method is not None:
        method = method.upper()
        assert method in ['RIDGE'], f"{method} is not a valid method!"

    BAD = []
    results_df = None

    if type(tickers) is list:
        RESULTS = {}

        i = 0
        total = len(tickers)
        for ticker in tickers:
            try:
                data = _mlr(factor_type, method, next_day, ticker,
                            print_summary)
                RESULTS[ticker] = _data_handler(data)
            except Exception as e:
                print(f'Trouble with {ticker}!')
                print(e)
                tickers.remove(ticker)
                BAD.append(ticker)

            i += 1
            print(f'{round((i/total)*100, 2)}% complete!')

        result_tickers = [t for t in RESULTS]
        results_df = pd.concat([RESULTS[x] for x in result_tickers])

    else:
        try:
            data = _mlr(factor_type, method, next_day, tickers, print_summary)
            results_df = _data_handler(data)
        except Exception as e:
            print(f'Trouble with {tickers}!')
            print(e)
            BAD.append(tickers)

    return results_df, BAD


def start_sp500_analysis(factor_type: int = 5, method: str = None,
                         next_day: bool = False, save_locally: bool = True):
    sl = ''

    results_df, BAD = perform_mlr(tickers=SP500_SYMS, method=method,
                                  next_day=next_day)

    if next_day is True:
        sl = 'T1'

    if method == 'RIDGE':
        sl += 'R'

    if save_locally is True:
        results_df.to_csv(f'results/sp500_ff{factor_type}_pcr_{sl}results.csv')

    print(BAD)

    return results_df


# print(perform_mlr(['aapl', 'ma'], 3, True))
# print(perform_mlr('ma', True, 5, True)[0])
# start_sp500_analysis(method='ridge', next_day=False)
# start_sp500_analysis()
# start_sp500_analysis(next_day=True)
# perform_mlr('AAPL', print_summary=True)
# perform_mlr('AAPL', method='RIDGE', print_summary=True)
