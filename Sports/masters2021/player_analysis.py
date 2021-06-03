import pandas as pd

player_df = pd.read_csv('player_scores.csv')
tourney_df = pd.read_csv('tourney_avg_score.csv')

tourney_id_list = tourney_df[tourney_df.columns[0]].to_list()

# print(player_df.head())
# print(tourney_df.head())

adjusted_player_scores = []

i = 0
for tourney in tourney_id_list:
    temp_player_df = player_df[player_df[player_df.columns[0]] == tourney]
    temp_player_df.set_index(player_df.columns[0], inplace=True)
    # print(temp_player_df)

    temp_tourney_df = tourney_df[tourney_df[tourney_df.columns[0]] == tourney]
    avg_tourney_score = temp_tourney_df.iloc[0][1]
    # print(avg_tourney_score)

    adjusted_df = temp_player_df.subtract(avg_tourney_score)
    adjusted_player_scores.append(adjusted_df)

    i += 1
    print(f'Completed {round((i/len(tourney_id_list))*100, 2)}%')


adj_df = pd.concat(adjusted_player_scores)
adj_df.to_csv('adj_scores.csv')

print(adj_df)
