# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 09:18:37 2016

@author: ZFang
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import pandas as pd


def setup_driver():
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    return driver  

    
if __name__ == '__main__':
    url = 'https://www.hedgefundresearch.com/family-indices/hfrx'
    driver = setup_driver()
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source,'lxml')
    
    
    table = soup.find_all('div',attrs={'class':'data-table-wrapper'})
    data = []
    for t_ in table:
        rows = t_.find_all('tr')
        for r_ in rows:
            cols = r_.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
    df = pd.DataFrame([part for part in data])    
    df.columns = ['Index Name','DTD','MTD','YTD','Index Value','Recent Month_1','Recent Month_2','YTD','Last 12M','Last 36M']
           
            
    