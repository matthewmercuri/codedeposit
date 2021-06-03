from data import Data
import numpy as np
import os
import pandas as pd

Data = Data()

TOP = 16

depth_files = os.listdir('./depth/')

qb = []
rb1 = []
rb2 = []
rb3 = []
wr1 = []
wr2 = []
wr3 = []
wr4 = []
te = []

for _file in depth_files:
    df = pd.read_csv(f'depth/{_file}', index_col=0)

    _qb = df.iloc[0][0]
    qb.append(_qb)

    _rb1 = df.iloc[1][0]
    rb1.append(_rb1)
    _rb2 = df.iloc[1][1]
    rb2.append(_rb2)
    _rb3 = df.iloc[1][2]
    rb3.append(_rb3)

    _wr1 = df.iloc[2][0]
    wr1.append(_wr1)
    _wr2 = df.iloc[2][1]
    wr2.append(_wr2)
    _wr3 = df.iloc[2][2]
    wr3.append(_wr3)
    _wr4 = df.iloc[2][3]
    wr4.append(_wr4)

    _te = df.iloc[3][0]
    te.append(_te)

# print(qb)
# print(rb1)
# print(rb2)
# print(rb3)
# print(wr1)
# print(wr2)
# print(wr3)
# print(wr4)
# print(te)

fant_df = Data.fantasy_df()
fant_df['FantPt'] = pd.to_numeric(fant_df['FantPt'], errors='coerce')
fant_df['G'] = pd.to_numeric(fant_df['G'], errors='coerce')
fant_df['FP/G'] = fant_df['FantPt'] / fant_df['G']
fant_df.dropna(subset=['FP/G'], inplace=True)
fant_df.set_index('Player', inplace=True)


fant_df['Rel'] = 0.0


def generate_relative_scores(players, pos, filename):
    pos = pos.upper()

    averages = []
    errors = []
    for player in players:
        try:
            pts = fant_df.loc[player]['FP/G']
            averages.append(pts)
        except Exception:
            errors.append(player)
    averages = np.array(averages)
    averages[::-1].sort()
    averages = averages[:TOP]

    qb_avg = np.mean(averages)

    for player in players:
        try:
            value = fant_df.loc[player]['FP/G'] - qb_avg
            fant_df.at[player, 'Rel'] = value
        except Exception:
            pass

    df = fant_df[fant_df['FantPos'] == pos]
    df = df['Rel']
    df = df.sort_values(ascending=False)
    df.to_csv(f'relranks/{pos}.csv')

    return df, errors


# =============== QB ===============
# qb_averages = []
# errors = []
# for q in qb:
#     try:
#         pts = fant_df.loc[q]['FP/G']
#         qb_averages.append(pts)
#     except Exception:
#         errors.append(q)
# qb_averages = np.array(qb_averages)
# qb_averages[::-1].sort()
# qb_averages = qb_averages[:TOP]

# qb_avg = np.mean(qb_averages)

# for q in qb:
#     try:
#         value = fant_df.loc[q]['FP/G'] - qb_avg
#         fant_df.at[q, 'Rel'] = value
#     except Exception:
#         pass

# qb_df = fant_df[fant_df['FantPos'] == 'QB']
# qb_df = qb_df.sort_values(by='Rel', ascending=False)
# ==================================

# print(qb_df)
generate_relative_scores(qb, 'QB', 'QB')
generate_relative_scores(te, 'TE', 'TE')
generate_relative_scores(rb1, 'RB', 'RB1')
generate_relative_scores(rb2, 'RB', 'RB2')
generate_relative_scores(rb3, 'RB', 'RB3')
generate_relative_scores(wr1, 'WR', 'WR1')
generate_relative_scores(wr2, 'WR', 'WR2')
generate_relative_scores(wr3, 'WR', 'WR3')
generate_relative_scores(wr4, 'WR', 'WR4')
