import pandas as pd

player_names_file = open('field.txt', 'r')
player_names = player_names_file.readlines()
player_names = [x.strip() for x in player_names]

adj_df = pd.read_csv('adj_scores.csv')
adj_df.sort_values(by=adj_df.columns[0], inplace=True)
print(adj_df)

data_names = adj_df.columns.tolist()[1:]


# checking to see who we do not have data on
no_data = []
for p in player_names:
    if p not in data_names:
        no_data.append(p)
        player_names.remove(p)
print(no_data)

player_data = {}
for p in player_names:
    p_df = adj_df[p]
    p_df.dropna(inplace=True)
    p_df = p_df.tail(12)

    if len(p_df) <= 10:
        continue
    else:
        mean_score = p_df.mean()
        std = p_df.std()
        player_data[p] = {'m': mean_score, 's': std}


# print(player_names)
# print(data_names)
mc_df = pd.DataFrame.from_dict(player_data)
mc_df.to_csv('mcdata.csv')
print(mc_df)
