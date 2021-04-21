import pandas as pd
import math
from random import random
import matplotlib.pyplot as plt

def compute_RSI(vector: pd.Series, method, RSI_Length, tolerance)->pd.Series:

    method = method.lower()

    diff = vector.diff()
    dUp = diff.clip(lower=0)
    dDown = -1*diff.clip(upper=0)

    if method == 'linear':
        rolUp = dUp.rolling(window=RSI_Length, min_periods=RSI_Length - tolerance).mean()
        rolDown = dDown.rolling(window=RSI_Length, min_periods=RSI_Length - tolerance).mean()

    elif method == 'exponential':
        rolUp = dUp.ewm(com=RSI_Length, adjust=False).mean()
        rolDown = dDown.ewm(com=RSI_Length, adjust=False).mean()

    RS = rolUp / rolDown
    RSI = 100 - (100 / (1 + RS))

    return RSI


