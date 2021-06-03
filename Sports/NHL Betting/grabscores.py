import pandas as pd
import requests

r = requests.get('https://www.hockey-reference.com/leagues/NHL_2020_games.html')

scores_df = pd.read_html(r.text)
scores_df = scores_df[0]

scores_df.to_csv('Data/scores_df.csv')

print('Downloaded updated scores!')
