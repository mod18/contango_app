# dim_categories
"""
drop table dim_categories;
create table dim_categories (category_name TEXT);

insert into dim_categories (category_name)
values
('S&P500 Index'),
('Volatility'),
('Gold'),
('Silver'),
('Oil')
;
"""

# dim_tickers
"""
drop table dim_tickers;
create table dim_tickers (ticker_name TEXT PRIMARY_KEY, category TEXT, ticker_type TEXT, link TEXT, exchange TEXT, num_contracts INTEGER, leverage_ratio INTEGER);

insert into dim_tickers (ticker_name, category, ticker_type, link, exchange, num_contracts, leverage_ratio)
values
('SPY', 'S&P500 Index', 'ETF', NULL, NULL, NULL, 1),
('SPXS', 'S&P500 Index', 'ETF', NULL, NULL, NULL, -3),
('SPXL', 'S&P500 Index', 'ETF', NULL, NULL, NULL, 3),
('ES', 'S&P500 Index', 'Future', NULL, 'CME', 3, NULL),
('VXX', 'Volatility', 'ETF', NULL, NULL, NULL, 1),
('UVXY', 'Volatility', 'ETF', NULL, NULL, NULL, 3),
('SVXY', 'Volatility', 'ETF', NULL, NULL, NULL, -1),
('VX', 'Volatility', 'Future', NULL, 'CBOE', 3, NULL),
('GLD', 'Gold', 'ETF', NULL, NULL, NULL, 1),
('GC', 'Gold', 'Future', NULL, 'CME', 3, NULL),
('SLV', 'Silver', 'ETF', NULL, NULL, NULL, 1),
('SI', 'Silver', 'Future', NULL, 'CME', 3, NULL),
('USO', 'Oil', 'ETF', NULL, NULL, NULL, 1),
('SCO', 'Oil', 'ETF', NULL, NULL, NULL, -2),
('CL', 'Oil', 'Future', NULL, 'CME', 3, NULL)
;
"""

# fct_closing_quotes_raw
"""
drop table fct_closing_quotes_raw;
create table fct_closing_quotes_raw (date TEXT, ticker_name TEXT, ticker_contract INT, closing_price REAL, retrieved_ts INTEGER, source TEXT);
"""
# fct_closing_quotes_daily
"""
drop table fct_closing_quotes_daily;
create table fct_closing_quotes_daily (date TEXT, ticker_name TEXT, ticker_contract INT, closing_price REAL, retrieved_ts INTEGER, source TEXT);
"""
# fct_futures_daily
"""
drop table fct_futures_daily;
create table fct_futures_daily (id INTEGER, date TEXT, ticker_id TEXT, contango TEXT, front_contango REAL, closing_price_1 REAL, c1_quote_id TEXT, closing_price_2 REAL, c2_quote_id TEXT, closing_price_3 REAL, c3_quote_id TEXT);
"""
# fct_etf_daily
"""
drop table fct_etf_daily;
create table fct_etf_daily (id INTEGER, ticker_id INTEGER, date TEXT, closing_price REAL);
"""