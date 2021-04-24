import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time, datetime
from datetime import datetime

stocks = ['uber']
#['UBER','FLT.V','TSLA','eark.ne','rci-b.to','SNDL','PLTR','PBR',"AAL",'A','AAL','AAP','AAPL','ABBV','ABC','ABMD','ABT','ACN','ADBE','ADI','ADM','ADP','ADSK','AEE','AEP','AES','AFL','AIG','AIZ','AJG','AKAM','ALB','ALGN','ALK','ALL','ALLE','ALXN','AMAT','AMCR','AMD','AME','AMGN','AMP','AMT','AMZN','ANET','ANSS','ANTM','AON','AOS','APA','APD','APH','APTV','ARE','ATO','ATVI','AVB','AVGO','AVY','AWK','AXP','AZO','BA','BAC','BAX','BBY','BDX','BEN','BF-B','BIIB','BIO','BK','BKNG','BKR','BLK','BLL','BMY','BR','BRK-B','BSX','BWA','BXP','C','CAG','CAH','CARR','CAT','CB','CBOE','CBRE','CCI','CCL','CDNS','CDW','CE','CERN','CF','CFG','CHD','CHRW','CHTR','CI','CINF','CL','CLX','CMA','CMCSA','CME']
#'UBER','FLT.V','TSLA','eark.ne','rci-b.to'
StartBal = 100

for stock in stocks: 
	#Interval required 5 minutes
	sl = StartBal
	buy = 0
	RSIL = 0
	b = 0
	tv = 0
	data = yf.download(tickers=stock, start='2021-01-24', interval='1m',end='2021-01-30',progress=False)
	#RSI CALC
	data['Return'] = np.log(data['Close'] / data['Close'].shift(1) )
	data['Movement'] = data['Close'] - data['Close'].shift(1)
	data['up'] = np.where((data['Movement'] > 0) ,data['Movement'],0)
	data['down'] = np.where((data['Movement'] < 0) ,data['Movement'],0)
	window_length = 20
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
	
	data = data[data.index.strftime('%Y-%m-%d') == '2021-02-23']
	#data.to_csv(stock + '.csv')
	LastRSI = 0
	LastLBPer = 10000000
	LastUBPer = 10000000
	LastClose =10000000
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
		if buy  == 0 and row['RSI'] < 30 and LastRSI < row['RSI'] and LastLBPer< 0.001  and LastClose < row['Close']:
			StartBal -= row['Close']
			buy = 1
			b+=1
			print(f"{index} - BOUGHT")
		if buy == 1 and row['RSI'] >= 70 and LastRSI < row['RSI'] and LastUBPer< 0.003  and LastClose < row['Close']:
			StartBal += row['Close']
			buy = 0
			print(f"{index} - SOLD")
		if TStop == 1 and buy ==1:
			StartBal += row['Close']
			buy = 0
		if TStop == 1 and buy ==1:
			StartBal += row['Close']
			buy = 0
		LastRSI = row['RSI']
		LastClose = row['Close']
		LastLBPer = row['LBPer']
		LastUBPer = row['UBPer']
	print(f"stock {stock} beg {sl} end {StartBal}  pending {buy} and tr {b}")