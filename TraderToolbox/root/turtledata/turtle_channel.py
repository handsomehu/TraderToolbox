'''
Created on Aug 9, 2018
Automatic update turtle signal using tushare
@author: I038825 Leon Zhao
'''
import sys
import pandas as pd
import csv
import tushare as ts
import datetime as dt
import talib as tl
from turtle_cons import code_params,fakecode

params = code_params
cons = ts.get_apis()
wday= dt.datetime.now().weekday()
wday = wday + 1 # change monday from 0 to 1
if wday == 5 :
    wday = 0
else:
    pass
#dt.now().strftime("%w")
#get date from 90 days before to get data
n_days_before = dt.datetime.now() - dt.timedelta(days=10)
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
df_init["buyin"] = tl.MAX(high,20)
df_init["sellin"] = tl.MIN(high,20)
df_init["buyexit"] = tl.MIN(high,10)
df_init["sellexit"] = tl.MAX(high,10)
#print(df_init.ix[:,["high","buyin"]])

df_init = df_init.iloc[-1:]

n_days_before = dt.datetime.now() - dt.timedelta(days=90)
datestr = n_days_before.strftime("%Y-%m-%d")
for item in params:
    #print(item)
    #print(params[item]['atr'])
    df = ts.bar(item, conn=cons, asset='X', start_date=datestr, end_date='')

    df = df.sort_index(ascending=True)
    high = df["high"].values
    open = df["open"].values
    low  = df["low"].values
    close = df["close"].values
    df["atr"] = tl.ATR(high,low, close,params[item]['atr'])
    df["atr"] = df["atr"].shift(wday)
    df["buyin"] = tl.MAX(high,params[item]['li'])
    df["sellin"] = tl.MIN(low,params[item]['si'])
    df["buyexit"] = tl.MIN(low,params[item]['le'])
    df["sellexit"] = tl.MAX(high,params[item]['se'])    
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
