import matplotlib.pyplot as plt
import time, datetime, math
from datetime import datetime, timedelta
import sqlite3
import MarketData as MD

stock = 'UBER'

data = MD.getmarket('DB',stock,2)

data[['close','RSI_14','BBL','BBU']].plot(figsize=(10,4))
plt.grid(True)
plt.title(stock + ' AD')
plt.axis('tight')
plt.ylabel('Price')
plt.show()