import datetime
import time
import logging
import os
import pandas as pd
from typing import Dict, List, Union
from .constants import LOG_FORMAT
from .alphav import AlphavantageClient
from .quandl import QuandlClient
from .utils import db_connector, get_sql

logger = logging.getLogger('DATABOT')
logging.basicConfig(format=LOG_FORMAT)
logger.setLevel(logging.DEBUG) #Testing only


class DataBot:
    """Class to organize fetching data from APIs and storing in database.

    Designed to take in two parameters:
        1. The category of data to retrieve (Volatility, Gold, etc.)
        2. The date to pull (default is the current date)
    """
    def __init__(self, category: str, date=str(datetime.date.today())):
        self.category = category
        self.date = date
        self.manifest = self.get_manifest()
        self.root = os.path.abspath(__name__)

    def __repr__(self):
        return f'DataBot_{self.category}_{self.date}'

    def get_manifest(self) -> list:
        """Queries database for relevant tickers to pull."""
        manifest = []
        eng = db_connector()
        query = get_sql(filename='get_manifest.sql', formatting_map={'category_name': self.category})
        with eng.connect() as connection:
            result = connection.execute(query)
            for row in result:
                manifest_entry = {'ticker_name': row[0], 'ticker_type': row[1], 'exchange': row[2], 'num_contracts': row[3],
                                  'leverage_ratio': row[4]}
                manifest.append(manifest_entry)
        return manifest

    def get_data(self) -> Dict[str, Union[pd.DataFrame, List]]:
        """Gets data from relevant APIs based on request.

        Returns:
            A dict containing the results of the request as a DataFrame and a list containing any errors
        """
        api_manifest = {'alphavantage': [], 'quandl': [],}
        payload = []
        errs = []
        for row in self.manifest:
            if row['ticker_type'] == 'Future':
                api_manifest['quandl'].append({'ticker_name': row['ticker_name'], 'exchange': row['exchange'], 'num_contracts': row['num_contracts'],})
            else:
                api_manifest['alphavantage'].append({'ticker_name': row['ticker_name'],})

        if len(api_manifest['quandl']) > 0:
            q = QuandlClient()
            for row in api_manifest['quandl']:
                num_contracts = range(1, row['num_contracts'] + 1)
                for contract in num_contracts:
                    base_ticker = row['ticker_name']
                    ticker_with_contract = base_ticker + str(contract)
                    exchange = row['exchange']
                    data = q.get(ticker=ticker_with_contract, exchange=exchange, date=self.date)
                    try:
                        # Why oh why aren't the date fields consistently named..
                        if data.get('Trade Date'):
                            data['Date'] = data.pop('Trade Date')
                        payload.append({
                            'date': data['Date'],
                            'ticker_name': base_ticker,
                            'ticker_contract': contract,
                            'closing_price': data['Settle'],
                            'retrieved_ts': int(time.time()),
                            'source': 'quandl',
                        })
                    except TypeError as t:
                        logger.error(f'No data retrieved for {ticker_with_contract}: {t}')
                        errs.append(ticker_with_contract)
                        continue
                    except KeyError as k:
                        logger.error(f'KeyError while parsing response for {ticker_with_contract}. Check data response format for any needed adjustments: {k}')
                        logger.debug(data)
                        errs.append(ticker_with_contract)
                        continue
                    except Exception as e:
                        logger.error(f'An unknown error occurred while updating the data for {ticker_with_contract}: {e}')
                        errs.append(ticker_with_contract)
                        continue

        if len(api_manifest['alphavantage']) > 0:
            av = AlphavantageClient()
            for row in api_manifest['alphavantage']:
                ticker = row['ticker_name']
                data = av.get(ticker=ticker, function=av.functions['stock_daily'], date=self.date)
                try:
                    payload.append({
                        'date': data['date'],
                        'ticker_name': ticker,
                        'ticker_contract': None,
                        'closing_price': data['adjusted close'],
                        'retrieved_ts': int(time.time()),
                        'source': 'alphavantage',
                    })
                except TypeError as t:
                    logger.error(f'No data retrieved for {ticker}: {t}')
                    errs.append(ticker)
                    continue
                except Exception as e:
                    logger.error(f'An unknown error occurred while updating the data for {ticker}: {e}')
                    errs.append(ticker)
                    continue

        return {'data_df': pd.DataFrame(payload), 'errors': errs}

    def write_to_db(self, data_df: pd.DataFrame, table_name: str) -> bool:
        """Uploads a DataFrame to a SQL database.

        Returns False if no error, True if error.
        """
        try:
            con = db_connector()
            data_df.to_sql(con=con, name=table_name, if_exists='append', index=False)
            logger.info(f'{data_df.shape[0]} rows inserted into {table_name} ({self.category})')
            return False
        except Exception as e:
            logger.error(f'{e}')
            return True
