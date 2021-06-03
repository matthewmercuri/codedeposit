import pandas as pd

COLS_TO_DROP = ['CALL', 'PUT', 'TOTAL']


# Reading and cleaning datasets
pcr_df = pd.read_csv('Data/totalequitypcratio.csv', skiprows=2, index_col=0)
pcr_df.index = pd.to_datetime(pcr_df.index)

ff5_df = pd.read_csv('Data/North_America_5_Factors_Daily.csv', skiprows=3, index_col=0)
ff5_df.index = pd.to_datetime(ff5_df.index, format='%Y%m%d')


# Calculating PCR and rolling 20 SMA of PCR
pcr_df['PCR'] = pcr_df['PUT'] / pcr_df['CALL']
pcr_df.drop(columns=['P/C Ratio'], inplace=True)
pcr_df['PCR 20 Day SMA'] = pcr_df['PCR'].rolling(window=20).mean()
pcr_df.dropna(inplace=True)

# Joining factors
ff5_df = ff5_df[ff5_df.index <= '2019-10-04']
ff5_df = ff5_df[ff5_df.index >= '2006-11-29']

factor_df = pd.merge(ff5_df, pcr_df, left_index=True, right_index=True)
factor_df.drop(columns=COLS_TO_DROP, inplace=True)
correlations = factor_df.corr()
correlations.to_csv('Results/factor_corr.csv')
factor_df.to_csv('Results/allfactors.csv')

print(correlations)
print(ff5_df)
print(pcr_df)
print(factor_df)
