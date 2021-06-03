import pandas as pd

YEAR = '2019'
PATH_TO_PASS = f'data/{YEAR} Results/{YEAR}passpoints.csv'
PATH_TO_RR = f'data/{YEAR} Results/{YEAR}rrpoints.csv'

FANT_STATS = f'data/{YEAR}fantasy.csv'
FANT_DF = fant_stats()

MIN_GAMES = 8

PASSING_STATS = pd.read_csv(f'Data/{YEAR}passing.csv')
RUSHING_STATS = pd.read_csv(f'Data/{YEAR}rushing.csv')
RECEIVING_STATS = pd.read_csv(f'Data/{YEAR}receiving.csv')

pass_df = pd.read_csv(PATH_TO_PASS, index_col=0)
rr_df = pd.read_csv(PATH_TO_RR, index_col=0)


def fantasy_rankings(csv=False):
    selectors = ['Position', 'Games', 'P/G', 'Total Points']
    p_df = pass_df[selectors]
    r_df = rr_df[selectors]
    df = pd.concat([p_df, r_df])
    df = df.sort_values('P/G', ascending=False)
    df['Position'] = df.apply(_get_pos, axis=1)

    if csv is True:
        df.to_csv(f'{YEAR}fantasyrankings.csv')
    else:
        print(df)

    return df


def fant_stats(player_stats_file=FANT_STATS):
    df = pd.read_csv(player_stats_file, skiprows=1)
    df = df[df['G'] >= MIN_GAMES]
    df = df.apply(_name_code, axis=1)
    df = df.set_index('Player')
    return df


def _name_code(x):
    code = x['Player'].split('\\', 1)
    x['Code'] = code[1]
    x['Player'] = code[0]
    x['Player'] = x['Player'].split('*', 1)[0]
    x['Code'] = x['Code'].strip()
    x['Player'] = x['Player'].strip()
    return x


def _get_pos(x):
    player = x['Player']
    x['Position'] = FANT_DF['FantPos'].loc[player]


def passing():
    pass


fantasy_rankings()
# readclean()
