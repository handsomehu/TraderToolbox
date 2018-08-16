'''
Created on Aug 16, 2018
Automatic update Dual Thrust intraday singal using tushare
@author: I038825 Leon Zhao
'''
import sys
import pandas as pd
import csv
import tushare as ts
import datetime as dt
import talib as tl
from dt_cons import code_params,fakecode

todayopen = 0
rangehigh = 0
rangelow = 0 
ranghighclose = 0
rangelowclose = 0

params = code_params
cons = ts.get_apis()
wday= dt.datetime.now().weekday()
wday = wday + 1 # change monday from 0 to 1
if wday == 5 :
    wday = 0
else:
    pass
#dt.now().strftime("%w")
#get index futures date from 10 days before to initial data
n_days_before = dt.datetime.now() - dt.timedelta(days=50)
datestr = n_days_before.strftime("%Y-%m-%d")
df_init = ts.bar(fakecode, conn=cons, asset='X', start_date=datestr, end_date='')
df_init = df_init.sort_index(ascending=True)

high = df_init["high"].values
open = df_init["open"].values
low =  df_init["low"].values
close = df_init["close"].values
df_init["atr"] = tl.ATR(high,low, close,20)
df_init["atr"]
df_init["atr"] = df_init["atr"].shift(wday)
df_init["atr"]

df_init["todayopen"] = df_init["open"]
df_init["rangehigh"] = tl.MAX(high,5)
df_init["rangelow"] =  tl.MIN(low,5)
df_init["highclose"] = tl.MAX(close,5)
df_init["lowclose"]  = tl.MIN(close,5)
#print(df_init.ix[:,["high","buyin"]])

df_init["rangehigh"] = df_init["rangehigh"][-1]
df_init["rangelow"] =  df_init["rangelow"][-1]
df_init["highclose"] = df_init["highclose"][-1]
df_init["lowclose"]  = df_init["lowclose"][-1]
#print(df_init.ix[:,["high","buyin"]])

df_init["r1"] = df_init["rangehigh"]-df_init["lowclose"]
df_init["r2"] = df_init["highclose"]-df_init["rangelow"]

df_init = df_init.iloc[-1:]

r1 = df_init["r1"][0]
r2 = df_init["r2"][0] 
if r1 > r2 :
    df_init["range"] = r1
else:
    df_init["range"] = r2

df_init["longentry"] = df_init["todayopen"] + 0.4*df_init["range"]
df_init["shortentry"] = df_init["todayopen"] - 0.4*df_init["range"]
df_init["longexit"] = df_init["longentry"] -2*df_init["atr"]
df_init["shortexit"] = df_init["longentry"] +2*df_init["atr"]
    

n_days_before = dt.datetime.now() - dt.timedelta(days=50)
datestr = n_days_before.strftime("%Y-%m-%d")
for item in params:
    #print(item)
    #print(params[item]['atr'])
    df = ts.bar(item, conn=cons, asset='X', start_date=datestr, end_date='')

    df = df.sort_index(ascending=True)
    
    
    high = df["high"].values
    open = df["open"].values
    low =  df["low"].values
    close = df["close"].values
    df["atr"] = tl.ATR(high,low, close,20)
    df["atr"]
    df["atr"] = df["atr"].shift(wday)
    df["atr"]
    
    df["todayopen"] = df["open"]
    df["rangehigh"] = tl.MAX(high,5)
    df["rangelow"] =  tl.MIN(low,5)
    df["highclose"] = tl.MAX(close,5)
    df["lowclose"]  = tl.MIN(close,5)
    #print(df.ix[:,["high","buyin"]])
    
    df["rangehigh"] = df["rangehigh"][-1]
    df["rangelow"] =  df["rangelow"][-1]
    df["highclose"] = df["highclose"][-1]
    df["lowclose"]  = df["lowclose"][-1]
    #print(df.ix[:,["high","buyin"]])
    
    df["r1"] = df["rangehigh"]-df["lowclose"]
    df["r2"] = df["highclose"]-df["rangelow"]
    
    df = df.iloc[-1:]

    r1 = df["r1"][0]
    r2 = df["r2"][0] 
    if r1 > r2 :    
        df["range"] = df["r1"]
    else:
        df["range"] = df["r2"]
    
    df["longentry"] = df["todayopen"] + 0.4*df["range"]
    df["shortentry"] = df["todayopen"] - 0.4*df["range"]
    df["longexit"] = df["longentry"] -2*df["atr"]
    df["shortexit"] = df["longentry"] +2*df["atr"]   
    df = df.iloc[-1:]    
    df_init = pd.concat([df_init, df])

filename = ''
if wday == 0:
    filename = 'FriDC.csv'
elif wday == 1:
    filename = 'MonDC.csv'
elif wday == 2:
    filename = 'TuDC.csv'
elif wday == 3:
    filename = 'WenDC.csv'
else:
    filename = 'ThuDC.csv'

    
df_init.to_csv(filename)
sys.exit(0)
#print(params[item])