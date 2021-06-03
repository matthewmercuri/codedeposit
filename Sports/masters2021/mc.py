import numpy as np
import pandas as pd

df = pd.read_csv('mcdata.csv')

players = df.columns.tolist()[1:]

SIMULATIONS = 10000

scores = {}
for p in players:
    p_m = df[p].iloc[0]
    p_s = df[p].iloc[1]
    p_adj_scores = np.random.normal(p_m, p_s, SIMULATIONS)

    scores[p] = p_adj_scores

# sims
sim_df = pd.DataFrame.from_dict(scores, orient='index')
# print(sim_df)

# sim_df['test'] = sim_df.rank()
# print(sim_df)

# for sim in range(SIMULATIONS):
#     s_df = sim_df[sim]
#     s_df = s_df.sort_values()
#     s_df.reset_index(inplace=True)
#     # s_df['Player'] = s_df.index
#     print(s_df)
#     break

ranks_list = []
for s in range(SIMULATIONS):
    ranks = sim_df[s].rank()
    ranks.sort_values(inplace=True)
    ranks_list.append(ranks)

final_df = pd.concat(ranks_list, axis=1)
final_df['Avg_Rank'] = final_df.mean(axis=1)
final_df.sort_values(by='Avg_Rank', inplace=True)
print(final_df)

final_df.to_csv('FINAL.csv')
