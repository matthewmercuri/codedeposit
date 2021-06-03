from bs4 import BeautifulSoup
import pandas as pd
import requests

from rbclean import rb_gamelog_cleaned
# from wrclean import wr_gamelog_cleaned
# from qbclean import qb_gamelog_cleaned
# from teclean import te_gamelog_cleaned

BASE_URL = 'https://www.pro-football-reference.com'
YEAR = 2020


def _expand_fantasy_standings(df):
    df['FantPt/G'] = df['Fantasy_FantPt'] / df['Games_G']

    return df


def get_fantasy_table(year=YEAR, save_locally=False):
    URL = BASE_URL + f'/years/{year}/fantasy.htm'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'lxml')

    df = pd.read_html(soup.prettify())[0]
    cols = df.columns

    new_cols = []
    for col in cols:
        top, bottom = col

        if top[:2] == 'Un':
            new_cols.append(bottom)
        else:
            new_cols.append(f'{top}_{bottom}')

    df.columns = new_cols
    df = df[df['Rk'] != 'Rk']
    df.drop(df.columns[0], axis=1, inplace=True)

    df['Player'] = df['Player'].astype(str)
    df['Player'] = df['Player'].apply(lambda x: x.upper().strip())

    df['FantPos'] = df['FantPos'].astype(str)
    df['FantPos'] = df['FantPos'].apply(lambda x: x.upper().strip())

    numeric_cols = df.columns[4:]
    for num_col in numeric_cols:
        df[num_col] = pd.to_numeric(df[num_col], downcast='float')

    df.fillna(0, inplace=True)

    if save_locally is True:
        df.to_csv(f'fantstandings{year}.csv')

    return df


def pos_fantasy_standings(position, year=YEAR):
    position = position.upper()
    df = get_fantasy_table(year)

    valid_pos = ['QB', 'WR', 'TE', 'RB']
    if position in valid_pos:
        df = df[df['FantPos'] == position]
        df = _expand_fantasy_standings(df)
    else:
        print(f'{position} is not a valid position!')

    return df


def active_players(year=YEAR):
    df = get_fantasy_table(year)
    players = df['Player'].to_list()

    return players


def player_profile_links(year=YEAR):
    URL = BASE_URL + f'/years/{year}/fantasy.htm'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'lxml')

    player_profiles = {}

    players_raw = soup.find_all('td', {'data-stat': 'player'})

    for player_raw in players_raw:
        name = player_raw.find('a').contents[0].upper().strip()
        prof_link = player_raw.find('a', href=True)['href']
        player_profiles[name] = prof_link

    return player_profiles


def active_player_gamelog(player):
    player = player.upper()
    player_profiles = player_profile_links()

    df = None

    if player not in player_profiles:
        print(player_profiles)
        print(f'Unable to pull gamelog data for {player}.')
    else:
        URL = BASE_URL + player_profiles[player] + '/gamelog/'
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'lxml')
        if player_profiles[player] == 'QB':
            df = qb_gamelog_cleaned(soup)
        elif player_profiles[player] == 'RB':
            df = rb_gamelog_cleaned(soup)
        elif player_profiles[player] == 'WR':
            df = wr_gamelog_cleaned(soup)
        elif player_profiles[player] == 'TE':
            df = te_gamelog_cleaned(soup)
        else:
            print(f'Do not know the position for {player}')

    return df


# qb_df = pos_fantasy_standings('qb')
# qb_df.to_csv('qbs.csv')
# print(qb_df.describe())

# print(active_players())
# print(active_player_info())
