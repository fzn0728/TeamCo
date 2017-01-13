# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 16:04:17 2016

@author: ZFang
"""





from urllib.request import urlopen
import json
from datetime import datetime, timedelta
import dateutil.relativedelta
import numpy as np
import pandas as pd


def currency_get_data(date):
    
    url = "http://api.fixer.io/%s?base=USD"%date
    response = urlopen(url)
    data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    return data

current_date = datetime.today() - timedelta(days=1)
one_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=1)
three_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=3)
six_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=6)
twelve_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=12)

current_date = current_date.strftime('%Y-%m-%d')
one_month_delta = one_month_delta.strftime('%Y-%m-%d')
three_month_delta = three_month_delta.strftime('%Y-%m-%d')
six_month_delta = six_month_delta.strftime('%Y-%m-%d')
twelve_month_delta = twelve_month_delta.strftime('%Y-%m-%d')


Currency_df = pd.DataFrame(np.zeros([3,5]),columns=['Spot','MTD','3 Month Change','6 Month Change','1 Year Change'],index=['USD/GBP','USD/EUR','JPY/USD'])


data_c = currency_get_data(current_date)
Currency_df.iloc[0,0]=1/data_c['rates']['GBP']
Currency_df.iloc[1,0]=1/data_c['rates']['EUR']
Currency_df.iloc[2,0]=data_c['rates']['JPY']

data_one = currency_get_data(one_month_delta)
Currency_df.iloc[0,1]=(1/data_one['rates']['GBP']-Currency_df.iloc[0,0])/Currency_df.iloc[0,0]
Currency_df.iloc[1,1]=(1/data_one['rates']['EUR']-Currency_df.iloc[1,0])/Currency_df.iloc[1,0]
Currency_df.iloc[2,1]=(data_one['rates']['JPY']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]

data_three = currency_get_data(three_month_delta)
Currency_df.iloc[0,2]=(1/data_three['rates']['GBP']-Currency_df.iloc[0,0])/Currency_df.iloc[0,0]
Currency_df.iloc[1,2]=(1/data_three['rates']['EUR']-Currency_df.iloc[1,0])/Currency_df.iloc[1,0]
Currency_df.iloc[2,2]=(data_three['rates']['JPY']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]

data_six = currency_get_data(six_month_delta)
Currency_df.iloc[0,3]=(1/data_six['rates']['GBP']-Currency_df.iloc[0,0])/Currency_df.iloc[0,0]
Currency_df.iloc[1,3]=(1/data_six['rates']['EUR']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]
Currency_df.iloc[2,3]=(data_six['rates']['JPY']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]

data_twe = currency_get_data(twelve_month_delta)
Currency_df.iloc[0,4]=(1/data_twe['rates']['GBP']-Currency_df.iloc[0,0])/Currency_df.iloc[0,0]
Currency_df.iloc[1,4]=(1/data_twe['rates']['EUR']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]
Currency_df.iloc[2,4]=(data_twe['rates']['JPY']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]