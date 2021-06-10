import numpy as np
import pandas as pd

df = pd.read_csv('data2.csv', low_memory=False)
# print(df.columns)

tournaments = list(set(df['tournament name'].to_list()))
tourney_id = list(set(df['tournament id'].to_list()))

avg_player_scores = {}
avg_tourny_scores = {}
i = 0

for tourn in tourney_id:
    i += 1

    tourn_df = df[df['tournament id'] == tourn]
    players_tourney = tourn_df['player'].to_list()

    player_dict = {}
    score_dict = []

    for player in players_tourney:
        player_df = tourn_df[tourn_df['player'] == player]
        total_strokes = player_df['strokes'].sum()

        avg_player_score = total_strokes / (len(player_df) / 18)
        player_dict[player] = avg_player_score
        score_dict.append(avg_player_score)

    avg_player_scores[tourn] = player_dict
    avg_tourny_scores[tourn] = np.mean(score_dict)

    print(f'Completed {round((i/len(tourney_id))*100, 2)}%')

tourney_scores_df = pd.DataFrame.from_dict(avg_tourny_scores, orient='index')
tourney_scores_df.to_csv('tourney_avg_score.csv')

player_scores_df = pd.DataFrame.from_dict(avg_player_scores, orient='index')
player_scores_df.to_csv('player_scores.csv')
