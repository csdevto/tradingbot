import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
import time
stock = 'EARK.NE'
#Interval required 5 minutes
while True:
	data = yf.download(tickers='EARK.NE', period='5d', interval='1m')
	data['MA20'] = data['Close'].rolling(window=20).mean()
	data['20dSTD'] = data['Close'].rolling(window=20).std()
	data['Upper'] = data['MA20'] + (data['20dSTD'] * 2)
	data['Lower'] = data['MA20'] - (data['20dSTD'] * 2)

	dt = pd.DataFrame(data=data[['Close','Upper','Lower','MA20']])
	t1=dt.tail(n=1)
	if (t1['Close'].values-t1["Lower"].values) > 0 and (t1['Close'].values-t1['MA20'].values) > 0:
		print('buy')
	time.sleep(60)