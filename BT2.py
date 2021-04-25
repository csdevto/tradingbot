import time, datetime, math
from datetime import datetime, timedelta
import MarketData as MD


#stock to test
stocks = ['UBER']

#set parameters to start
#trading balance


per=[]

for stock in stocks:
	StartBalance = 1000
	PrevBalance = StartBalance
	NumShares = CurrentTime = buy = RSI = Transactions = TimeTillClosing = LastCheck = LastBBU = LastRSI = 0
	LastLBPer = LastUBPer = LastClose = 10000000
	data = MD.getmarket('DB',stock,90)
	
	#data = data[data.index.strftime('%Y-%m-%d') == '2021-04-23']
	#print(data)
	#print(data)
	for index, row in data.iterrows():
		timestr = '15:57:00'
		CurrentTime = index
		Close = row['close']
		RSI = row['RSI_14']
		BBU = row['BBU']
		UBPer = row['UBPer']
		BBL = row['BBL']
		LBPer = row['LBPer']
		if CurrentTime != LastCheck:
			current_time = CurrentTime.strftime("%H:%M:%S")
			ftr = [3600,60,1]
			TimeTillClosing= sum([a*Transactions for a,Transactions in zip(ftr, map(int,timestr.split(':')))]) - sum([a*Transactions for a,Transactions in zip(ftr, map(int,current_time.split(':')))])
			TStop = 0
			if TimeTillClosing<0:
				#determines if time is 3:57 and sells the position
				TStop = 1
			
			if buy == 1 and RSI >= 70 and LastClose < Close  and BBU < Close:
				StartBalance += Close * NumShares
				NumShares = 0
				buy = 0
				per.append((((StartBalance/PrevBalance)-1)*100))
				print(f"{index} - SOLD - Balance {StartBalance} % Made {(((StartBalance/PrevBalance)-1)*100)}")

			if buy  == 0 and RSI <= 30 and LastClose < Close and LastBBL < LastClose and BBL < Close:
				PrevBalance = StartBalance
				NumShares = math.floor(StartBalance / Close)
				StartBalance -= Close * NumShares
				buy = 1
				Transactions+=1
				print(f"{index} - BOUGHT - at {Close} - {NumShares} # of shares")
			#print(f"stock {stock} time {CurrentTime} - current price {LastClose} its this clsoe to low bol {UBPer} beg {PrevBalance} end {StartBalance}  pending {buy} and tr {Transactions} --- Last Upper BL {LastBBU}  current Up {BBU}")
			
			#Store Previous datetime info to compare
			LastRSI = RSI
			LastClose = Close
			LastBBL = BBL
			LastLBPer = LBPer
			LastBBU = BBU
			LastUBPer = UBPer

		LastCheck = CurrentTime
	##MODIFY ISSUE PERWON
	print(f"total transactions {Transactions} and pending {buy}")
	#time.sleep(2)
	Lost = sum(map(lambda x: x< 0,per))
	Won = sum(map(lambda x: x> 0,per))
	print(sum(per))
	print(StartBalance)
