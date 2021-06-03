import pandas as pd
from bs4 import BeautifulSoup


def rb_gamelog_cleaned(soup):
    df = pd.read_html(soup.prettify())[0]

    return df
