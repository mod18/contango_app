import pytest
import pandas as pd
from utils.constants import ALPHAVANTAGE_API_KEY
from utils.apis import AlphavantageApi

class TestAlphavantageApi:
    def test_build_request_url(self):
        wrapper = AlphavantageApi()
        url = f'https://www.alphavantage.co/query?apikey={ALPHAVANTAGE_API_KEY}&function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPY'
        test_url = wrapper._build_request_url(params={'function': 'TIME_SERIES_DAILY_ADJUSTED', 'symbol': 'SPY'})
        print(test_url)
        assert url == test_url



