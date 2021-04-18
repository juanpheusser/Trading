import requests
import pandas as pd
import numpy as np

import requests
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import math

request_frequency_minutes = 1
sample_periods = 14
datetime_change = timedelta(minutes=request_frequency_minutes)

params = {
    'access_key': 'e55c6599b2fddba05caaec9976eeb003',
    'symbols': 'GE,BAC,USO,LTM,BCS,DAL,BCH,TSLA,FB,AAPL',
    'interval': str(request_frequency_minutes) + 'min'
}

api_result = requests.get('https://api.marketstack.com/v1/tickers/intraday/latest', params)
