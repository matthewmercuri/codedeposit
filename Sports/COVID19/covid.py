import matplotlib.pyplot as plt
import pandas as pd

DATA_URL = "https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv"
DATA_START = "2020-04-15"

DESIRED_COLS = ['Total Cases', 'Total tests completed in the last day',
                'Under Investigation', 'Deaths']

df = pd.read_csv(DATA_URL, index_col=0, infer_datetime_format=True)
df = df[DESIRED_COLS]
df['New Cases'] = df['Total Cases'].diff()
df = df[df.index >= DATA_START]

df['Positives/Test'] = df['New Cases'] / df['Total tests completed in the last day']
df['Positivity Rate'] = df['Positives/Test'] * 100
df['Positives per thousand tests'] = df['Positives/Test'] * 1000
df['PptT 30 MA'] = df['Positives per thousand tests'].rolling(window=30).mean()
df['PptT 15 MA'] = df['Positives per thousand tests'].rolling(window=15).mean()
df['PptT 5 MA'] = df['Positives per thousand tests'].rolling(window=5).mean()

print(df.tail())
print(df.describe())


def positivity_analysis():
    x = df.index

    plt.xticks(rotation=70)

    plt.plot(x, df['Positives per thousand tests'], label="Pos/1000")
    plt.plot(x, df['PptT 30 MA'], label="30 MA")
    plt.plot(x, df['PptT 15 MA'], label="15 MA")
    plt.plot(x, df['PptT 5 MA'], label="5 MA")
    plt.legend()

    plt.show()


def test_backlog():
    x = df.index
    plt.xticks(rotation=70)
    plt.plot(x, df['Under Investigation'])
    plt.show()


positivity_analysis()
test_backlog()
