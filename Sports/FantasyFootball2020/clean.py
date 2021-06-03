import pandas as pd

YEAR = '2019'
FANT_STATS_PATH = f'data/{YEAR}fantasy.csv'

RR_SELECTORS = ['Att', 'Yds', 'Y/A', 'Tgt', 'Rec', 'Yds',	'Y/R', 'Ctch%', 'Y/Tgt']

MIN_GAMES = 8


def fant_stats(player_stats_file=FANT_STATS_PATH):
    df = pd.read_csv(player_stats_file, skiprows=1)
    df = df[df['G'] >= MIN_GAMES]
    df = df.apply(_name_code, axis=1)
    df = df.apply(_first_initial, axis=1)
    df = df.set_index('Player')
    df.dropna(subset=['FantPt'], inplace=True)
    df = _add_stats(df)
    df = df.sort_values('FantPt/G', ascending=False)
    df.to_csv('2019Fant.csv')
    return df


def fant_stats_by_pos(save_csv=False):
    df = fant_stats()
    qb_df = df[df['FantPos'] == "QB"]
    rb_df = df[df['FantPos'] == "RB"]
    wr_df = df[df['FantPos'] == "WR"]
    te_df = df[df['FantPos'] == "TE"]

    if save_csv is True:
        qb_df.to_csv('data/2019Results/qb.csv')
        rb_df.to_csv('data/2019Results/rb.csv')
        wr_df.to_csv('data/2019Results/wr.csv')
        te_df.to_csv('data/2019Results/te.csv')


def get_rr_data():
    INITIAL = 'M'
    CODE = 'McCaCh01'
    url = f'https://www.pro-football-reference.com/players/{INITIAL}/{CODE}/gamelog/'
    dfs = pd.read_html(url, skiprows=1)
    df = dfs[0]
    df = df.droplevel(1, axis=1)
    df = df.set_index('Date')
    df = df[df['Year'] != 'Year']
    df = df[:-1]
    df = df[RR_SELECTORS]
    # df = df[df['Year'] >= 2018]
    print(df)


def _name_code(x):
    code = x['Player'].split('\\', 1)
    x['Code'] = code[1]
    x['Player'] = code[0]
    x['Player'] = x['Player'].split('*', 1)[0]
    x['Code'] = x['Code'].strip()
    x['Player'] = x['Player'].strip()
    return x


def _first_initial(x):
    name = x['Code']
    initial = name[0]
    x['Initial'] = initial
    return x


def _add_stats(df):
    df['FantPt/G'] = df['FantPt'] / df['G']
    df['PPR/G'] = df['PPR'] / df['G']
    return df


fant_stats()
# fant_stats_by_pos(True)
get_rr_data()
