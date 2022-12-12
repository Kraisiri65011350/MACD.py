import numpy as n
import pandas as p
import matplotlib.pyplot as m
import mplfinance as mpl
import yfinance as yf
from tkinter import *
import tkinter.messagebox

class project :
    def buy_sell(signal) :
        buy=[]
        sell=[]
        flag=-1

        for i in range(0 , len(signal)) :
            # signal['MACD'][i] < signal['Signal'][i] and (signal['D'][i]>80 and  signal['K'][i]>80 and signal['D'][i]>signal['K'][i])
            if signal['MACD'][i] > signal['Signal'][i] or (signal['K'][i]<20 or signal['K'][i]<20 and signal['D'][i]<signal['K'][i]):
                sell.append(n.nan)

                if flag != 1 :
                    buy.append(signal['Close'][i])
                    flag=1
                else :
                    buy.append(n.nan)
            # signal['MACD'][i] > signal['Signal'][i] and (signal['K'][i]<20 and  signal['K'][i]<20 and signal['D'][i]<signal['K'][i])
            elif signal['MACD'][i] < signal['Signal'][i] or (signal['D'][i]>80 or signal['K'][i]>80 and signal['D'][i]>signal['K'][i]):
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

    def set(coi):
        coin = str(coi.get()).upper()

        ticker = yf.Ticker(str(coin)+'-USD')
        data = ticker.history(period='1y')


        if len(data)==0:
              tkinter.messagebox.showerror('Error case','Invalid Input')

        ShortEMA = data.Close.ewm(span=12).mean()
        LongEMA = data.Close.ewm(span=26 ).mean()

        MACD = ShortEMA - LongEMA
        Signal = MACD.ewm(span=9).mean()

        # create new column data
        data["MACD"] = MACD
        data["Signal"] = Signal

        # Adds a "n_high" column with max value of previous 14 periods
        data['n_high'] = data['High'].rolling(14).max()
        # Adds an "n_low" column with min value of previous 14 periods
        data['n_low'] = data['Low'].rolling(14).min()
        # Uses the min/max values to calculate the %k (as a percentage)
        data['K'] = (data['Close'] - data['n_low']) * 100 / (data['n_high'] - data['n_low'])
        # Uses the %k to calculates a SMA over the past 3 values of %k
        data['D'] = data['K'].rolling(3).mean()
        #create point for specify buy-sell
        a = project.buy_sell(data)
        data['Buy Signal'] = a[0]
        data['Sell Signal'] = a[1]
        return data,MACD,Signal    

    def candlegraph(coi) :
        data,MACD,Signal=project.set(coi)
        mpl.plot(data , type='candle')
    def bspoint(coi) :
        data,MACD,Signal=project.set(coi)
        
        m.figure(figsize=(15,25))
        m.scatter(data.index , data['Buy Signal'] , color='green' , label='Up' , marker='^' , alpha=1)
        m.scatter(data.index , data['Sell Signal'] , color='red' , label='Down' , marker='v' , alpha=1)

        m.plot(data['Close'] , label='CLose Price' ,alpha=0.35)

        m.title('Up and Down Trend on Short Period')
        m.xlabel('Date')
        m.ylabel('Close price in $')
        m.legend(loc='upper right')
        m.show()    
        
    def bspointandindicator(coi) :
        data,MACD,Signal=project.set(coi)
        
        m.figure(figsize=(15,25))
        m.scatter(data.index , data['Buy Signal'] , color='green' , label='Up' , marker='^' , alpha=1)
        m.scatter(data.index , data['Sell Signal'] , color='red' , label='Down' , marker='v' , alpha=1)

        m.plot(data['Close'] , label='CLose Price' ,alpha=0.35)
        m.plot(data.index , MACD , label='MACD' , color='m',linewidth=0.7) 
        m.plot(data.index , Signal , label="Signal line" , color='b',linewidth=0.7)
        m.plot(data.index , data['K'] , label='Pencentage K' , color='r',linewidth=0.7) 
        m.plot(data.index , data['D'] , label="Pencentage D" , color='c',linewidth=0.7)

        m.title('Up and Down Trend on Short Period')
        m.xlabel('Date')
        m.ylabel('Close price in $')
        m.legend(loc='upper right')
        m.show()  

    def delt(lab) :
        lab.delete(0,END)

    def gui():
        root = Tk()
        root.geometry('660x150+400+300')
        root.title('My project')

        coi = StringVar()
        lab = Entry(root,textvariable=coi,font=50,bg='cyan')
        lab.grid(row=0,column=0,columnspan=10)

        a = Button(root,text='show candle graph',command=lambda:project.candlegraph(coi),padx=7,pady=7,font=30,bg='green')
        a.grid(row=1,column=0)
        b = Button(root,text='buy-sell point',command=lambda:project.bspoint(coi),padx=7,pady=7,font=30)
        b.grid(row=1,column=1)
        c = Button(root,text='buy-sell point & Indicator',command=lambda:project.bspointandindicator(coi),padx=7,pady=7,font=30,bg='yellow')
        c.grid(row=1,column=2)
        d = Button(root,text='clear',command=lambda:project.delt(lab),padx=7,pady=7,font=30,bg='red')
        d.grid(row=1,column=3)
        root.mainloop()
    
    

project.gui()    


