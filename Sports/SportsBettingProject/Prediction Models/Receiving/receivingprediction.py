import pandas as pd

statfiles = ['ReceivingStats2014.csv','ReceivingStats2014.csv','ReceivingStats2014.csv','ReceivingStats2014.csv']

li = [] #empty list to fill with our stat dataframes

for file in statfiles:
	df = pd.read_csv(f'D://SportsBettingProject/NFL Stats/{file}', index_col=None, header=0) #reading stats to df
	li.append(df) #putting df into list

def targetspergame(x): #function to calculate targets per game
	return x['Tgt'] / x['G']

completed_df = pd.concat(li, axis=0, ignore_index=True) #connecting all the dfs
completed_df['Targets/Game'] = df.apply(targetspergame, axis=1) #creating a new function for targets per game

completed_df.drop(['Rk','Pos','Fmb', 'Player', 'Tm', 'Tgt', 'G', 'GS', 'Rec', 'Yds', 'TD', 'Lng', 'Y/R'], axis=1, inplace=True) #deleting unwanted columns
#completed_df.to_excel("Test.xlsx")

#print(completed_df.shape)
print(completed_df.head())


testdf = pd.read_csv('D://SportsBettingProject/NFL Stats/spreadspoke_scores.csv', index_col=None, header=0)
testdf.tail(1000).to_excel("whatthehell.xlsx")