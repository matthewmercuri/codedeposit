import pandas as pd
import pyfantasyfootball as ff
import time

MIN_GAMES = 7

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


def qb_df(qb):
    df = ff.Data.fantasy_gamelogs(qb)

    if len(df) >= MIN_GAMES:
        df['Avg_L5_FantPt'] = df['FantPt'].rolling(window=5).mean()
        df['Att'] = df['Passing_Att'] + df['Rushing_Att']
        df['FP/Att'] = df['FantPt'] / df['Att']
        df['Avg_L5_Att'] = df['Att'].rolling(window=5).mean()
        df['Avg_L5_FP/Att'] = df['FP/Att'].rolling(window=5).mean()

        df['Next_Game_FP'] = df['FantPt'].shift(-1)  # what we want to predict

    return df


def qb_trainset():
    needed_cols = ['Avg_L5_Att', 'Avg_L5_FP/Att', 'Next_Game_FP']

    total = len(qbs)
    i = 0
    print(f'Approximate time {total*2}s')

    train_df = []
    for qb in qbs:
        print(qb)
        df = qb_df(qb)
        if len(df) >= MIN_GAMES:
            df = df[needed_cols]
            df.dropna(inplace=True)
            train_df.append(df)

        i += 1
        print(f'{round((i/total)*100, 2)}% complete')
        time.sleep(2)

    train_df = pd.concat(train_df)
    train_df.to_csv('test.csv')


# print(qb(qbs[0]))
qb_trainset()
