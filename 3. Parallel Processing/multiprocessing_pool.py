# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 09:02:05 2016

@author: ZFang
"""

from multiprocessing import Pool
import requests
# from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import queue

os.chdir('C:\\Users\\ZFang\\Desktop\\TeamCo\\URLfetch\\urlfetch')


def fetch_url(x):
    myurl = ("http://finance.yahoo.com/q/cp?s=%s" % x)
    html = str(requests.get(myurl).content)
    #soup = BeautifulSoup(html,'lxml')
    listOut = [x, html]
    return listOut

tickDF = pd.read_excel('short_tickerlist.xlsx')
li = tickDF['Ticker'].tolist()


start = time.time()

if __name__ == '__main__':
    q = queue.Queue()
    p = Pool(7)
    output = p.map_async(fetch_url,li,chunksize=28)
    while not output.ready():
        print("Number of ticker left {0}".format((output._number_left)*28))
        time.sleep(1)
    result = output.get()
    p.close()
    p.join()
    print("Time is %ss" %(time.time()-start))
