import pandas as pd
import yfinance as yf
import time, datetime
from datetime import datetime, timedelta
import sqlite3
import pandas_ta as ta

con = sqlite3.connect("DB/stocks.db")
def getmarket(loc,ticker,days):
    data = ""
    DataPeriod = days
    if(loc == "YF"):
        DataPeriod = str(DataPeriod) + "d"
        data = yf.download(tickers=ticker, period=DataPeriod, interval='1m',progress=False)
    if(loc =="DB"):
        DataPeriod = datetime.today()-timedelta(days=DataPeriod)
        data = pd.read_sql_query("SELECT * FROM stocks_hist WHERE symbol='" + ticker + "' AND Datetime >= '" + DataPeriod.strftime("%Y-%m-%d") + "' ORDER BY Datetime ASC",con,index_col='Datetime')
    
    #Make Pulled data indexed by date and sorted ASC
    data.index = pd.to_datetime(data.index)
    data=data.sort_index()
    
    #Parameters for Strategy
    
    TradingStrategy = ta.Strategy(
        name="Bands",
        description="BBands and RSI",
        ta=[
            {"kind": "bbands", "length": 20,"col_names": ("BBL", "BBM", "BBU","BBB")},
            {"kind": "rsi","col_names": ("RSI")},
        ]
    )
    data.ta.strategy(TradingStrategy)
    data['LBPer']=(data['close']/data['BBL'])-1
    data['UBPer']=(data['BBU']/data['close'])-1
    return data