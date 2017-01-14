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
from fredapi import Fred
from datetime import datetime, timedelta
import dateutil.relativedelta
import numpy as np

if __name__ == '__main__':
    
    fred = Fred(api_key='a0718ea00e6784c5f8b452741622a98c')
    current_date = datetime.today() - timedelta(days=1)
    one_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=1)
    three_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=3)
    six_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=6)
    twelve_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=12)
    today = current_date.strftime('%m/%d/%Y')
    
    ### Get value
    Treasury_10Y = pd.DataFrame(fred.get_series('DGS10',observation_start=today))
    Treasury_10_1M = pd.DataFrame(fred.get_series('DGS10',observation_start=one_month_delta))
    Treasury_10_3M = pd.DataFrame(fred.get_series('DGS10',observation_start=three_month_delta))
    Treasury_10_6M = pd.DataFrame(fred.get_series('DGS10',observation_start=six_month_delta))
    Treasury_10_12M = pd.DataFrame(fred.get_series('DGS10',observation_start=twelve_month_delta))
    
    Treasury_30Y = pd.DataFrame(fred.get_series('DGS30',observation_start=today))
    Treasury_30_1M = pd.DataFrame(fred.get_series('DGS30',observation_start=one_month_delta))
    Treasury_30_3M = pd.DataFrame(fred.get_series('DGS30',observation_start=three_month_delta))
    Treasury_30_6M = pd.DataFrame(fred.get_series('DGS30',observation_start=six_month_delta))
    Treasury_30_12M = pd.DataFrame(fred.get_series('DGS30',observation_start=twelve_month_delta))
    
    
    # Collect them into the dataframe
    Bond_Yield_df = pd.DataFrame(np.zeros([4,5]),columns=['Yield','MTD','3 Month Change','6 Month Change','1 Year Change'],index=['10-Year Treasury Note','30-Year Treasury Note','10-Year AA Corporates','20-Year AA Corporates'])
    Bond_Yield_df.iloc[0,0] = Treasury_10Y.iloc[0,0]
    Bond_Yield_df.iloc[0,1] = Treasury_10_1M.iloc[0,0]
    Bond_Yield_df.iloc[0,2] = Treasury_10_3M.iloc[0,0]
    Bond_Yield_df.iloc[0,3] = Treasury_10_6M.iloc[0,0]
    Bond_Yield_df.iloc[0,4] = Treasury_10_12M.iloc[0,0]

    Bond_Yield_df.iloc[1,0] = Treasury_30Y.iloc[0,0]
    Bond_Yield_df.iloc[1,1] = Treasury_30_1M.iloc[0,0]
    Bond_Yield_df.iloc[1,2] = Treasury_30_3M.iloc[0,0]
    Bond_Yield_df.iloc[1,3] = Treasury_30_6M.iloc[0,0]
    Bond_Yield_df.iloc[1,4] = Treasury_30_12M.iloc[0,0]

