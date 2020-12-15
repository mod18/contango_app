import datetime
import logging
from typing import Tuple

from .utils import db_connector, get_sql
from .constants import LOG_FORMAT

logger = logging.getLogger('CLOSING_DATA_TRANSFORM')
logging.basicConfig(format=LOG_FORMAT)
logger.setLevel(logging.DEBUG)


def transform_closing_data(date = str(datetime.date.today())) -> Tuple:
    """Wrapper function to transform closing data.

    Output tables:
    1. fct_futures_daily
    2. fct_etf_daily

    Params:
        None
    Returns:
        A tuple containing an int status code indicating status of run and a dict containing any errors:
        100 - Run successfully completed
        300 - Run failed
    """
    eng = db_connector()
    errors = []
    tables = ['fct_closing_quotes_daily', 'fct_futures_daily', 'fct_etf_daily']
    with eng.connect() as connection:
        for table in tables:
            try:
                logger.debug(f'Updating {table}')
                filename = table + '.sql'
                logger.debug(get_sql(filename=filename, formatting_map={'date': date}))
                trans = connection.begin()
                connection.execute(get_sql(filename=filename, formatting_map={'date': date}))
                trans.commit()
            except Exception as e:
                logger.error(f'{table} update FAILED: {e}')
                errors.append(table)
                return 300, errors
        logger.debug('All tables updated successfully')
        return 100, errors
