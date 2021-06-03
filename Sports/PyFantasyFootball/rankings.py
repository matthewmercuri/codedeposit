import pandas as pd
import pyfantasyfootball as ff
import time

MIN_GAMES = 11

# FANTASY POINTS
FP_PASS_YDS = 0.04
FP_PASS_TD = 4
FP_INT = -2
FP_RUSH_YDS = 0.1
FP_RUSH_TD = 6
FP_REC_YDS = 0.1
FP_REC_TD = 6
FP_KICK_PR_TD = 6
FP_FUM_LOST = -2
FP_2PT_CONV = 2

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


def rb_rankings():
    total = len(rbs)
    i = 0

    print(f'Approximate time: {total*2.5}s')

    rb_dfs = []
    for rb in rbs:
        df = ff.Data.fantasy_gamelogs(rb)
        if len(df) >= MIN_GAMES:
            try:
                df = rb_expand(df)
                df['Player'] = rb

                df = df[['Player', 'Touches 5G MA', 'FantPt 5G MA',
                         'Touches 10G MA', 'FantPt 10G MA']]
                df = df.tail(1)
                rb_dfs.append(df)
            except Exception as e:
                print(e)
                print(rb)

        i += 1
        print(f'{round((i/total)*100, 2)}% complete')
        time.sleep(2)

    rb_df = pd.concat(rb_dfs)
    rb_df.set_index('Player', inplace=True)

    return rb_df


def wr_rankings():
    total = len(wrs)
    i = 0

    print(f'Approximate time: {total*2.5}s')

    wr_dfs = []
    for wr in wrs:
        df = ff.Data.fantasy_gamelogs(wr)
        if len(df) >= MIN_GAMES:
            try:
                df = wr_expand(df)
                df['Player'] = wr

                df = df[['Player', 'Touches 5G MA', 'FantPt 5G MA',
                         'Touches 10G MA', 'FantPt 10G MA']]
                df = df.tail(1)
                wr_dfs.append(df)
            except Exception as e:
                print(e)
                print(wr)

        i += 1
        print(f'{round((i/total)*100, 2)}% complete')
        time.sleep(2)

    wr_df = pd.concat(wr_dfs)
    wr_df.set_index('Player', inplace=True)

    return wr_df


def rb_expand(df):
    df = standard_expand(df)

    return df


def wr_expand(df):
    df = standard_expand(df)

    return df


def standard_expand(df):
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

    return df


# print(ff.Data.fantasy_gamelogs('Ezekiel Elliott').to_csv('zeke.csv'))
# print(ff.Data.fantasy_gamelogs('Ezekiel Elliott').columns)
# rb_expand(ff.Data.fantasy_gamelogs('Ezekiel Elliott')).to_csv('zeke.csv')

rb_rankings().to_csv('rbranks.csv')
wr_rankings().to_csv('wrranks.csv')
