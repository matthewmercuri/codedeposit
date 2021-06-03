import pandas as pd

df_all = pd.read_csv('NFL Stats/spreadspoke_scores.csv') #reading whole df into a df



#selecting relevant columns
df_betting = df_all[['schedule_season', 'team_home','team_away','team_favorite_id','spread_favorite','score_home','score_away']]
df_betting = df_betting[df_betting['schedule_season'] >= 2016] #limiting to seasons from 2016 onwards
df_betting.dropna(subset=['schedule_season', 'team_home','team_away','team_favorite_id','spread_favorite'], inplace=True)
df_betting['spread_favorite'] = df_betting['spread_favorite'].abs() #making all spreads positive (always for the fav anyways)

df_names = pd.read_csv('df_names.csv', header=None) #grabbing a new df with team codes from local file
df_names_dict = pd.Series(df_names[0].values, index=df_names[1]).to_dict() #creating dictionary with full and code names

df_betting.replace(to_replace=df_names_dict, inplace=True) #replacing full names with code names using dict

df = df_all[df_all['schedule_season'] >= 2000] #selecting for seasons starting in 2000
df = df[['schedule_season','schedule_date','team_home','team_away','score_home','score_away']]
df.dropna(subset=['score_home','score_away'], inplace=True)


winseq = [] #creating empty list
favseq = []
covseq = []

def _did_fav_cover(x, covseq=covseq):
	#This function takes the df and an empty list and inserts
	#a sequence of indicators depending on if the fav covered

	if x['team_favorite_id'] == 'PICK':
		covseq.append('PUSH')

	elif x['team_favorite_id'] == x['team_home']:
		if (x['score_home'] - x['score_away']) > x['spread_favorite']:
			covseq.append('covered')
		elif (x['score_home'] - x['score_away']) == x['spread_favorite']:
			covseq.append('PUSH')
		else:
			covseq.append('not_covered')

	elif x['team_favorite_id'] == x['team_away']:
		if (x['score_away'] - x['score_home']) > x['spread_favorite']:
			covseq.append('covered')
		elif (x['score_away'] - x['score_home']) == x['spread_favorite']:
			covseq.append('PUSH')
		else:
			covseq.append('not_covered')


def _favourite_wins_helper(x, favseq=favseq):
	#This function takes the df and an empty list and inserts
	#a sequence of indicators depending on if the fav won

	if x['team_favorite_id'] == x['team_home']:
		if x['score_home'] > x['score_away']:
			favseq.append('favew')
		else:
			favseq.append('favel')

	elif x['team_favorite_id'] == x['team_away']:
		if x['score_away'] > x['score_home']:
			favseq.append('favew')
		else:
			favseq.append('favel')

	elif x['team_favorite_id'] == 'PICK':
		favseq.append('WASH')

	else:
		print('Something went wrong figuring out if the favourite won!')
		print(x['team_favorite_id'])
		print(x['team_away'])
		print(x['team_home'])


def _whowon(x, winseq=winseq):
	#This function takes the df and an empty list and inserts
	#a sequence of indicators depending on if the home or away team won

	if x['score_home'] > x['score_away']:
		winseq.append('homew')

	elif x['score_away'] > x['score_home']:
		winseq.append('awayw')

	elif x['score_home'] == x['score_away']:
		winseq.append('tie')

	else:
		print("Something is wrong with our counting!")




def wintracker(gameresults=winseq,df=df):
	#This function takes our win sequence list once complete and counts the results
	df.apply(_whowon, axis=1)
	games = len(gameresults)
	home_wins = gameresults.count('homew')
	away_wins = gameresults.count('awayw')
	ties = gameresults.count('tie')

	return games, home_wins, away_wins, ties

def favourite_wins(favseq=favseq, df_betting=df_betting):
	#This function takes our favourite sequence list once complete and counts the results
	df_betting.apply(_favourite_wins_helper, axis=1)
	gamestracked = len(favseq)
	favwins = favseq.count('favew')
	favlosses = favseq.count('favel')
	favwinper = favwins / gamestracked

	return gamestracked, favwins, favlosses, favwinper

def favourite_covers(covseq=covseq, df_betting=df_betting):
	#This function takes our cover sequence list once complete and counts the results
	df_betting.apply(_did_fav_cover, axis=1)
	gameswithspread = len(covseq)
	favcovers = covseq.count('covered')
	nocovers = covseq.count('not_covered')
	pushes = covseq.count('PUSH')

	return gameswithspread, favcovers, nocovers, pushes



def create_mod_df(covseq=covseq, favseq=favseq, winseq=winseq, df_betting=df_betting, create_csv=False):
	#This function takes all the data we created in our lists and assigns them to columns in the df

	gameswithspread, favcovers, nocovers, pushes = favourite_covers()
	gamestracked, favwins, favlosses, favwinper = favourite_wins()
	games, home_wins, away_wins, ties = wintracker()

	df_betting['Favourite_Win'] = favseq
	df_betting['Favourtie_Cover'] = covseq
	df_betting['H_or_W_Win'] = winseq

	#If true we create a local copy of the df as a csv
	if create_csv == True:
		df_betting.to_csv('NFL_CompleteGameStats.csv')

	return df_betting


def print_favourite_stats():

	gameswithspread, favcovers, nocovers, pushes = favourite_covers()
	gamestracked, favwins, favlosses, favwinper = favourite_wins()

	print("There was a total of", gamestracked, "games tracked!")
	print(favwins, 'favourites have won.')
	print(favcovers, 'favourites of the', favwins, 'favourites who won, also covered.')
	print(favlosses, 'favourites have lost.')
	print('Vegas has been correct', round((favwinper * 100), 2), 'percent of the time!')
	print('Looking at', gameswithspread, 'games:')
	print('The favourite has covered', round(((favcovers / gameswithspread) * 100), 2), 'percent of the time!')

def print_matchup_stats():
	#gathers complete stats and prints to console
	games, home_wins, away_wins, ties = wintracker() 

	homewper = home_wins / games
	print(df.shape)
	print(games)
	print(home_wins)
	print(away_wins)
	print(ties)
	print(homewper)

#df_betting.to_excel('testing.xlsx')

print_matchup_stats()
print_favourite_stats()
#create_mod_df(create_csv=True)

