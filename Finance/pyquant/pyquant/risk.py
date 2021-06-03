import numpy as np
import pandas as pd


def log_returns(price_series, period=1):
    log_returns = np.log(price_series) - np.log(price_series.shift(period))
    return log_returns
