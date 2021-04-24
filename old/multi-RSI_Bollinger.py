import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time, datetime
from datetime import datetime
print("Lets start...")
stocks = ['TSLA']
#['UBER','FLT.V','TSLA','eark.ne','rci-b.to','SNDL','PLTR','PBR',"AAL",'A','AAL','AAP','AAPL','ABBV','ABC','ABMD','ABT','ACN','ADBE','ADI','ADM','ADP','ADSK','AEE','AEP','AES','AFL','AIG','AIZ','AJG','AKAM','ALB','ALGN','ALK','ALL','ALLE','ALXN','AMAT','AMCR','AMD','AME','AMGN','AMP','AMT','AMZN','ANET','ANSS','ANTM','AON','AOS','APA','APD','APH','APTV','ARE','ATO','ATVI','AVB','AVGO','AVY','AWK','AXP','AZO','BA','BAC','BAX','BBY','BDX','BEN','BF-B','BIIB','BIO','BK','BKNG','BKR','BLK','BLL','BMY','BR','BRK-B','BSX','BWA','BXP','C','CAG','CAH','CARR','CAT','CB','CBOE','CBRE','CCI','CCL','CDNS','CDW','CE','CERN','CF','CFG','CHD','CHRW','CHTR','CI','CINF','CL','CLX','CMA','CMCSA','CME']
#,'FLT.V','TSLA','eark.ne','rci-b.to','BTC-USD'

#Interval required 5 minutes
StartBal = 1000
sl = StartBal
Nshares = 0
buy = 0
RSIL = 0
b = 0
tv = 0
olddata = 0
LastRSI = 0
LastLBPer = 10000000
LastUBPer = 10000000
LastClose =10000000
now = 0
while True:

	for stock in stocks:
		data = yf.download(tickers=stock, period='2d', interval='1m',progress=False)
		#data.to_csv(stock + '.csv')
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


		
		data['AD'] = 0
		#ADL Line
		data['CMFV'] = (((data['Close']-data['Low'])-(data['High']-data['Close']))/(data['High']-data['Low']))*data['Volume']
		data['AD'] = data['CMFV'].rolling(14, min_periods=14).sum()
		data['AD'] = data['AD'].shift(1)
		#print(data)
		#data.to_csv(stock + '.csv')
		#data = data[data.index.strftime('%Y-%m-%d') == '2021-02-23']
		
		data=data.tail(n=1)
		
		for index, row in data.iterrows():
			timestr = '15:57:00'
			now = index
			if now != olddata:
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
				if buy  == 0 and row['RSI'] <= 30 and LastRSI < row['RSI'] and LastClose < row['Close'] and row['AD'] < row['Close']:
					Nshares = math.floor(StartBal / row['Close'])
					StartBal -= row['Close'] * Nshares
					buy = 1
					b+=1
					print(f"{index} - BOUGHT - Balance {StartBal}")
				if buy == 1 and row['RSI'] >= 70 and LastRSI > row['RSI']  and LastClose < row['Close'] and row['AD'] > row['Close']:
					StartBal += row['Close'] * Nshares
					Nshares = 0
					buy = 0
					print(f"{index} - SOLD - Balance {StartBal}")
				if TStop == 1 and buy ==1:
					StartBal += row['Close'] * Nshares
					Nshares = 0
					buy = 0
					print(f"{index} - SOLD - Balance {StartBal} ")
				#print(f"Last RSI = {LastRSI} Current {row['RSI']} Last Close = {LastClose} current {row['Close']} and AD = {row['AD']}")
				LastRSI = row['RSI']
				LastClose = row['Close']
				LastLBPer = row['LBPer']
				LastUBPer = row['UBPer']
				#print(f"stock {stock} time {now} - current price {LastClose} its this clsoe to low bol {row['LBPer']} beg {sl} end {StartBal}  pending {buy} and tr {b}")
		olddata = now
	time.sleep(1)
	