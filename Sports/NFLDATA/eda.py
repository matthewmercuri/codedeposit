# flake8: noqa

from data import *
import pandas as pd


# qb_df = pos_fantasy_standings('qb')
# qb_df = qb_df[qb_df['Games_GS'] >= 3]

# print(qb_df)
# print(qb_df.describe())

# wr_df = pos_fantasy_standings('wr')
# wr_df = wr_df[wr_df['Games_GS'] >= 3]

# print(wr_df)
# print(wr_df.describe())

# rb_df = pos_fantasy_standings('rb')
# rb_df = rb_df[rb_df['Games_GS'] >= 3]

# print(rb_df)
# print(rb_df.describe())

print(active_player_gamelog('Derrick Henry'))
