'''
Created on Aug 9, 2018

@author: I038825
'''
import tushare as ts

cons = ts.get_apis()

df = ts.bar('CU1810', conn=cons, asset='X', start_date='2018-07-01', end_date='')
print(df.head(5))