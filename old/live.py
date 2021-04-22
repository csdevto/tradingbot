import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time, datetime
from datetime import datetime

stock = 'UBER'
#,'FLT.V','TSLA','eark.ne','rci-b.to','BTC-USD'

#Interval required 5 minutes
StartBal = 100
sl = StartBal
buy = 0
RSIL = 0
b = 0
tv = 0
while True: 
	data = yf.download(tickers=stock, period='1d', interval='1m',progress=False)
	#RSI CALC
	data['Return'] = np.log(data['Close'] / data['Close'].shift(1) )
	data['Movement'] = data['Close'] - data['Close'].shift(1)
	data['up'] = np.where((data['Movement'] > 0) ,data['Movement'],0)
	data['down'] = np.where((data['Movement'] < 0) ,data['Movement'],0)
	window_length = 14
	#calculate moving average of the last 14 days  gains
	up = data['up'].rolling(window_length).mean()

	#calculate moving average of the last 14 days  losses
	down = data['down'].abs().rolling(window_length).mean()

	RS = up / down

	data['RSI'] = 100.0 - (100.0 / (1.0 + RS))

	#Bollinger bands, 1 std and 2 std 
	data['MA20'] = data['Close'].rolling(window=20).mean()
	data['20dSTD'] = data['Close'].rolling(window=20).std()
	data['Upper'] = data['MA20'] + (data['20dSTD'] * 2)
	data['Lower'] = data['MA20'] - (data['20dSTD'] * 2)
	data['Upper1s'] = data['MA20'] + (data['20dSTD'] * 1)
	data['Lower1s'] = data['MA20'] - (data['20dSTD'] * 1)
	data['LBPer']=(data['Close']/data['Lower'])-1
	data['UBPer']=(data['Upper']/data['Close'])-1
	data['UBPer1s']=(data['Close']/data['Upper1s'])-1
	#data.to_csv(stock + '.csv')
	#data = data[data.index.strftime('%Y-%m-%d') == '2021-02-19']
	LastRSI = 0
	LastLBPer = 10000000
	LastUBPer = 10000000
	LastClose =10000000
	data=data.tail(n=1)
	for index, row in data.iterrows():
		timestr = '15:57:00'
		now = index
		current_time = now.strftime("%H:%M:%S")
		ftr = [3600,60,1]
		tv = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]) - sum([a*b for a,b in zip(ftr, map(int,current_time.split(':')))])
		TStop = 0
		if tv<0:
			#determines if time is 3:57 and sells the position
			TStop = 1
		'''if buy == 1:
			StartBal += row['Close']
			buy = 0'''
		"""if buy  == 0 and row['RSI'] < 30 and LastRSI < row['RSI'] and LastLBPer< 0.001  and LastClose < row['Close']:
			StartBal -= row['Close']
			buy = 1
			b+=1
			print(f"{index} - BOUGHT")
		if buy == 1 and row['RSI'] >= 70 and LastRSI < row['RSI'] and LastUBPer< 0.003  and LastClose < row['Close']:
			StartBal += row['Close']
			buy = 0
			print(f"{index} - SOLD")"""
		if buy  == 0 and LastLBPer< 0.001  and LastClose < row['Close']:
			StartBal -= row['Close']
			buy = 1
			b+=1
			print(f"{index} - BOUGHT")
		if buy == 1 and LastUBPer< 0.003  and LastClose < row['Close']:
			StartBal += row['Close']
			buy = 0
			print(f"{index} - SOLD")
		if TStop == 1:
			StartBal += row['Close']
			buy = 0
		LastRSI = row['RSI']
		LastClose = row['Close']
		LastLBPer = row['LBPer']
		LastUBPer = row['UBPer']
	print(f"stock {stock} time {now} - current price {LastClose} end {StartBal}  pending {buy} and tr {b} - low bol {LastLBPer}")
	time.sleep(1)
	