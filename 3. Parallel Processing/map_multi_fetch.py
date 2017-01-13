# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 09:33:22 2016

@author: ZFang
"""
import os
import pandas as pd
from urllib.request import urlopen
import time

os.chdir('C:\\Users\\ZFang\\Desktop\\TeamCo\\URLfetch\\urlfetch')

start = time.time()


ticker = pd.ExcelFile('tickerlist.xlsx')
ticker_df = ticker.parse(str(ticker.sheet_names[0]))
ticker_list = list(ticker_df['Ticker'])[0:10]




def fetch(ticker):
    result = []
    url = 'http://finance.yahoo.com/quote/' + ticker
    result.append(ticker)
    result.append(urlopen(url).read())
    print(url+' fetching...... ' + str(time.time()-start))
    return result
    
    
l = []
for t in map(fetch, ticker_list):
    l.append(list(t))
    
    
    
