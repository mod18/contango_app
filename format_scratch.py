from data.alphav import AlphavantageClient
av = AlphavantageClient()
d = av.get(ticker='tsla', function=av.functions['stock_sma'], interval='daily', time_period='8', series_type='close')

ticker_name TEXT, ticker_type TEXT, exchange TEXT, num_contracts INTEGER

from data.databot import DataBot
d = DataBot('S&P500 Index')
m = d.get_manifest(

from data.closing_data import update_closing_data
c = ['Volatility', 'Bonds']
s = update_closing_data(categories=c)


# AV test
https://www.alphavantage.co/query?apikey=7BWY4BELAWAZJZ74&function=TIME_SERIES_DAILY_ADJUSTED&symbol=%5EGSPC

https://www.alphavantage.co/query?function=SYMBOL_SEARCH&apikey=7BWY4BELAWAZJZ74&keywords=vix