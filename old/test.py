import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time, datetime
from datetime import datetime

stock = 'NVEI.TO'
#Interval required 5 minutes
StartBal = 100
TL = 0
TT = 0
Bought = 0
TStop = 0
TB = 0
TS = 0
data = yf.download(tickers=stock, period='5d', interval='1m')
data['MA20'] = data['Close'].rolling(window=20).mean()
data['20dSTD'] = data['Close'].rolling(window=20).std()
data['Upper'] = data['MA20'] + (data['20dSTD'] * 2)
data['Lower'] = data['MA20'] - (data['20dSTD'] * 2)
data['Upper1s'] = data['MA20'] + (data['20dSTD'] * 1)
data['Lower1s'] = data['MA20'] - (data['20dSTD'] * 1)
data['LBPer']=(data['Close']/data['Lower'])-1

#ADL Line
data['CMFV'] = (((data['Close']-data['Low'])-(data['High']-data['Close']))/(data['High']-data['Low']))*data['Volume']
data['AD'] = data['AD'].shift(1) + data['CMFV']

dt = pd.DataFrame(data=data[['Close','Lower','Upper','MA20','Upper1s','Lower1s','LBPer']])
dt = dt[dt.index.strftime('%Y-%m-%d') == '2021-02-19']
print(dt)

for index, row in dt.iterrows():
	print(index)
	timestr = '15:57:00'
	now = index
	current_time = now.strftime("%H:%M:%S")
	ftr = [3600,60,1]
	tv = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]) - sum([a*b for a,b in zip(ftr, map(int,current_time.split(':')))])
	if tv<0:
		#determines if time is 3:57 and sells the position
		TStop = 1
	if row['Close']< row['Lower']:
		TL += 1
	if Bought == 0:
		if row['Close'] > row['Lower'] and row['Close'] < row['Lower1s']and TL ==1:
			StartBal -= row['Close']
			Bought = 1
			TB +=1
			TL = 0
		elif row['Close'] > row['Lower1s'] and row['Close'] < row['Upper']:
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
		elif row['Close'] > row['Upper']:
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
print(str(Bought) + "End Balance: " + str(StartBal) +"Traded "+ str(TB) + "-" + str(TS))



