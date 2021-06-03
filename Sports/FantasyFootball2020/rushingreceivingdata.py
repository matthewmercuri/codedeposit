import pandas as pd

QBS_2019 = 'data/2019 Results/2019passpoints.csv'

RUSH_STATS_FILE = 'data/2019rushing.csv'
REC_STATS_FILE = 'data/2019receiving.csv'

MIN_GAMES = 8

FANTASY_COLS_RR = ['Position', 'Games', 'Rushing Yards',
                   'Rushing TD', 'Receptions', 'Receiving Yards',
                   'Receiving TD', 'P/G', 'Total Points']

RUSH_PER_YARD = 1 / 10
RUSHING_TD = 6
RECEPTIONS = 1
RECEIVING_PER_YARD = 1 / 10
RECEIVING_TD = 6


def check_if_qb(player):
    _df = pd.read_csv(QBS_2019)
    qbs = _df['Player'].tolist()
    if player in qbs:
        return True
    else:
        return False


def clean_rush_data(player_stats_file=RUSH_STATS_FILE):
    rush_df = pd.read_csv(player_stats_file, index_col='Rk')
    rush_df['Player'] = rush_df['Player'].apply(lambda x: x.split("\\", 1)[0])
    rush_df['Player'] = rush_df['Player'].apply(lambda x: x.split("*", 1)[0])
    rush_df = rush_df[rush_df['G'] >= MIN_GAMES]

    rush_df = rush_df.set_index('Player')

    return rush_df


def clean_rec_data(player_stats_file=REC_STATS_FILE):
    rec_df = pd.read_csv(player_stats_file, index_col='Rk')
    rec_df['Player'] = rec_df['Player'].apply(lambda x: x.split("\\", 1)[0])
    rec_df['Player'] = rec_df['Player'].apply(lambda x: x.split("*", 1)[0])
    rec_df = rec_df[rec_df['G'] >= MIN_GAMES]

    rec_df = rec_df.set_index('Player')

    return rec_df


def create_df():
    rush_df = clean_rush_data()
    rec_df = clean_rec_data()
    RUSH_PLAYERS = rush_df.index.tolist()
    REC_PLAYERS = rec_df.index.tolist()
    _PLAYERS = RUSH_PLAYERS + REC_PLAYERS
    _PLAYERS2 = list(set(_PLAYERS))
    PLAYERS = []
    for player in _PLAYERS2:
        isqb = check_if_qb(player)
        if isqb is False:
            PLAYERS.append(player)

    rr_df = pd.DataFrame(columns=FANTASY_COLS_RR, index=PLAYERS)
    return rr_df


def build_fantasy_sheet(save_csv=False):
    rush_df = clean_rush_data()
    rec_df = clean_rec_data()
    rr_df = create_df()
    PLAYERS = rr_df.index

    for player in PLAYERS:
        # Rushing
        if player in rush_df.index:
            position = rush_df['Pos'].loc[player]
            games = rush_df['G'].loc[player]
            rushing_yards = rush_df['Yds'].loc[player] * RUSH_PER_YARD
            rushing_td = rush_df['TD'].loc[player] * RUSHING_TD
        else:
            rushing_yards = 0
            rushing_td = 0

        # Receiving
        if player in rec_df.index:
            games = rec_df['G'].loc[player]
            receiving_yards = rec_df['Yds'].loc[player] * RECEIVING_PER_YARD
            receptions = rec_df['Rec'].loc[player] * RECEPTIONS
            receiving_td = rec_df['TD'].loc[player] * RECEIVING_TD

            if not position:
                position = rec_df['Pos'].loc[player]
        else:
            receiving_yards = 0
            receptions = 0
            receiving_td = 0

        total_points = sum([rushing_yards, rushing_td, receiving_yards,
                            receptions, receiving_td])
        points_per_game = total_points / games

        points_dict = ({'Position': position, 'Games': games,
                        'Rushing Yards': rushing_yards,
                        'Rushing TD': rushing_td,
                        'Receptions': receptions,
                        'Receiving Yards': receiving_yards,
                        'Receiving TD': receiving_td,
                        'P/G': points_per_game, 'Total Points': total_points})

        rr_df.loc[player] = pd.Series(points_dict)
        rr_df = rr_df.sort_values('P/G', ascending=False)
        rr_df['Position'] = rr_df['Position'].str.upper()

    if save_csv is True:
        rr_df.to_csv('2019rrpoints.csv')
    else:
        print(rr_df)


build_fantasy_sheet()
