import numpy as np
import pandas as pd
import statsmodels.api as sm

START_DATE = '2006-11-29'
END_DATE = '2019-10-04'

USED_FACTORS = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'PCR']


factors_df = pd.read_csv('Results/allfactors.csv', index_col=0)

vug_df = pd.read_csv('Data/VUG.csv', index_col=0)
vug_df['Daily P Return'] = (vug_df['Adjusted Close'].pct_change(periods=1))*100

vug_df = vug_df[vug_df.index <= END_DATE]
vug_df = vug_df[vug_df.index >= START_DATE]

# Regression analysis
factors = factors_df[USED_FACTORS]
factors['Constant'] = 1.0
returns = vug_df['Daily P Return']


model = sm.OLS(returns, factors)
results = model.fit()
print(results.summary())

print(factors)


print(factors_df)
print(vug_df)

