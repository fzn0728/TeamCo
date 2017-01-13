# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 15:55:22 2016

@author: ZFang
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import pandas as pd

def setup_driver():
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    return driver  

    


if __name__ == '__main__':
    driver = setup_driver()
    url = 'http://us.spindices.com/indices/equity/sp-500'
    driver.get(url)
    time.sleep(5)
    driver.find_element_by_class_name('table ').click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source,'lxml')    
    table = soup.find('table',attrs={'class':'daily-return-table'})
    rows = table.find_all('tr')
    data = []
    for t_ in rows:
        cols = t_.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    df = pd.DataFrame([part for part in data])
    df.columns = ['Index','Index Level','1 Day','MTD','QTD','YTD']