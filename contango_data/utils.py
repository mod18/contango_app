import django
import os
import sys
from typing import Dict
from contango import get_env_variable

from django.conf import settings
from sqlalchemy import create_engine, engine


def db_connector() -> engine.Engine:
    """Util to connect to main database.

    Refactor this to support future database migration away from sqlite.

    Params:
        database (str): the name of the database to connect to

    Returns:
        Connection string to the database
    """
    sys.path.insert(0, os.path.abspath(""))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'contango.settings'
    django.setup()

    database_url = f"postgresql+psycopg2://{get_env_variable('DB_USER')}:{get_env_variable('DB_PASSWORD')}@{get_env_variable('DB_HOST')}:{get_env_variable('DB_PORT')}/{get_env_variable('DB_NAME')}"
    eng = create_engine(database_url, execution_options={'isolation_level': 'READ COMMITTED',}, echo=False)
    return eng


def get_sql(filename: str, formatting_map: Dict[str, str] = None) -> str:
    sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql', filename)
    with open(sql_path, 'r') as sql_file:
        if formatting_map:
            sql = sql_file.read().format_map(formatting_map)
        else:
            sql = sql_file.read()
    return sql
