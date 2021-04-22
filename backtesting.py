import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time, datetime, math
from datetime import datetime
import sqlite3

con = sqlite3.connect("/Users/christiansierra/Desktop/alg/DB/stocks.db")
#con.row_factory = sqlite3.Row
#stocks = ['eark.ne']
data = pd.read_sql_query("select DISTINCT symbol FROM stocks_hist",con)
stocks = data['symbol']
#['UBER','FLT.V','TSLA','eark.ne','rci-b.to','SNDL','PLTR','PBR',"AAL",'A','AAL','AAP','AAPL','ABBV','ABC','ABMD','ABT','ACN','ADBE','ADI','ADM','ADP','ADSK','AEE','AEP','AES','AFL','AIG','AIZ','AJG','AKAM','ALB','ALGN','ALK','ALL','ALLE','ALXN','AMAT','AMCR','AMD','AME','AMGN','AMP','AMT','AMZN','ANET','ANSS','ANTM','AON','AOS','APA','APD','APH','APTV','ARE','ATO','ATVI','AVB','AVGO','AVY','AWK','AXP','AZO','BA','BAC','BAX','BBY','BDX','BEN','BF-B','BIIB','BIO','BK','BKNG','BKR','BLK','BLL','BMY','BR','BRK-B','BSX','BWA','BXP','C','CAG','CAH','CARR','CAT','CB','CBOE','CBRE','CCI','CCL','CDNS','CDW','CE','CERN','CF','CFG','CHD','CHRW','CHTR','CI','CINF','CL','CLX','CMA','CMCSA','CME']
#,'FLT.V','TSLA','eark.ne','rci-b.to','BTC-USD'
##AMD AND INTEL DOING BEST
#Interval required 5 minutes
StartBal = 1000
Nshares = 0
sl = StartBal
buy = 0
RSIL = 0
b = 0
tv = 0
olddata = 0
per=[]

for stock in stocks:
	
	data = pd.read_sql_query("SELECT * FROM stocks_hist WHERE symbol='" + stock + "' ORDER BY Datetime ASC ",con,index_col='Datetime')
	data.index = pd.to_datetime(data.index)
	print(data)
	#data = yf.download(tickers=stock, period='5d', interval='1m',progress=False)
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
	#data.to_csv('csv/' + stock + '.csv')

	#data = data[data.index.strftime('%Y-%m-%d') == '2021-02-17']
	LastRSI = 0
	LastLBPer = 10000000
	LastUBPer = 10000000
	LastClose =10000000
	now = 0
	#data=data.tail(n=1)
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
			'''if buy  == 0 and row['RSI'] < 10 and LastRSI < row['RSI'] and row['Close'] < row['Lower'] and LastClose < row['Close'] and row['AD'] < row['Close']:
				Nshares = math.floor(StartBal / row['Close'])
				StartBal -= row['Close'] * Nshares
				buy = 1
				b+=1
				print(f"{index} - BOUGHT - at {row['Close']} - {Nshares} # of shares")
			if buy == 1 and row['RSI'] > 70 and LastRSI > row['RSI'] and row['Close'] > LastUB and LastClose < row['Close'] and row['AD'] > row['Close']:
				StartBal += row['Close'] * Nshares
				Nshares = 0
				buy = 0
				print(f"{index} - SOLD - Balance {StartBal}")'''
			if buy == 1 and row['RSI'] >= 80 and LastRSI > row['RSI']  and LastClose < row['Close'] and row['AD'] > row['Close']:
				StartBal += row['Close'] * Nshares
				Nshares = 0
				buy = 0
				per.append((((StartBal/sl)-1)*100))
				#print(f"{index} - SOLD - Balance {StartBal} % Made {(((StartBal/sl)-1)*100)}")
			'''if TStop == 1 and buy ==1:
				StartBal += row['Close'] * Nshares
				Nshares = 0
				buy = 0
				per.append((((StartBal/sl)-1)*100))
				#print(f"{index} - SOLD - Balance {StartBal} % Made {(((StartBal/sl)-1)*100)}")'''

			if buy  == 0 and row['RSI'] <= 5 and LastRSI < row['RSI'] and LastClose < row['Close'] and row['AD'] < row['Close'] and row['Close']>LastLB and row['Close']>row['Lower'] and row['Close']<row['Lower1s']:
				sl = StartBal
				Nshares = math.floor(StartBal / row['Close'])
				StartBal -= row['Close'] * Nshares
				buy = 1
				b+=1
				#print(f"{index} - BOUGHT - at {row['Close']} - {Nshares} # of shares")

			LastRSI = row['RSI']
			LastClose = row['Close']
			LastLB = row['Lower']
			LastUB = row['Upper']
			#print(f"stock {stock} time {now} - current price {LastClose} its this clsoe to low bol {row['UBPer']} beg {sl} end {StartBal}  pending {buy} and tr {b}")
		olddata = now
	print(f"total transactions {b} and pending {buy}")
#time.sleep(1)
	Lost = sum(map(lambda x: x< 0,per))
	Won = sum(map(lambda x: x> 0,per))
	perwon = (Won/len(per)*100)
	print(perwon)
	print(sum(per))
	print(sl)
	