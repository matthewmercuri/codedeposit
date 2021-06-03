import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv('test.csv', index_col=0)
print(len(df))
print(df.corr())

X = df.iloc[:, :-1]
y = df.iloc[:, -1:]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

reg = LinearRegression(normalize=True).fit(X_train, y_train)

print(f'Paramaters: {reg.coef_}')
print(f'Intercept: {reg.intercept_}')
print(f'R Squared: {reg.score(X_test, y_test)}')
