from data import Data
import numpy as np
import pandas as pd
import time

Data = Data()

GAMES_TO_USE = 32

PASSING_YARDS = 0.04
PASSING_TD = 4
PASSING_INT = -2
RUSHING_YARDS = 0.1
RUSHING_TD = 6
RECEIVING_YARDS = 0.1
RECEIVING_TD = 6


def _get_positions(players_dict, fant_df):
    positions_dict = {}
    fant_df['FantPos'] = fant_df['FantPos'].astype(str)

    for player in players_dict:
        player_entry = fant_df.loc[fant_df['Player'] == player]
        pos = player_entry.iloc[0]['FantPos']
        positions_dict[player] = pos.upper()

    return positions_dict


def _drop_no_pos_players(players_dict, positions_dict):
    dropped = []
    for player in players_dict:
        if positions_dict[player] == 'nan':
            dropped.append(player)

    for drop in dropped:
        del players_dict[drop]

    return players_dict, dropped


players_dict = Data.players()
fant_df = Data.fantasy_df()
positions_dict = _get_positions(players_dict, fant_df)
players_dict, dropped = _drop_no_pos_players(players_dict, positions_dict)

qbs = [k for k, v in positions_dict.items() if v == 'QB']
rbs = [k for k, v in positions_dict.items() if v == 'RB']
wrs = [k for k, v in positions_dict.items() if v == 'WR']
te = [k for k, v in positions_dict.items() if v == 'TE']

rbs.remove('Ty Montgomery')


def rel_perf_experienced(players, pos):
    pos = pos.upper()
    tot = len(players)
    i = 0
    print(f'Completion time estimate: {tot*2/60} min')

    avg_fp_touch = []
    std_fp_touch = []
    avg_touch = []
    bad_games = []
    result_dict = {}
    for player in players:
        # try:
        df = Data.career_stats(player)

        if len(df) >= GAMES_TO_USE:
            if pos == 'RB':
                df.dropna(subset=['Yds', 'TD', 'Yds.1', 'TD.1', 'Att',
                                  'Rec'], inplace=True)
                df['Yds'] = df['Yds'].astype(float)
                df['TD'] = df['TD'].astype(float)
                df['Yds.1'] = df['Yds.1'].astype(float)
                df['TD.1'] = df['TD.1'].astype(float)
                df['Att'] = df['Att'].astype(int)
                df['Rec'] = df['Rec'].astype(int)

                df['FantPts'] = ((df['Yds']*RUSHING_YARDS) +
                                 (df['TD']*RUSHING_TD) +
                                 (df['TD.1']*RECEIVING_TD) +
                                 (df['Yds.1']*RECEIVING_YARDS))
            elif pos == 'WR':
                if 'Att' not in df.columns:
                    df['Yds.1'] = 0
                    df['Att'] = 0
                    df['TD.1'] = 0

                df.dropna(subset=['Yds', 'TD', 'Yds.1', 'TD.1', 'Att',
                                  'Rec'], inplace=True)
                df['Yds'] = df['Yds'].astype(float)
                df['TD'] = df['TD'].astype(float)
                df['Yds.1'] = df['Yds.1'].astype(float)
                df['TD.1'] = df['TD.1'].astype(float)
                df['Att'] = df['Att'].astype(int)
                df['Rec'] = df['Rec'].astype(int)

                df['FantPts'] = ((df['Yds.1']*RUSHING_YARDS) +
                                 (df['TD.1']*RUSHING_TD) +
                                 (df['TD']*RECEIVING_TD) +
                                 (df['Yds']*RECEIVING_YARDS))
            else:
                print('Please enter a valid position: WR or RB')

            df['Touches'] = df['Att'] + df['Rec']
            df['FP/Touch'] = df['FantPts'] / df['Touches']
            mean = df['FP/Touch'].tail(GAMES_TO_USE).mean()
            median = df['FP/Touch'].tail(GAMES_TO_USE).median()
            std = df['FP/Touch'].tail(GAMES_TO_USE).std()

            touches_mean = df['Touches'].tail(GAMES_TO_USE).mean()
            touches_std = df['Touches'].tail(GAMES_TO_USE).std()

            last_5_perf = (df['FP/Touch'].tail(5).mean() - mean) / std
            last_5_avg_touches = df['Touches'].tail(5).mean()

            avg_fp_per_game = df['FantPts'].tail(5).mean()

            avg_fp_touch.append(mean)
            std_fp_touch.append(std)
            avg_touch.append(touches_mean)

            _dict = {}

            _dict['Mean'] = mean
            _dict['Median'] = median
            _dict['STD'] = std
            _dict['+1SD'] = mean + std
            _dict['-1SD'] = mean - std
            _dict['L5 Rel to Self'] = last_5_perf
            _dict['.30'] = np.quantile(df['FP/Touch'].tail(GAMES_TO_USE),
                                       0.3)
            _dict['.70'] = np.quantile(df['FP/Touch'].tail(GAMES_TO_USE),
                                       0.7)
            _dict['L5 Touches'] = last_5_avg_touches
            _dict['L5 Touches Rel to Self'] = ((df['Touches'].tail(5).mean()
                                               - touches_mean) / touches_std)
            _dict['L5 Avg FP/G'] = avg_fp_per_game

            result_dict[player] = _dict
        else:
            bad_games.append(player)
        # except Exception as e:
        #     print(e)
        #     bad_data.append(player)

        i += 1
        pct_complete = round((i / tot) * 100, 2)
        print(f'{pct_complete}% complete')
        time.sleep(2)

    df = pd.DataFrame.from_dict(result_dict, orient='index')

    league_avg_fp_touch = np.asarray(avg_fp_touch)
    league_std_fp_touch = np.asarray(std_fp_touch)
    league_avg_touch = np.asarray(avg_fp_touch)
    league_std_touch = np.std(league_avg_touch)
    df['Mean Rel to Peers'] = ((df['Mean'] - np.mean(league_avg_fp_touch))
                               / np.std(league_avg_fp_touch))
    df['SD Rel to Peers'] = ((df['STD'] - np.mean(league_std_fp_touch))
                             / np.std(league_std_fp_touch))
    df['Touches Rel to Peers'] = (df['L5 Touches'] - np.mean(league_avg_touch)
                                  / league_std_touch)
    df['Mean Rel to Peers RK'] = df['Mean Rel to Peers'].rank(ascending=False)
    df['STD Rel to Peers RK'] = df['SD Rel to Peers'].rank()
    df['Avg Rank Rel to Peers'] = (df['Mean Rel to Peers RK'] +
                                   df['STD Rel to Peers RK']) / 2

    df.to_csv(f'{pos}relperf.csv')
    df.corr().to_csv(f'{pos}corrtable.csv')


rel_perf_experienced(rbs, 'rb')
rel_perf_experienced(wrs, 'wr')
