from datetime import date, timedelta
import numpy as np
import pandas as pd
from scipy import stats

WAGER = 10

teams = pd.read_csv('Data/teamnames.csv')
teams = teams['Teams'].values.tolist()

_today = date.today()
today = pd.Timestamp(date.today())
yesterday = pd.Timestamp(today - timedelta(1))
_tomorrow = today + timedelta(1)
tomorrow = pd.Timestamp(today + timedelta(1))

scores_df = pd.read_csv('Data/scores_df.csv', index_col=0)
scores_df['Date'] = pd.to_datetime(scores_df['Date'])


def get_team_scores(team):
    df = scores_df[(scores_df['Visitor'] == team) | (scores_df['Home'] == team)]
    return df


def truncate_to_yesterday(df):
    df = df[df['Date'] <= yesterday]
    return df


def truncate_to_today(df):
    df = df[df['Date'] <= today]
    return df


def get_team_goals_array(df, team):
    df = truncate_to_yesterday(df)
    df = df[(df['Visitor'] == team) | (df['Home'] == team)]
    df = df.reset_index()
    goals_array = np.zeros(len(df))
    for i in range(0, len(df)):
        if df['Visitor'].iloc[i] == team:
            goals = df['G'].iloc[i]
            goals_array[i] = goals
        elif df['Home'].iloc[i] == team:
            goals = df['G.1'].iloc[i]
            goals_array[i] = goals
    return goals_array


def get_team_goal_diff_array(df, team):
    df = truncate_to_yesterday(df)
    df = df[(df['Visitor'] == team) | (df['Home'] == team)]
    df = df.reset_index()
    goal_diff_array = np.zeros(len(df))
    for i in range(0, len(df)):
        if df['Visitor'].iloc[i] == team:
            gf = df['G'].iloc[i]
            ga = df['G.1'].iloc[i]
            g_diff = gf - ga
            goal_diff_array[i] = g_diff
        elif df['Home'].iloc[i] == team:
            gf = df['G.1'].iloc[i]
            ga = df['G'].iloc[i]
            g_diff = gf - ga
            goal_diff_array[i] = g_diff
    return goal_diff_array


def find_nhl_goals_array(df):
    home_goals_array = np.zeros(len(df))
    away_goals_array = np.zeros(len(df))
    for i in range(0, len(df)):
        home_goals_array[i] = df['G'].iloc[i]
        away_goals_array[i] = df['G.1'].iloc[i]


def construct_goals_for_df(teams, n_last_games, save=True):
    columns = ['Average Goals For', 'STD Goals For']
    goals_df = pd.DataFrame(columns=columns, index=[team for team in teams])
    last_games = -n_last_games

    for team in teams:
        team_df = get_team_scores(team)
        team_df = truncate_to_yesterday(team_df)
        team_goals_array = get_team_goals_array(team_df, team)
        team_mean_goals = np.mean(team_goals_array[last_games:])
        team_std_goals = np.std(team_goals_array[last_games:])

        goals_df.loc[team] = [team_mean_goals, team_std_goals]

    goals_df.sort_values(by=['Average Goals For'], ascending=False, inplace=True)

    if save is True:
        goals_df.to_csv(f'Results/nhl_goals_info_last{n_last_games}_{_today}.csv')

    return goals_df


def construct_goal_diff_df(teams, n_last_games, save=True):
    columns = ['Average Goal Diff', 'STD Goal Diff']
    diff_df = pd.DataFrame(columns=columns, index=[team for team in teams])
    last_games = -n_last_games

    for team in teams:
        team_df = get_team_scores(team)
        team_df = truncate_to_yesterday(team_df)
        team_goal_diff_array = get_team_goal_diff_array(team_df, team)
        team_mean_goal_diff = np.mean(team_goal_diff_array[last_games:])
        team_std_goal_diff = np.std(team_goal_diff_array[last_games:])

        diff_df.loc[team] = [team_mean_goal_diff, team_std_goal_diff]

    diff_df.sort_values(by=['Average Goal Diff'], ascending=False, inplace=True)

    if save is True:
        diff_df.to_csv(f'Results/nhl_goal_diff_info_last{n_last_games}_{_today}.csv')

    return diff_df


def todays_games(take_last=30, df=scores_df, dist='normal'):
    df = df[df['Date'] == today]
    df = df.reset_index()

    predictions_df = pd.DataFrame(columns=['Home', 'Home Win Percent',
                                           'Away', 'Away Win Percent'])

    for i in range(0, len(df)):
        home = df['Home'].loc[i]
        away = df['Visitor'].loc[i]

        home_win_per, away_win_per = monte_carlo(home, away, dist)

        predictions_df.loc[i] = [home, home_win_per, away, away_win_per]

    predictions_df['Home Odds'] = 1 / (predictions_df['Home Win Percent']*(10**(-2)))
    predictions_df['Away Odds'] = 1 / (predictions_df['Away Win Percent']*(10**(-2)))

    predictions_df['Adj Home Odds'] = predictions_df['Home Odds']*0.95
    predictions_df['Adj Away Odds'] = predictions_df['Away Odds']*1.05

    predictions_df.to_csv(f'Results/predicted_odds_last{take_last}_{_today}_{dist}.csv')

    return predictions_df


def tomorrows_games(take_last=30, df=scores_df, dist='normal'):
    df = df[df['Date'] == tomorrow]
    df = df.reset_index()

    predictions_df = pd.DataFrame(columns=['Home', 'Home Win Percent',
                                           'Away', 'Away Win Percent'])

    for i in range(0, len(df)):
        home = df['Home'].loc[i]
        away = df['Visitor'].loc[i]

        home_win_per, away_win_per = monte_carlo(home, away, dist)

        predictions_df.loc[i] = [home, home_win_per, away, away_win_per]

    predictions_df['Home Odds'] = 1 / (predictions_df['Home Win Percent']*(10**(-2)))
    predictions_df['Away Odds'] = 1 / (predictions_df['Away Win Percent']*(10**(-2)))

    predictions_df['Adj Home Odds'] = predictions_df['Home Odds']*0.95
    predictions_df['Adj Away Odds'] = predictions_df['Away Odds']*1.05

    predictions_df.to_csv(f'Results/predicted_odds_last{take_last}_tomorrow_pre_{dist}.csv')

    return predictions_df


def monte_carlo(home, away, dist, take_last=30, n_sims=100000, teams=teams):
    team_goal_data_df = construct_goals_for_df(teams, take_last, save=False)

    home_mean = team_goal_data_df['Average Goals For'].loc[home]
    away_mean = team_goal_data_df['Average Goals For'].loc[away]

    home_std = team_goal_data_df['STD Goals For'].loc[home]
    away_std = team_goal_data_df['STD Goals For'].loc[away]

    if dist == 'normal':
        home_goals = np.random.normal(home_mean, home_std, n_sims)
        away_goals = np.random.normal(away_mean, away_std, n_sims)
    elif dist == 'poisson':
        home_goals = np.random.poisson(home_mean, n_sims)
        away_goals = np.random.poisson(away_mean, n_sims)

    home_wins_array = home_goals > away_goals

    home_wins = sum(home_wins_array)
    away_wins = n_sims - home_wins

    home_win_percent = round((home_wins / n_sims)*100, 4)
    away_win_percent = round((away_wins / n_sims)*100, 4)
    print(f'The home team wins: {home_win_percent} percent of the time!')

    return home_win_percent, away_win_percent


def monte_carlo_goal_diff(home, away, take_last=30, n_sims=100000, teams=teams):
    team_goal_diff_df = construct_goal_diff_df(teams, take_last, save=False)

    home_mean = team_goal_diff_df['Average Goal Diff'].loc[home]
    away_mean = team_goal_diff_df['Average Goal Diff'].loc[away]

    home_std = team_goal_diff_df['STD Goal Diff'].loc[home]
    away_std = team_goal_diff_df['STD Goal Diff'].loc[away]

    home_goal_diff = np.random.normal(home_mean, home_std, n_sims)
    away_goal_diff = np.random.normal(away_mean, away_std, n_sims)

    home_wins_array = home_goal_diff > away_goal_diff

    home_wins = sum(home_wins_array)
    away_wins = n_sims - home_wins

    home_win_percent = round((home_wins / n_sims)*100, 4)
    away_win_percent = round((away_wins / n_sims)*100, 4)
    print(f'The home team wins: {home_win_percent} percent of the time!')

    return home_win_percent, away_win_percent


def todays_games_diff(take_last=30, df=scores_df, dist='normal'):
    df = df[df['Date'] == today]
    df = df.reset_index()

    predictions_df = pd.DataFrame(columns=['Home', 'Home Win Percent',
                                           'Away', 'Away Win Percent'])

    for i in range(0, len(df)):
        home = df['Home'].loc[i]
        away = df['Visitor'].loc[i]

        home_win_per, away_win_per = monte_carlo_goal_diff(home, away)

        predictions_df.loc[i] = [home, home_win_per, away, away_win_per]

    predictions_df['Home Odds'] = 1 / (predictions_df['Home Win Percent']*(10**(-2)))
    predictions_df['Away Odds'] = 1 / (predictions_df['Away Win Percent']*(10**(-2)))

    predictions_df['Adj Home Odds'] = predictions_df['Home Odds']*0.95
    predictions_df['Adj Away Odds'] = predictions_df['Away Odds']*1.05

    predictions_df.to_csv(f'Results/predicted_odds_last{take_last}_{_today}_goaldiff.csv')

    return predictions_df


def tomorrows_games_diff(take_last=30, df=scores_df):
    df = df[df['Date'] == tomorrow]
    df = df.reset_index()

    predictions_df = pd.DataFrame(columns=['Home', 'Home Win Percent',
                                           'Away', 'Away Win Percent'])

    for i in range(0, len(df)):
        home = df['Home'].loc[i]
        away = df['Visitor'].loc[i]

        home_win_per, away_win_per = monte_carlo_goal_diff(home, away)

        predictions_df.loc[i] = [home, home_win_per, away, away_win_per]

    predictions_df['Home Odds'] = 1 / (predictions_df['Home Win Percent']*(10**(-2)))
    predictions_df['Away Odds'] = 1 / (predictions_df['Away Win Percent']*(10**(-2)))

    predictions_df['Adj Home Odds'] = predictions_df['Home Odds']*0.95
    predictions_df['Adj Away Odds'] = predictions_df['Away Odds']*1.05

    predictions_df.to_csv(f'Results/predicted_odds_last{take_last}_tomorrow_pre_goaldiff.csv')

    return predictions_df

# print(scores_df, today, yesterday)
# leafs_df = get_team_scores('Toronto Maple Leafs')
# leafs_df = truncate_to_yesterday(leafs_df)
# leafs_gf = get_team_goals_array(leafs_df, 'Toronto Maple Leafs')

# print(leafs_df)
# print(leafs_gf)
# print(np.var(leafs_gf[30:]))
# print(np.mean(leafs_gf[30:]))
# print(teams)

# contstuct_goals_for_df(teams, 50)


# monte_carlo('Minnesota Wild', 'Dallas Stars', take_last=20)
# todays_games(take_last=15)
todays_games_diff(take_last=20)
# tomorrows_games(take_last=30)
# tomorrows_games_diff(take_last=20)
# todays_games(take_last=20, dist='poisson')

# print(get_team_goals_array(scores_df, 'Toronto Maple Leafs'))
# print(get_team_goal_diff_array(scores_df, 'Toronto Maple Leafs'))
# print(stats.kstest(get_team_goal_diff_array(scores_df, 'Toronto Maple Leafs'), 'norm'))
# print(stats.kstest(get_team_goals_array(scores_df, 'Toronto Maple Leafs'), 'norm'))
