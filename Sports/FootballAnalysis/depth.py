from bs4 import BeautifulSoup
import pandas as pd
import requests


BASE_URL = 'https://www.fantasypros.com/nfl/depth-charts.php'

r = requests.get(BASE_URL)
soup = BeautifulSoup(r.text, 'lxml')

divs = soup.find_all('div', class_='team-list')

dfs = []
for div in divs:
    team = div.find('input')['value']
    positions = div.find_all('div', class_='position-list')

    data = {}
    for pos in positions:
        pos_name = pos.find('h4').text
        pos_name = pos_name[3:]

        players = [x.text for x in pos.find_all('a')]
        data[pos_name] = players

    df = pd.DataFrame.from_dict(data, orient='index')
    df.to_csv(f'depth/{team}.csv')
