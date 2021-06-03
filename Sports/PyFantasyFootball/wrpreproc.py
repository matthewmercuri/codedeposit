import pandas as pd
import pyfantasyfootball as ff
import time

MIN_GAMES = 11

players_dict = ff.Data.players()

qbs = []
wrs = []
rbs = []
tes = []
no_pos = []

for player, info in players_dict.items():
    if info['Position'] == 'QB':
        qbs.append(player)
    elif info['Position'] == 'RB':
        rbs.append(player)
    elif info['Position'] == 'WR':
        wrs.append(player)
    elif info['Position'] == 'TE':
        tes.append(player)
    else:
        no_pos.append(player)


def wr_train_set():
    i = 0
    total = len(wrs)

    not_enough_games = []
    trouble_features_df = []
    train_dfs = []
    for player in wrs:
        game_df = ff.Data.fantasy_gamelogs(player)
        if len(game_df) >= MIN_GAMES:
            try:
                feature_df = _features(game_df)
                train_dfs.append(feature_df)
            except Exception:
                print(f'Had trouble creating features df for {player}')
                trouble_features_df.append(player)
        else:
            not_enough_games.append(player)

        print(f'{round((i/total)*100, 2)}% complete')
        i += 1
        time.sleep(2)

    train_df = pd.concat(train_dfs)
    train_df.to_csv('train.csv')


def _features(df):
    df['Touches'] = df['Rushing_Att'] + df['Receiving_Rec']
    df['FPt/Touch'] = df['FantPt'] / df['Touches']

    df['Touches 5G MA'] = df['Touches'].rolling(window=5).mean()
    df['Touches 10G MA'] = df['Touches'].rolling(window=10).mean()
    df['Touches 5-10'] = df['Touches 5G MA'] - df['Touches 10G MA']

    df['FPt/Touch 5G MA'] = df['FPt/Touch'].rolling(window=5).mean()
    df['FPt/Touch 10G MA'] = df['FPt/Touch'].rolling(window=10).mean()
    df['FPt/Touch 5-10'] = df['FPt/Touch 5G MA'] - df['FPt/Touch 10G MA']

    df['FantPt 5G MA'] = df['FantPt'].rolling(window=5).mean()
    df['FantPt 10G MA'] = df['FantPt'].rolling(window=10).mean()
    df['FantPt 5-10'] = df['FantPt 5G MA'] - df['FantPt 10G MA']

    df['TD 5G MA'] = (df['Receiving_TD'] +
                      df['Rushing_TD']).rolling(window=5).mean()
    df['FantPt 5G Med'] = df['FantPt 5G MA'].rolling(window=5).median()
    df['Snaps 5G MA'] = df['Off. Snaps_Num'].rolling(window=5).mean()

    df['FantPt NEXT 5 AVG'] = df['FantPt 5G MA'].shift(periods=5)

    return df


# wr_train_set()
_features(ff.Data.fantasy_gamelogs("Cooper Kupp")).to_csv('kupp.csv')
