import datetime
import logging
import concurrent.futures

from typing import List, Dict, Any, Tuple, Union
from .databot import DataBot
from .constants import CATEGORIES, LOG_FORMAT
from .utils import db_connector

logger = logging.getLogger('CLOSING_DATA_UPDATE')
logging.basicConfig(format=LOG_FORMAT)
logger.setLevel(logging.DEBUG) #Testing only


def update_closing_data(categories: List = CATEGORIES, date=str(datetime.date.today())) -> Tuple:
    """Wrapper function to get data for listed categories.

    Takes in a list of pre-defined categories corresponding to broad sectors of interest (eg, Gold, Volatility, etc.),
    gets closing price data for constituent financial instruments for the current day, logs data to fct_closing_quotes_raw
    for upstream processing

    Params:
        categories: a list of categories to include in the run (predefined in dim_tickers table)
    Returns:
        A tuple containing an int status code indicating status of run and a dict containing any errors:
        100 - Run successfully completed
        200 - Run partially completed with errors
        300 - Run failed
    """
    bots = init_databots(categories=categories, date=date)
    errors = {}
    if len(bots[1]) > 0:
        errors['missing_categories'] = bots[1]

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        update_statuses = list(executor.map(run_databot, bots[0]))

    for status in update_statuses:
        logger.debug(status)
        if len(status['data_retrieval_errors']) > 0:
            errors[status['category']].update({'data_retrieval_errors': status['data_retrieval_errors']})
        if status['db_upload_error']:
            errors[status['category']].update({'db_upload_error': status['db_upload_error']})
    if len(errors) == 0:
        return 100, errors
    elif len(errors) == len(bots[0]):
        return 300, errors
    else:
        return 200, errors


def run_databot(bot: DataBot) -> Dict[str, Union[List, bool]]:
    """Target function to get data from APIs and log to fct_closing_quotes_raw"""
    logger.debug(f'Running {bot}')
    results = bot.get_data()
    upload_status = bot.write_to_db(data_df=results['data_df'], table_name='fct_closing_quotes_raw')
    return {'category': bot.category, 'data_retrieval_errors': results['errors'], 'db_upload_error': upload_status}


def init_databots(categories: List, date: str) -> Tuple:
    """Inits a list of DataBot objects from a list of categories."""
    eng = db_connector()
    with eng.connect() as connection:
        valid_categories = [row[0] for row in connection.execute('SELECT DISTINCT category_name FROM main_category')]
    bots = [DataBot(category=category, date=date) for category in categories if category in valid_categories]
    if len(bots) == len(categories):
        logger.debug(f'Successfully initialized {len(bots)} bots for {len(categories)} categories.')
        return bots, []
    else:
        built_categories = [bot.category for bot in bots]
        missing_categories = set(categories) - set(built_categories)
        logger.error(f'Failed to initialize all requested bots: {str(missing_categories)}')
        return bots, missing_categories


