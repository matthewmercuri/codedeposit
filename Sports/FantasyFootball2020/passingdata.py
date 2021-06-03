import pandas as pd

PASS_STATS_FILE = 'data/2019passing.csv'
RUSH_STATS_FILE = 'data/2019rushing.csv'

MIN_GAMES = 8
MIN_PASS_ATT = 100

FANTASY_COLS_QB = ['Position', 'Games', 'Passing Yards',
                   'Passing TD', 'Rushing TD', 'Interceptions',
                   'Rushing Yards', 'P/G', 'Total Points']

PASSING_PER_YARD = 1 / 25
PASSING_TD = 4
INTERCEPTION = -2
RUSH_PER_YARD = 1 / 10
RUSHING_TD = 6
RECEPTIONS = 1
RECEIVING_PER_YARD = 1 / 10
RECEIVING_TD = 6
KICKOFF_PUNT_TD = 6
FUM_FOR_TD = 6
FUM_LOST = -2
TWO_CONVERT = 2


def clean_pass_data(player_stats_file=PASS_STATS_FILE):
    pass_df = pd.read_csv(player_stats_file, index_col='Rk')
    pass_df['Player'] = pass_df['Player'].apply(lambda x: x.split("\\", 1)[0])
    pass_df['Player'] = pass_df['Player'].apply(lambda x: x.split("*", 1)[0])
    pass_df = pass_df[pass_df['G'] >= MIN_GAMES]
    pass_df = pass_df[pass_df['Att'] >= MIN_PASS_ATT]

    pass_df = pass_df.set_index('Player')

    return pass_df


def clean_rush_data(player_stats_file=RUSH_STATS_FILE):
    rush_df = pd.read_csv(player_stats_file, index_col='Rk')
    rush_df['Player'] = rush_df['Player'].apply(lambda x: x.split("\\", 1)[0])
    rush_df['Player'] = rush_df['Player'].apply(lambda x: x.split("*", 1)[0])

    rush_df = rush_df.set_index('Player')

    return rush_df


def build_fantasy_sheet(save_csv=False):
    pass_df = clean_pass_data()
    rush_df = clean_rush_data()
    PLAYERS = pass_df.index
    qb_df = pd.DataFrame(columns=FANTASY_COLS_QB, index=PLAYERS)

    for player in PLAYERS:
        position = pass_df['Pos'].loc[player]
        games = pass_df['G'].loc[player]
        passing_yards = pass_df['Yds'].loc[player] * PASSING_PER_YARD
        passing_td = pass_df['TD'].loc[player] * PASSING_TD
        interceptions = pass_df['Int'].loc[player] * INTERCEPTION

        if player in rush_df.index:
            rushing_td = rush_df['TD'].loc[player] * RUSHING_TD
            rushing_yards = rush_df['Yds'].loc[player] * RUSH_PER_YARD
        else:
            rushing_td = 0
            rushing_yards = 0

        total_points = sum([passing_yards, passing_td, rushing_td,
                            interceptions, rushing_yards])
        points_per_game = total_points / games

        points_dict = ({'Position': position, 'Games': games,
                        'Passing Yards': passing_yards,
                        'Passing TD': passing_td, 'Rushing TD': rushing_td,
                        'Interceptions': interceptions,
                        'Rushing Yards': rushing_yards,
                        'P/G': points_per_game,
                        'Total Points': total_points})

        qb_df.loc[player] = pd.Series(points_dict)
        qb_df = qb_df.sort_values('P/G', ascending=False)
        qb_df['Position'] = qb_df['Position'].str.upper()

    if save_csv is True:
        qb_df.to_csv('2019passpoints.csv')
    else:
        print(qb_df)


build_fantasy_sheet()
