import data
import pandas as pd
from scipy import stats

Data = data.Data()

df = Data.career_stats('Tom Brady')
pass_yards = df['Yds'].astype(float)
pass_yards = pass_yards.iloc[100:]

# print(pass_yards)

print(stats.kstest(pass_yards, 'norm', args=(pass_yards.mean(), pass_yards.std())))