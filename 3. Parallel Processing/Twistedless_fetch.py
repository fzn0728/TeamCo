# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 08:40:18 2016

@author: ZFang
"""

from urllib import parse
from urllib.request import urlopen
from threading import Thread
import http.client, sys
from queue import Queue
import pandas as pd
import os

os.chdir('C:\\Users\\ZFang\\Desktop\\TeamCo\\URLfetch\\urlfetch')

concurrent = 200

def doWork():
    while True:
        url = q.get()
        ourl, l = fetch(url)
        print(url)
        q.task_done()

def fetch(ourl):
    try:
        l = urlopen(ourl, timeout=60).read()
        return ourl, l
    except:
        return "error", ourl


    
ticker = pd.ExcelFile('tickerlist.xlsx')
ticker_df = ticker.parse(str(ticker.sheet_names[0]))
ticker_list = list(ticker_df['Ticker'])[0:10]

q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for ticker in ticker_list:
        url = 'http://finance.yahoo.com/quote/' + ticker
        q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)