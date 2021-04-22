import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time, datetime
import sqlite3

con = sqlite3.connect("/Users/christiansierra/Desktop/alg/DB/stocks.db")
#stocks = ['NIO']
data = pd.read_sql_query("select DISTINCT symbol FROM stocks_hist",con)
stocks = data['symbol']
for stock in stocks: 
	x = datetime.datetime.strptime("2021-02-22","%Y-%m-%d").date()- datetime.timedelta(days=30)
	print(x)
	print(datetime.date.today())
	N = 0
	while x <= datetime.date.today():
		y= x + datetime.timedelta(days=7)
		data = yf.download(tickers=stock, start=x, end=y, interval='1m')
		data['symbol']=stock

		print(data)
		if data.empty:
			pass
		else:
			data.to_sql('stocks_hist', con, if_exists='append', index=True)
		"""
		if N == 0:
			data.to_csv(stock + '.csv')
			
			N = 1
		else:
			data.to_csv(stock + '.csv',mode='a',header=False)"""
		x = y
		print(x)
		print(datetime.date.today())