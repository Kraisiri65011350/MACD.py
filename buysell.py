# the program uses the moving average convergence/divergence (MACD) crossover

import numpy as n
import pandas as p
import matplotlib.pyplot as m
import mplfinance as mpl
import yfinance as yf

# m.style.use('fivethirtyeight')

a=input('enter crypto : ').upper()

# import data
ticker = yf.Ticker(a+'-USD')
data = ticker.history(period='1y')

# plot close price as graph
# m.figure(figsize=(15,25))
# m.plot(data['Close'] , label='Close')
# m.title('close price history')
# m.xlabel('date')
# m.ylabel('price is US dollar')
# m.show()

#calculae EMA , MACD 
ShortEMA = data.Close.ewm(span=12).mean()
LongEMA = data.Close.ewm(span=26 ).mean()

MACD = ShortEMA - LongEMA
Signal = MACD.ewm(span=9).mean()

# m.figure(figsize=(15,25))
# m.plot(data.index , MACD , label=a+' MACD' , color='r')
# m.plot(data.index , Signal , label="Signal line" , color='b')
# m.legend(loc='lower right')
# m.show()


# create new column data
data["MACD"] = MACD
data["Signal"] = Signal



#create point for specify buy-sell

def buy_sell(signal) :
    buy=[]
    sell=[]
    flag=-1

    for i in range(0 , len(signal)) :
        if signal['MACD'][i] > signal['Signal'][i] :
            sell.append(n.nan)

            if flag != 1 :
                buy.append(signal['Close'][i])
                flag=1
            else :
                buy.append(n.nan)
        elif signal['MACD'][i] < signal['Signal'][i] :
            buy.append(n.nan)
            if flag != 0 :
                sell.append(signal["Close"][i])
                flag=0
            else :
                sell.append(n.nan)
        else :
            buy.append(n.nan)
            sell.append(n.nan)
    return (buy , sell)

a = buy_sell(data)
data['Buy Signal'] = a[0]
data['Sell Signal'] = a[1]

print(data)

mpl.plot(data , type='candle')

m.figure(figsize=(15,25))
m.scatter(data.index , data['Buy Signal'] , color='green' , label='buy' , marker='^' , alpha=1)
m.scatter(data.index , data['Sell Signal'] , color='red' , label='sell' , marker='v' , alpha=1)

m.plot(data['Close'] , label='CLose Price' ,alpha=0.35)
m.plot(data.index , MACD , label='MACD' , color='m',linewidth=0.7) 
m.plot(data.index , Signal , label="Signal line" , color='b',linewidth=0.7)

m.title('close price buy and sell')
m.xlabel('Date')
m.ylabel('Close price in $')
m.legend(loc='upper right')
m.show()

