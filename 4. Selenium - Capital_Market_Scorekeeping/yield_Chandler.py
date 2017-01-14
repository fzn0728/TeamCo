# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 12:25:43 2016

@author: ZFang
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import pandas as pd
from selenium.webdriver.support.ui import Select


def setup_driver():
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    return driver  

    
if __name__ == '__main__':
    url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'
    driver = setup_driver()
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source,'lxml')
    
    
    table = soup.find_all('table',attrs={'class':'t-chart'})
    data = []
    for t_ in table:
        rows = t_.find_all('tr')
        for r_ in rows:
            cols = r_.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
    df = pd.DataFrame([part for part in data])    
    df.columns = ['Date','1 Mo','3 Mo','6 Mo','1 Yr','2 Yr','3 Yr','5 Yr','7 Yr','10 Yr','20 Yr','30 Yr']
    # Part 2
    select = Select(driver.find_element_by_id('interestRateTimePeriod'))
    select.select_by_visible_text('2016')       
#    opt = driver.find_element_by_id('interestRateTimePeriod')
#    opt.click()
#    for option in opt.find_elements_by_tag_name('option'):
#        if option.text == '2016':
#            option.click()
            
    # select = Select(driver.find_element_by_id('interestRateTimePeriod')).select_by_visible_text('2016').click()     
    # select = Select(driver.find_element_by_id('interestRateTimePeriod')).select_by_value('TextView.aspx?data=yieldYear&amp;year=2016').click()
    # driver.find_element_by_xpath("//select[@id='interestRateTimePeriod']/option[@value='TextView.aspx?data=yieldYear&amp;year=2016']").click()
    # driver.find_element_by_css_selector("select#interestRateTimePeriod > option[value='TextView.aspx?data=yieldYear&amp;year=2016']").click()