import pandas as pd

raw_data = ['ReceivingStats2014','ReceivingStats2015','ReceivingStats2017','ReceivingStats2018']


#function inputs the filename and outputs a cleaned df
#data is obtained from pro-football-reference
def clean_raw_csv(filename):

	df = pd.read_csv(f'NFL Stats/{filename}.csv')
	df['Player'] = df['Player'].apply(lambda x: x.split('\\')[0]) #splits player name from \ and replaces it with first element
	df['Player'] = df['Player'].apply(lambda x: x.split('*')[0]) #splits player name from * and replaces it with first element
	print(df.head())
	df.to_csv(f'CleanWorkingData/{filename}Cleaned.csv', index=None)

	return df

for x in raw_data:
	clean_raw_csv(x)