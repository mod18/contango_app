import datetime
import logging
from typing import List
from .constants import CATEGORIES, LOG_FORMAT
from .closing_data_update import update_closing_data
from .closing_data_transform import transform_closing_data

from .utils import db_connector

logger = logging.getLogger('DATA_BACKFILL')
logging.basicConfig(format=LOG_FORMAT)
logger.setLevel(logging.DEBUG)


def backfill_data(start_date: str, end_date: str = None, categories: List = CATEGORIES, purge=False) -> None:
    """Function to mass backfill data.

    Optionally, specify purge=True to first delete all data from the given dates from the database.
    """
    if not end_date:
        end_date = start_date

    if purge:
        purge_tables(start_date=start_date, end_date=end_date)

    dates = build_datelist(start_date, end_date)
    jobs = [{'date': date, 'category': category} for date in dates for category in categories]
    for job in jobs:
        update_closing_data(categories=[job['category']], date=job['date'])
        transform_closing_data(date=job['date'])
        logger.debug(f"Backfill complete for {str(job['category'])} on {str(job['date'])}")
    return


def purge_tables(start_date: str, end_date: str) -> None:
    """Deletes all data in all pipeline tables for a given date range.

    Designed to be used from an interpreter/CLI, requires user confirmation.

    Obviously be careful using this.
    """
    tables = [
        'fct_closing_quotes_raw',
        'fct_closing_quotes_daily',
        'fct_etf_daily',
        'fct_futures_daily',
    ]
    confirm = input(f'Confirm deletion of ALL data from {len(tables)} tables between {start_date} and {end_date}: Y/N\n')
    if confirm == 'Y':
        eng = db_connector()
        with eng.connect() as connection:
            for table in tables:
                connection.execute(f"DELETE FROM {table} WHERE date BETWEEN '{start_date}' AND '{end_date}';")
        logger.debug(f'All data from {str(tables)} deleted between {start_date} and {end_date}')
    return


def build_datelist(start_date: str, end_date: str) -> List:
    """Returns a list of dates from a start and end date."""
    format = '%Y-%m-%d'
    start_d = datetime.datetime.strptime(start_date, format)
    end_d = datetime.datetime.strptime(end_date, format)
    cur_date = start_d
    dates = []
    while cur_date <= end_d:
        if cur_date.weekday() < 5:
            dates.append(datetime.datetime.strftime(cur_date, format))
        cur_date += datetime.timedelta(days=1)
    return dates
