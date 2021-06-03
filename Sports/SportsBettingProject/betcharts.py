from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#There are 801 NFL games in three seasons, discluding preseason

df = pd.read_csv('NFL_CompleteGameStats.csv') #pulling df from local csv

spreads_list = df['spread_favorite'].tolist() #pulling spreads into a list
spreads_list = [-x for x in spreads_list] #making all spreads negative to show its for favorites

spreads_df = pd.DataFrame(list(set(spreads_list))) #making a df containing unique spreads
spreads_df.columns = ['Spreads'] #renaming the column

spreads_list_length = len(spreads_list) #creating a variable equal to the length of the spreads list

def _spread_counter(df, spreads_list=spreads_list):
	#Takes spread value and returns the frequency it occurs in our list of all spreads
	spread = df['Spreads']
	frequency = spreads_list.count(spread)

	return frequency

def _spread_frequency_perc(df, spreads_list_length=spreads_list_length):
	#Takes the spread frequency and returns the percent occurence 
	spread_frequency = df['Frequency']
	spread_frequency_percent = round(((spread_frequency/spreads_list_length)*100), 3)

	return spread_frequency_percent


spreads_df['Frequency'] = spreads_df.apply(_spread_counter, axis=1) #creaing a column for frequency
spreads_df['Freq_Perc'] = spreads_df.apply(_spread_frequency_perc, axis=1) #creaing a column for freq perc

#freq_per_list = spreads_df['Freq_Perc'].tolist()

plt.style.use('ggplot')

def show_line_hist():

	graph_title = 'NFL Spread Distribution: 2016-2018 (Three Seasons or 801 Games)'
	fig, ax = plt.subplots()
	fig.canvas.set_window_title(graph_title)
	plt.bar(spreads_df['Spreads'], spreads_df['Frequency'], ec='black', width=0.45, facecolor='b')
	plt.title(graph_title, fontsize=20)
	plt.xticks(spreads_df['Spreads'], rotation=90)
	plt.yticks(np.arange(0,140,5))
	plt.xlabel('Spread (for Favourite)', fontsize=20)
	plt.ylabel('Frequency (# of Occurences)', fontsize=20)

	for p in ax.patches:
		width, height = p.get_width(), p.get_height()
		x, y = p.get_xy()
		percentage = round((height / spreads_list_length)*100, 2)
		ax.annotate('{}%'.format(percentage), (x, y + height + 0.5), fontsize=8)

	plt.show()

show_line_hist()