import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time
stock = 'FB'


#Interval required 5 minutes
data = yf.download(tickers='UBER', period='5d', interval='1m')

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

data = data[data.index.strftime('%Y-%m-%d') == '2021-02-25']
#Print data
print(data[['Close','Upper','AD']])

data[['Close','MA20','Upper','Lower','Upper1s','Lower1s','AD']].plot(figsize=(10,4))
plt.grid(True)
plt.title(stock + ' Bollinger Bands')
plt.axis('tight')
plt.ylabel('Price')
plt.show()
data[['AD']].plot(figsize=(10,4))
plt.grid(True)
plt.title(stock + ' Bollinger Bands')
plt.axis('tight')
plt.ylabel('Price')
plt.show()
