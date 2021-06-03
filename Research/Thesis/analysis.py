import pandas as pd


def test(x):
    pval_pcr = x['pval_P/C Ratio']
    if pval_pcr < 0.05:
        return 1
    else:
        return 0


def get_info(x):
    # Get basic info about tickers that PCR is sig for, so as to find patterns
    pass


def stat_sig_pcr():
    df = pd.read_csv('results/sp500_ff5_pcr_results.csv', index_col=0)
    df.dropna(inplace=True)

    df['PCR StatSig'] = df.apply(test, axis=1)

    good_df = df[df['PCR StatSig'] == 1]

    return good_df
