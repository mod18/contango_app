# https://stackoverflow.com/questions/34425607/how-to-write-a-pandas-dataframe-to-django-model


from django.conf import settings
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

import os, sys
sys.path.insert(0, os.path.abspath(""))
os.environ['DJANGO_SETTINGS_MODULE'] = 'contango.settings'
import django
django.setup()

database_name = settings.DATABASES['default']['NAME']
database_url = f'sqlite:///{database_name}'
engine = create_engine(database_url, echo=False)

t = [('SPY', 5, 'ETF', np.nan, np.nan, np.nan, 1),
('SPXS', 5, 'ETF', np.nan, np.nan, np.nan, -3),
('SPXL', 5, 'ETF', np.nan, np.nan, np.nan, 3),
('ES', 5, 'Future', np.nan, 'CME', 3, np.nan),
('VXX', 1, 'ETF', np.nan, np.nan, np.nan, 1),
('UVXY', 1, 'ETF', np.nan, np.nan, np.nan, 3),
('SVXY', 1, 'ETF', np.nan, np.nan, np.nan, -1),
('VX', 1, 'Future', np.nan, 'CBOE', 3, np.nan),
('GLD', 2, 'ETF', np.nan, np.nan, np.nan, 1),
('GC', 2, 'Future', np.nan, 'CME', 3, np.nan),
('SLV', 4, 'ETF', np.nan, np.nan, np.nan, 1),
('SI', 4, 'Future', np.nan, 'CME', 3, np.nan),
('USO', 3, 'ETF', np.nan, np.nan, np.nan, 1),
('SCO', 3, 'ETF', np.nan, np.nan, np.nan, -2),
('CL', 3, 'Future', np.nan, 'CME', 3, np.nan)]

df = pd.DataFrame(data=t, columns=['ticker_name', 'category_id', 'ticker_type', 'link', 'exchange', 'num_contracts', 'leverage_ratio'])
df.to_sql(con=engine, name='main_ticker', if_exists='append', index=False)

insert into fct_etf_daily (id, ticker_id, date, closing_price)
values
(3, 48, '2020-12-07', 31.00),
(2, 48, '2020-12-06', 30.00),
(1, 48, '2020-12-05', 29.00)