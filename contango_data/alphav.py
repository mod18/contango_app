import datetime
import json
import logging
import re
import requests
from time import sleep
from .constants import ALPHAVANTAGE_API_KEY, LOG_FORMAT

logger = logging.getLogger('ALPHAVANTAGE')
logging.basicConfig(format=LOG_FORMAT)
logger.setLevel(logging.DEBUG)


class AlphavantageClient:
    """Wrapper for the Alphavantage API.

    Documentation at https://www.alphavantage.co/documentation/.
    """
    def __init__(self):
        self.base_url = 'https://www.alphavantage.co/query?'
        self.functions = {'stock_daily': 'TIME_SERIES_DAILY_ADJUSTED',
                          'stock_weekly': 'TIME_SERIES_WEEKLY_ADJUSTED',
                          'stock_sma': 'SMA',
                          'stock_ema': 'EMA',
                          }

    def __repr__(self):
        return 'Alphavantage_API_Wrapper'

    def get(self, ticker: str, function: str, date=str(datetime.date.today()), api_key=ALPHAVANTAGE_API_KEY, **kwargs) -> json:
        """Gets data from Alphavantage API.
        
        Params:
            ticker: the ticker of interest
            function: the API function to use
            api_key: the api key to authenticate
            kwargs: other parameters depend on the function used (see API docs)
            
        Returns:
            A pandas DataFrame with the specified data
        """
        params = {'function': function,
                  'symbol': ticker.upper(),
                  }
        for k, v in kwargs.items():
            params[k] = v

        request_url = self._build_request_url(params=params, api_key=api_key)
        attempts = 1
        while attempts <= 5:
            try:
                logger.info(f'Getting data for {ticker} with API key {api_key}. Attempt {attempts}/5 ...')
                response = requests.get(request_url)
                if response.ok:
                    logger.info(f'Data successfully retrieved for {ticker}')
                    return AlphavantageClient._format_response(response.json(), date=date)
                elif response.status_code == 429:
                    sleep(attempts * attempts)
                    continue
                else:
                    logger.error(f'Bad response from API for {ticker}: {response.status_code}')
                    continue
            except Exception as e:
                print(f'{e}')
            finally:
                attempts += 1

    def _build_request_url(self, params: dict, api_key: str) -> str:
        request_url = self.base_url + f'apikey={api_key}'
        for k, v in params.items():
            request_url += f'&{k}={v}'
        logger.debug(f'Request URL: {request_url}')
        return request_url

    @classmethod
    def _format_response(cls, json_response: json, date: str) -> dict:
        """Formats API response to just get most recent days' data."""
        clean_metadata = AlphavantageClient._clean_keys(json_response['Meta Data'])
        ticker = clean_metadata['Symbol']
        last_day = clean_metadata['Last Refreshed']
        raw_data_key = list(json_response.keys())[1]
        try:
            raw_data = json_response[raw_data_key][date]
        except KeyError:
            logger.info(f'No data found for {ticker} on {date}, defaulting to most recent day.')
            date = last_day
            raw_data = json_response[raw_data_key][date]

        clean_raw_data = AlphavantageClient._clean_keys(raw_data)
        formatted_data = {'ticker': ticker, 'date': date,}
        for k, v in clean_raw_data.items():
            formatted_data[k] = v
        return formatted_data

    @classmethod
    def _clean_keys(cls, data: json) -> dict:
        """Cleans up the formatting of keys by removing non-alphanumeric chars."""
        data_clean_keys = {}
        for k, v in data.items():
            clean_key = re.search(r'(\w+ ?\w+)', k).group(0)
            data_clean_keys[clean_key] = v
        return data_clean_keys






