import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time, datetime
from datetime import datetime

stocks = ['UBER']

for stock in stocks: 
	#Interval required 5 minutes
	StartBal = 1000
	sl = StartBal
	TL = 0
	TT = 0
	Bought = 0
	TStop = 0
	TB = 0
	TS = 0
	TU1s =0
	data = yf.download(tickers=stock, period='5d', interval='1m')
	data['MA20'] = data['Close'].rolling(window=20).mean()
	data['20dSTD'] = data['Close'].rolling(window=20).std()
	data['Upper'] = data['MA20'] + (data['20dSTD'] * 2)
	data['Lower'] = data['MA20'] - (data['20dSTD'] * 2)
	data['Upper1s'] = data['MA20'] + (data['20dSTD'] * 1)
	data['Lower1s'] = data['MA20'] - (data['20dSTD'] * 1)
	data['LBPer']=(data['Close']/data['Lower'])-1
	data['UBPer']=(data['Upper']/data['Close'])-1
	data['UBPer1s']=(data['Close']/data['Upper1s'])-1

	data = data[data.index.strftime('%Y-%m-%d') == '2021-02-23']
	lastclose = 0
	for index, row in data.iterrows():
		timestr = '15:57:00'
		now = index
		current_time = now.strftime("%H:%M:%S")
		ftr = [3600,60,1]
		tv = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]) - sum([a*b for a,b in zip(ftr, map(int,current_time.split(':')))])
		if tv<0:
			#determines if time is 3:57 and sells the position
			TStop = 1
		if lastclose< row['Lower']:
			TL += 1
		if lastclose< row['Upper1s']:
			TU1s += 1
		if Bought == 0:
			""" if row['LBPer'] < 0.0015 and row['LBPer'] > 0 and TL ==1:
				StartBal -= row['Close']
				Bought = 1
				TB +=1
				TL = 0"""
			if row['UBPer1s']< 0.001 and TU1s ==1:
				StartBal -= row['Close']
				Bought = 1
				TB +=1
				TL = 0
		if Bought == 1:
			if TL >2:
				StartBal += row['Close']
				Bought = 0
				TT =0
				TS +=1
				TL=0
			if TU1s >2:
				StartBal += row['Close']
				Bought = 0
				TT =0
				TS +=1
				TU1s =0
			elif row['UBPer']<0.003:
				StartBal += row['Close']
				Bought = 0
				TT =0
				TS +=1

			elif TStop == 1:
				StartBal += row['Close']
				Bought = 0
				TT =0
				TStop = 0
				TS +=1
		lastclose = row['Close']
	print(stock + " " +str(StartBal) + "  " + str(Bought) +"End Balance: " + str(((StartBal/sl)-1)*100)+"Traded "+ str(TB) + "-" + str(TS))


