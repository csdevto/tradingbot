import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time, datetime, math
from datetime import datetime
import sqlite3


#Interval required 5 minutes
con = sqlite3.connect("DB/stocks.db")
#con.row_factory = sqlite3.Row
stock = 'UBER'
data = pd.read_sql_query("SELECT * FROM stocks_hist WHERE symbol='" + stock + "' AND Datetime >= '2021-04-22' ORDER BY Datetime DESC limit 10000 ",con,index_col='Datetime')
data.index = pd.to_datetime(data.index)
data= data.sort_index()
print(data)

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



#Bollinger bands, 1 std and 2 std 
data['MA20'] = data['Close'].rolling(window=20).mean()
data['20dSTD'] = data['Close'].rolling(window=20).std()
data['Upper'] = data['MA20'] + (data['20dSTD'] * 2)
data['Lower'] = data['MA20'] - (data['20dSTD'] * 2)
'''data['Upper1s'] = data['MA20'] + (data['20dSTD'] * 1)
data['Lower1s'] = data['MA20'] - (data['20dSTD'] * 1)
data['LBPer']=(data['Close']/data['Lower'])-1
data['UBPer']=(data['Upper']/data['Close'])-1
data['UBPer1s']=(data['Close']/data['Upper1s'])-1'''

data['AD'] = 0
#ADL Line
data['CMFV'] = (((data['Close']-data['Low'])-(data['High']-data['Close']))/(data['High']-data['Low']))*data['Volume']
data['AD'] = data['CMFV'].rolling(14, min_periods=14).sum()
data['AD'] = data['AD'].shift(1)

data['RSI'] = 100.0 - (100.0 / (1.0 + RS))
#data = data[data.index.strftime('%Y-%m-%d') == '2021-02-27']
#Print data
print(data)

'''data[['Close','AD']].plot(figsize=(10,4))
plt.grid(True)
plt.title(stock + ' AD')
plt.axis('tight')
plt.ylabel('Price')
plt.show()'''

