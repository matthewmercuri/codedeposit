from fantasyfootball import fantrankings as fr

Rankings = fr.Rankings()
# print(Rankings.full_fantasy_standings('QB'))
rankings, bad = Rankings.te_rankings()
rankings.to_csv('te_dec9.csv')
print(bad)
