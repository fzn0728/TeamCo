# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 10:28:54 2016

@author: ZFang
"""

import pandas_datareader.data as wb
import os
import pandas as pd
import time

os.chdir('C:\\Users\\ZFang\\Desktop\\TeamCo\\URLfetch\\urlfetch')
ticker = pd.ExcelFile('tickerlist.xlsx')
ticker_df = ticker.parse(str(ticker.sheet_names[0]))
ticker_list = list(ticker_df['Ticker'])
ticker_list[585] = 'True'

start = time.time()
result = wb.get_quote_google(ticker_list[0])
for i in range(1,len(ticker_list)-1000,1000):    
    quote = wb.get_quote_yahoo(ticker_list[i:i+1000])
    result = pd.concat([result,quote])
print('The total time is %s' %str(time.time()-start))