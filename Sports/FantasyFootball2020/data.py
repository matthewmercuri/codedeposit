# import numpy as np
import pandas as pd

PASS_STATS_FILE = 'data/2019passing.csv'

MIN_GAMES = 8
MIN_PASS_ATT = 100

FANTASY_COLS_QB = ['Position', 'Passing Yards', 'Passing TD', 'Interceptions',
                   'Rushing Yards', 'Total Points']

PASSING_PER_YARD = 1 / 25
PASSING_TD = 4
INTERCEPTION = -2
RUSH_PER_YARD = 1 / 10
RECEPTIONS = 1
RECEIVING_PER_YARD = 1 / 10
RECEIVING_TD = 6
KICKOFF_PUNT_TD = 6
FUM_FOR_TD = 6
FUM_LOST = -2
TWO_CONVERT = 2


def readclean(player_stats_file, position):
    pass_df = pd.read_csv(player_stats_file, index_col='Rk')
    pass_df['Player'] = pass_df['Player'].apply(lambda x: x.split("\\", 1)[0])
    pass_df['Player'] = pass_df['Player'].apply(lambda x: x.split("*", 1)[0])
    pass_df = pass_df[pass_df['G'] >= MIN_GAMES]

    if position == "qb":
        pass_df = pass_df[pass_df['Att'] >= MIN_PASS_ATT]

    print(pass_df)
    return pass_df


def offense_point_calc(cleaned_stats_file, position):
    if position == "qb":
        pass

def build_qb_fantasy_points():
    pass

readclean(PASS_STATS_FILE, "qb")
