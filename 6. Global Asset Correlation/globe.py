# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 09:44:31 2016

@author: ZFang


1- change currency order
2- refine YTD MTD QTD return
3- change the format value(return)


"""
from datetime import datetime
import pandas_datareader.data as wb
from fredapi import Fred
import pandas as pd
import numpy as np
from itertools import groupby
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime, timedelta
import plotly.plotly as py
from plotly.graph_objs import *
import dateutil.relativedelta
import urllib.request
import ast
import math
import string


    
def equity_price_MTD_QTD_YTD(tickerlist):
    last_day = datetime.today()-dateutil.relativedelta.relativedelta(days=1)
    last_last_day = pd.date_range(end=last_day, periods=2, freq='B')[0].to_datetime()
    last_month = pd.date_range(end=last_day, periods=1, freq='BM')[0].to_datetime()
    last_quarter = pd.date_range(end=last_day, periods=1, freq='BQ')[0].to_datetime()
    last_year = pd.date_range(end=last_day, periods=1, freq='BA')[0].to_datetime()
    
    # get all datetime
    # end = datetime.today()-dateutil.relativedelta.relativedelta(days=1)
    # last_day = datetime.today()-dateutil.relativedelta.relativedelta(days=1)
    # last_last_day = datetime.today()-dateutil.relativedelta.relativedelta(days=2)
    # last_month = datetime.today().replace(day=1)-dateutil.relativedelta.relativedelta(days=1)
    # q = math.ceil(datetime.today().month/3)-1
    # last_quarter = datetime.today().replace(month=q*3+1,day=1)-dateutil.relativedelta.relativedelta(days=1)
    # last_year = datetime.today().replace(month=1,day=1)-dateutil.relativedelta.relativedelta(days=1)
    # start = last_year - dateutil.relativedelta.relativedelta(days=1)
    date_list = [last_day,last_last_day,last_month,last_quarter,last_year]
    # pull the data
    
    # collect a new dataframe for return calculation
    price_cal_df= pd.DataFrame([])
    for d in date_list:
        price_cal_df = pd.concat([price_cal_df,check_empty(tickerlist,d)])
        
    # price_cal_df = price_cal_df.interpolate()
    # Change column name
    price_cal_df = add_column_name(price_cal_df)
    return price_cal_df  
    
    
    
def add_column_name(dataframe):
    l = []
    for i in dataframe.columns:
        l.append(ticker_dict[i])
    dataframe.columns = l
    return dataframe    
    
def equity_return_MTD_QTD_YTD(df):
    return_df = pd.DataFrame(np.zeros([5,9]),index=['T','DTD','MTD','QTD','YTD'],columns=df.columns)
    return_df.iloc[0,:] = round(100*(df.iloc[0,:]-df.iloc[0,:])/df.iloc[0,:],2)
    return_df.iloc[1,:] = round(100*(df.iloc[0,:]-df.iloc[1,:])/df.iloc[1,:],2)
    return_df.iloc[2,:] = round(100*(df.iloc[0,:]-df.iloc[2,:])/df.iloc[2,:],2)
    return_df.iloc[3,:] = round(100*(df.iloc[0,:]-df.iloc[3,:])/df.iloc[3,:],2)
    return_df.iloc[4,:] = round(100*(df.iloc[0,:]-df.iloc[4,:])/df.iloc[4,:],2)
    return return_df
    
    
def check_empty(tickerlist,date):
    i = 1
    price = wb.DataReader(tickerlist,'yahoo',date,date)['Adj Close']    
    while price.isnull().values.any() or price.empty:
        if price.empty:
            print('Go empty table one')
            target = price.columns
            for i in target:
                print('Start %s'%i)
                j=0
                while price[i].empty:
                    try:
                        j=j+1
                        print('Try j is %d'%j)
                        print('The i is %s'%i)
                        price.loc[0,i] = wb.DataReader(i,'yahoo',date-dateutil.relativedelta.relativedelta(days=j),\
                                    date-dateutil.relativedelta.relativedelta(days=j))['Adj Close'].values[0]
                    except:
                        price.loc[0,i] = None                  
        else:
            print('Go isnull one')
            target = price.columns[price.isnull().values[0]]
            for i in target:
                print('Start %s'%i)
                j=0
                while price[i].isnull().values[0]:
                    try:
                        j=j+1
                        price[i] = wb.DataReader(i,'yahoo',date-dateutil.relativedelta.relativedelta(days=j),\
                                    date-dateutil.relativedelta.relativedelta(days=j))['Adj Close'].values[0]
                    except:
                        price[i]= None      
    price.index = [date]
    price = price.convert_objects(convert_numeric=True)
    return price
    
    
    
    # wb.DataReader('^AORD','yahoo',date_list[2]-dateutil.relativedelta.relativedelta(days=j),\
                  # date_list[2]-dateutil.relativedelta.relativedelta(days=j))['Adj Close'].values[0]
                  
    
    # price = wb.DataReader(globe_equity_index_list,'yahoo',date_list[2],date_list[2])['Adj Close']  
    # check_empty(globe_equity_index_list,date_list[2])
    # wb.DataReader('N225','yahoo',date_list[0],date_list[0])['Adj Close']
    
    
    
def currency_price_MTD_QTD_YTD():
    # get all datetime
    last_day = datetime.strftime(datetime.today()-dateutil.relativedelta.relativedelta(days=1),'%Y-%m-%d')
    last_last_day = datetime.strftime(datetime.today()-dateutil.relativedelta.relativedelta(days=2),'%Y-%m-%d')
    last_month = datetime.strftime(datetime.today().replace(day=1)-dateutil.relativedelta.relativedelta(days=1),'%Y-%m-%d')
    q = math.ceil(datetime.today().month/3)-1
    last_quarter = datetime.strftime(datetime.today().replace(month=q*3+1,day=1)-dateutil.relativedelta.relativedelta(days=1),'%Y-%m-%d')
    last_year = datetime.strftime(datetime.today().replace(month=1,day=1)-dateutil.relativedelta.relativedelta(days=1),'%Y-%m-%d')
    date_list = [last_day,last_last_day,last_month,last_quarter,last_year]

    # Pull the data and do return calculation
    currency_df = pd.DataFrame([])
    for i in range(len(date_list)):
        with urllib.request.urlopen('http://api.fixer.io/%s?base=USD' %date_list[i]) as f:
            currency_dict = ast.literal_eval(f.read().decode('utf-8'))
            currency_df = pd.concat([currency_df,pd.DataFrame.from_dict(currency_dict['rates'],'index')], axis=1)
    currency_df.columns = ['Last_Day','Last_Last_Day','Last_Month','Last_Quarter','Last_Year']
    currency_df['dtd'] = round((currency_df['Last_Day']-currency_df['Last_Last_Day'])/currency_df['Last_Last_Day'],4)
    currency_df['mtd'] = round((currency_df['Last_Day']-currency_df['Last_Month'])/currency_df['Last_Month'],4)
    currency_df['qtd'] = round((currency_df['Last_Day']-currency_df['Last_Quarter'])/currency_df['Last_Quarter'],4)
    currency_df['ytd'] = round((currency_df['Last_Day']-currency_df['Last_Year'])/currency_df['Last_Year'],4)
    
    return currency_df
    


       
if __name__ == '__main__':
    globe_equity_index_list = ['^GSPC','^N225','^SSEC','^FTSE','^HSI','^BVSP','^AORD','^GDAXI','^BSESN']    
    ticker_dict = {'FXY':'JPY/USD','FXB':'GBP/USD','FXE':'EUR/USD','FXA':'AUD/USD','FXCH':'CHY/USD','BZF':'BRL/USD',
         '^GSPC':'S&P500','^N225':'Nikki_225','^SSEC':'SSE_Composite','^FTSE':'FTSE_100','^HSI':'HANG_SENG_INDEX',\
         '^BVSP':'IBOVESPA','^AORD':'ALL_ORDINARIES','^GDAXI':'DAX','^BSESN':'S&P_BSE_SENSEX',\
         'XLY':'Consumer Discretionary','XLP':'Consumer Staples','XLE':'Energy','XLF':'Financials',\
         'XLV':'Health Care','XLI':'Industrials','XLB':'Materials','XLRE':'Real Estate','XLK':'Technology','XLU':'Utilities'}
         

    ###### Equity Index Return ######
    print('It starts')
    zzz = equity_price_MTD_QTD_YTD(globe_equity_index_list)
    print('It ends')
    zzz_df = equity_return_MTD_QTD_YTD(zzz)
    zzz_str =  zzz_df.applymap(str)

    ###### Currency ######     
    currency_df = currency_price_MTD_QTD_YTD() 
        
    ###### Concat the data ######      
    a=[]
    for i,p,j,k,l,m in zip(zzz.columns,zzz.iloc[0,:],zzz_str.ix['DTD'],zzz_str.ix['MTD'],zzz_str.ix['QTD'],zzz_str.ix['YTD']):
        a.append(i+': '+str(round(p,2))+'('+j+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+k+'%/'+l+'%/'+m+'%')
    a[0] = a[0]+'<br>'+'AUD/USD: '+str(round(1/currency_df.loc['AUD','Last_Day'],2))+'('+str(-100*currency_df.loc['AUD','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(-100*currency_df.loc['AUD','mtd'])+'%/'+str(-100*currency_df.loc['AUD','qtd'])+'%/'+str(-100*currency_df.loc['AUD','ytd'])+'%'
    a[1] = a[1]+'<br>'+'USD/INR: '+str(round(currency_df.loc['INR','Last_Day'],2))+'('+str(100*currency_df.loc['INR','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['INR','mtd'])+'%/'+str(100*currency_df.loc['INR','qtd'])+'%/'+str(100*currency_df.loc['INR','ytd'])+'%'
    a[2] = a[2]+'<br>'+'USD/BRL: '+str(round(currency_df.loc['BRL','Last_Day'],2))+'('+str(100*currency_df.loc['BRL','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['BRL','mtd'])+'%/'+str(100*currency_df.loc['BRL','qtd'])+'%/'+str(100*currency_df.loc['BRL','ytd'])+'%'
    a[3] = a[3]+'<br>'+'GBP/USD: '+str(round(1/currency_df.loc['GBP','Last_Day'],2))+'('+str(-100*currency_df.loc['GBP','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(-100*currency_df.loc['GBP','mtd'])+'%/'+str(-100*currency_df.loc['GBP','qtd'])+'%/'+str(-100*currency_df.loc['GBP','ytd'])+'%'
    a[4] = a[4]+'<br>'+'EUR/USD: '+str(round(1/currency_df.loc['EUR','Last_Day'],2))+'('+str(-100*currency_df.loc['EUR','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(-100*currency_df.loc['EUR','mtd'])+'%/'+str(-100*currency_df.loc['EUR','qtd'])+'%/'+str(-100*currency_df.loc['EUR','ytd'])+'%'
    a[6] = a[6]+'<br>'+'USD/HKD: '+str(round(currency_df.loc['HKD','Last_Day'],2))+'('+str(100*currency_df.loc['HKD','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['HKD','mtd'])+'%/'+str(100*currency_df.loc['HKD','qtd'])+'%/'+str(100*currency_df.loc['HKD','ytd'])+'%'
    a[7] = a[7]+'<br>'+'USD/JPY: '+str(round(currency_df.loc['JPY','Last_Day'],2))+'('+str(100*currency_df.loc['JPY','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['JPY','mtd'])+'%/'+str(100*currency_df.loc['JPY','qtd'])+'%/'+str(100*currency_df.loc['JPY','ytd'])+'%'
    a[8] = a[8]+'<br>'+'USD/CNY: '+str(round(currency_df.loc['CNY','Last_Day'],2))+'('+str(100*currency_df.loc['CNY','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['CNY','mtd'])+'%/'+str(100*currency_df.loc['CNY','qtd'])+'%/'+str(100*currency_df.loc['CNY','ytd'])+'%'
    swiss = 'USD/CHF: '+str(round(currency_df.loc['CHF','Last_Day'],2))+'('+str(100*currency_df.loc['CHF','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['CHF','mtd'])+'%/'+str(100*currency_df.loc['CHF','qtd'])+'%/'+str(100*currency_df.loc['CHF','ytd'])+'%'
    a.append(swiss)
    
    py.sign_in('fzn0728', '1enskD2UuiVkZbqcMZ5K')

    label_color = "rgb(0, 215, 0)"

    Australia = {
      "hoverinfo": "text+name", 
      "lat": [-33.8688],
      "lon": [151.2093],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[0],
      "name":'Australia',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    India = {
      "hoverinfo": "text+name", 
      "lat": [19.0760],
      "lon": [72.8777],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[1],
      "name":'India',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    Brazil = {
      "hoverinfo": "text+name", 
      "lat": [-23.5505],
      "lon": [-46.6333],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[2],
      "name":'Brazil',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    UK = {
      "hoverinfo": "text+name", 
      "lat": [51.5074],
      "lon": [-0.1278],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[3],
      "name":'UK',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    Germany = {
      "hoverinfo": "text+name", 
      "lat": [52.5200],
      "lon": [13.4050],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[4],
      "name":'Germany',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    US = {
      "hoverinfo": "text+name", 
      "lat": [40.7128],
      "lon": [-74.0059],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[5],
      "name":'US',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    Hong_Kong = {
      "hoverinfo": "text+name", 
      "lat": [22.3964],
      "lon": [114.1095],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[6],
      "name":'Hong Kong',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }


    Japan = {
      "hoverinfo": "text+name", 
      "lat": [35.6895],
      "lon": [139.6917],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[7],
      "name":'Japan',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    Shanghai = {
      "hoverinfo": "text+name", 
      "lat": [31.2304],
      "lon": [121.4737],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[8],
      "name":'Shanghai',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    Switzerland = {
      "hoverinfo": "text+name", 
      "lat": [47.3769],
      "lon": [8.5417],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[9],
      "name":'Switzerland',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    
    '''
    trace1 = {
      "text": ['Australia','India','Brazil','United Kingdom','Germany','United States of America','China','Japan'],
      "locations": ["AUS","IND","BRA","GBR","DEU","USA","CHN","JPN",], 
      "type": "scattergeo", 
      "uid": "b73666", 
      "name":""
    }
    '''
    
    Country_index = {
      "z": ['7','8','6','5','4','1','2','3','9'],
      "text": ['Australia','India','Brazil','United Kingdom','Germany','United States of America','China','Japan','Switzerland'],
      "colorscale": [[0.0, "rgb(255,0,0)"], [0.2, "rgb(255,255,0)"], [0.4, "rgb(128,255,0)"],\
                      [0.6, "rgb(0,255,64)"],[0.8, "rgb(0,255,255)"], [1.0, "rgb(0,128,192)"]], 
      "locations": ["AUS","IND","BRA","GBR","DEU","USA","CHN","JPN","CHE"], 
      "type": "choropleth", 
      "uid": "b73666", 
      "showscale": False,
      "name":"Country Index",
      "zmax":"9",
      "zmin":"1"
    }
    
    
    
    data = Data([Australia, India, Brazil, UK, Germany, US, Hong_Kong, Japan, Shanghai, Switzerland, Country_index])
    layout = {
      "autosize": True, 
      "geo": {
        "countrywidth": 0.5, 
        "lakecolor": "rgb(129, 145, 254)", 
        "landcolor": "rgb(40, 23, 255)", 
        "lataxis": {
          "gridcolor": "rgb(102, 102, 102)", 
          "gridwidth": 0.5, 
          "showgrid": True
        }, 
        "lonaxis": {
          "gridcolor": "rgb(102, 102, 102)", 
          "gridwidth": 0.5, 
          "showgrid": True
        }, 
        "oceancolor": "rgb(214, 207, 209)", 
        "projection": {
          "rotation": {
            "lat": 40, 
            "lon": -100, 
            "roll": 0
          }, 
          "type": "orthographic"
        }, 
        "showcountries": True, 
        "showlakes": True, 
        "showland": True, 
        "showocean": True
      }, 
      "height": 400, 
      "margin": {
        "r": 100, 
        "t": 100, 
        "b": 100, 
        "l": 100
      }, 
      "showlegend": True, 
      "title": "Global Index Performance", 
      "width": 500
    }
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig)