import datetime
import logging
import re
import requests
import os
import pandas as pd
from time import sleep
from typing import Dict
from .constants import QUANDL_API_KEY, LOG_FORMAT
from .custom_errors import TickerNotFoundError, TooManyTickersError

logger = logging.getLogger('QUANDL')
logging.basicConfig(format=LOG_FORMAT)
logger.setLevel(logging.DEBUG)

class QuandlClient:
    """Base class for Quandl API.

    Quandl is used as a source of free FUTURES data. Equity/ETF data is obtained using the Alphavantage API (alphav.py)

    """
    def __init__(self):
        self.base_url = 'https://www.quandl.com/api/v3/datasets/'

    def __repr__(self):
        return 'QUANDL_API_WRAPPER'

    def get(self, ticker: str, exchange: str, format='.json', api_key=QUANDL_API_KEY, date=str(datetime.date.today())) -> Dict:
        """Method to send request to Quandl API.

        Example use for ES front month and back month:
            q = QuandlClient()
            es1 = q.get(ticker='es1', exchange='cme') #Front month ES
            es2 = q.get(ticker='es2', exchange='cme') #Back month ES

        Params:
            ticker: the ticker to pull (case insensitive) Where applicable, the ticker MUST include the contract number as well as the abbreviation.
            exchange: the exchange where the contract is trade (typically the CME)
            api_key: the Quandl API key to authenticate
            format: the format of data to return from the API (default: json)
            date: the date to retrieve the data (default: current date)
        Returns:
            A Dict with the most recent price data for a ticker
        """
        try:
            base_ticker = re.search(r'([A-Za-z]+)', ticker).group(0)
            contract_num = re.search(r'([0-9]+)', ticker).group(0)
        except AttributeError:
            logger.error(f'Unable to parse {ticker}. Please ensure a ticker and contract number are specified')
            raise TickerNotFoundError

        ticker_details = self._get_ticker_details(base_ticker, exchange)

        request_url = self.base_url + ticker_details['Quandl Code'] + contract_num + format + f'?api_key={api_key}&start_date={date}&end_date={date}'
        logger.debug(f'Request URL: {request_url}')

        attempts = 1
        while attempts <= 5:
            try:
                logger.info(f'Getting data for {base_ticker}{contract_num} with API key {api_key}. Attempt {attempts}/5 ...')
                response = requests.get(request_url)
                if response.ok:
                    dataset = response.json()['dataset']
                    if len(dataset['data']) > 0:
                        logger.info(f'Data successfully retrieved for {base_ticker}{contract_num} on {date}')
                        return dict(zip(dataset['column_names'], dataset['data'][0]))
                    else:
                        last_available_date = dataset['newest_available_date']
                        logger.info(f'No data found for {ticker} on {date}. Getting data for last available date ({last_available_date})')
                        return self.get(ticker=ticker, exchange=exchange, date=last_available_date)
                elif response.status_code == 429:
                    sleep(attempts * attempts)
                    continue
                else:
                    logger.error(f'Bad response from API: {response.status_code}')
                    continue
            except Exception as e:
                print(f'{e}')
            finally:
                attempts += 1

    @staticmethod
    def _get_ticker_details(ticker: str, exchange: str) -> Dict:
        """Gets Quandl table/symbol from continuous.csv mapping.

        Returns:
                A dict with the ticker, number of available contracts and the table code.
        """
        tickers_df = pd.read_csv('contango_data/ref/continuous.csv')
        ticker_lookup_df = tickers_df[['Ticker', 'Exchange', 'Number of Contracts', 'Quandl Code']]
        ticker_details = ticker_lookup_df[(ticker_lookup_df['Ticker'] == ticker.upper()) & (ticker_lookup_df['Exchange'] == exchange.upper())]
        if len(ticker_details) == 1:
            return ticker_details.to_dict(orient='records')[0]
        elif len(ticker_details) == 0:
            raise TickerNotFoundError
