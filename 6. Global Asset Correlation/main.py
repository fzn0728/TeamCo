# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:41:37 2016

@author: ZFang
"""

from datetime import datetime
import pandas_datareader.data as wb
from fredapi import Fred
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import dateutil.relativedelta
import urllib.request
import ast
import math
from plotly.graph_objs import *


def get_return(tickerlist):
    start = datetime(2000,1,1)
    end = datetime.today()
    p = wb.DataReader(tickerlist,'yahoo',start,end)
    price_df = p['Adj Close']
    price_df = price_df.interpolate()
    past_price_df = price_df.shift(1)
    return_df = (price_df - past_price_df)/past_price_df

    for i in return_df.columns:
        first_index = return_df.loc[:,i].first_valid_index()-timedelta(days=1)
        return_df.ix[first_index,i]=0
    return return_df
    
    
def get_price(tickerlist):
    start = datetime(2000,1,1)
    end = datetime.today()
    p = wb.DataReader(tickerlist,'yahoo',start,end)
    price_df = p['Adj Close']
    price_df = price_df.interpolate()
    
    return price_df    


def get_libor():
    fred = Fred(api_key='a0718ea00e6784c5f8b452741622a98c')
    Libor_1M = pd.DataFrame(fred.get_series('USD1MTD156N',observation_start='1/1/2000'))
    Libor_3M = pd.DataFrame(fred.get_series('USD3MTD156N',observation_start='1/1/2000'))
    Treasury_1Y = pd.DataFrame(fred.get_series('DGS1',observation_start='1/1/2000'))
    Treasury_5Y = pd.DataFrame(fred.get_series('DGS5',observation_start='1/1/2000'))
    Treasury_10Y = pd.DataFrame(fred.get_series('DGS10',observation_start='1/1/2000'))
    Treasury_20Y = pd.DataFrame(fred.get_series('DGS20',observation_start='1/1/2000'))
    Treasury_30Y = pd.DataFrame(fred.get_series('DGS30',observation_start='1/1/2000'))
    WILLREITIND = pd.DataFrame(fred.get_series('WILLREITIND',observation_start='1/1/2000'))
    OAS = pd.DataFrame(fred.get_series('BAMLH0A0HYM2',observation_start='1/1/2000'))
    
    
    GDP = pd.DataFrame(fred.get_series('GDPC1',observation_start='9/19/2011'))
    CPI = pd.DataFrame(fred.get_series('CPIAUCSL',observation_start='9/19/2011'))
    Fed_Rate = pd.DataFrame(fred.get_series('DFF',observation_start='9/19/2011'))
    Uneply = pd.DataFrame(fred.get_series('UNRATE',observation_start='9/19/2011'))
    M2 = pd.DataFrame(fred.get_series('M2',observation_start='9/19/2011'))
    Non_farm = pd.DataFrame(fred.get_series('PAYEMS',observation_start='9/19/2011'))
    Fed_Debt = pd.DataFrame(fred.get_series('GFDEGDQ188S',observation_start='9/19/2011'))
    Dollar_Index = pd.DataFrame(fred.get_series('TWEXB',observation_start='9/19/2011'))    
    HOUST = pd.DataFrame(fred.get_series('HOUST',observation_start='9/19/2011'))

    
    macro_m_price = pd.concat([GDP,CPI,Uneply,M2,Non_farm,Fed_Debt,Dollar_Index,HOUST],axis=1)
    macro_d_price = pd.concat([Libor_1M,Libor_3M,Treasury_1Y,Treasury_5Y,Treasury_10Y,Treasury_20Y,Treasury_30Y,WILLREITIND,OAS],axis=1)
    macro_m_price.columns=['GDP','CPI','Uneply','M2','Non_farm','Fed_Debt','Dollar_index','HOUST']
    macro_d_price.columns = ['Libor_1M','Libor_3M','Treasury_1Y','Treasury_5Y','Treasury_10Y','Treasury_20Y','Treasury_30Y','WILLREITIND','OAS']
    
    # Calculate return
    Fed_Rate = (Fed_Rate - Fed_Rate.shift(1))/Fed_Rate.shift(1)
    macro_m = (macro_m_price - macro_m_price.shift(1))/macro_m_price.shift(1)
    macro_d = (macro_d_price - macro_d_price.shift(1))/macro_d_price.shift(1)
    
    
    return Fed_Rate,macro_m_price,macro_m,macro_d_price,macro_d
    
def add_column_name(dataframe):
    l = []
    for i in dataframe.columns:
        l.append(ticker_dict[i])
    dataframe.columns = l
    return dataframe
   
    
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
      
    
def equity_return_MTD_QTD_YTD(df):
    return_df = pd.DataFrame(np.zeros([5,9]),index=['T','DTD','MTD','QTD','YTD'],columns=df.columns)
    return_df.iloc[0,:] = round(100*(df.iloc[0,:]-df.iloc[0,:])/df.iloc[0,:],2)
    return_df.iloc[1,:] = round(100*(df.iloc[0,:]-df.iloc[1,:])/df.iloc[1,:],2)
    return_df.iloc[2,:] = round(100*(df.iloc[0,:]-df.iloc[2,:])/df.iloc[2,:],2)
    return_df.iloc[3,:] = round(100*(df.iloc[0,:]-df.iloc[3,:])/df.iloc[3,:],2)
    return_df.iloc[4,:] = round(100*(df.iloc[0,:]-df.iloc[4,:])/df.iloc[4,:],2)
    return return_df
    
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
    
    equity_etf_list = ['SPY','EWJ','EWG','IWV','IYY','FEZ','ONEQ','TLT','IEF']
    equity_index_list = ['^GSPC','^N225','^SSEC','^FTSE','^HSI','^BVSP','^AORD','^GDAXI','^STOXX50E','^BSESN','^VIX']
    currency_list = ['FXY','FXB','FXE','FXA','FXF','FXCH']
    commodity_etf_list = ['GLD','SLV','OIL','UNL','JJC','WEAT','CORN']
    equity_sector_list = ['XLY','XLP','XLE','XLF','XLV','XLI','XLB','XLRE','XLK','XLU']
    globe_equity_index_list = ['^GSPC','^N225','^SSEC','^FTSE','^HSI','^BVSP','^AORD','^GDAXI','^BSESN']



    ticker_dict = {'FXY':'JPY/USD','FXB':'GBP/USD','FXE':'EUR/USD','FXA':'AUD/USD','FXF':'CHF/USD','FXCH':'CHY/USD',\
        'SPY':'S&P_ETF','EWJ':'NIKKEI_ETF','EWG':'DAX_ETF','IWV':'RUSSELL_ETF','IYY':'DOW_ETF',\
         'FEZ':'EURO_50_ETF','ONEQ':'NASDAQ_ETF','GLD':'GOLD','SLV':'SILVER','OIL':'OIL',\
         'UNL':'GAS','JJC':'COPPER','WEAT':'WEAT','CORN':'CORN','TLT':'20yr_Bond','IEF':'7_10_yr_Bond',\
         '^GSPC':'S&P500','^N225':'Nikki_225','^SSEC':'SSE_Composite','^FTSE':'FTSE_100','^HSI':'HANG_SENG_INDEX',\
         '^BVSP':'IBOVESPA','^AORD':'ALL_ORDINARIES','^GDAXI':'DAX','^STOXX50E':'ESTX50','^BSESN':'S&P_BSE_SENSEX',\
         '^VIX':'VIX','XLY':'Consumer Discretionary','XLP':'Consumer Staples','XLE':'Energy','XLF':'Financials',\
         'XLV':'Health Care','XLI':'Industrials','XLB':'Materials','XLRE':'Real Estate','XLK':'Technology','XLU':'Utilities'}
         
    ###### Equity ETF ######
    equity_etf = get_return(equity_etf_list)
    equity_etf = add_column_name(equity_etf)
    ###### Equity Index ######
    equity_index = get_return(equity_index_list)
    equity_index_price = get_price(equity_index_list)
    equity_index = add_column_name(equity_index)
    equity_index_price = add_column_name(equity_index_price)
    ###### Currency ######
    currency_etf = get_return(currency_list)    
    currency_etf = add_column_name(currency_etf)
    ###### Currency ######
    commodity_etf = get_return(commodity_etf_list).iloc[:-2,:]
    commodity_etf = add_column_name(commodity_etf)
    ###### Equity(SP500) Sector ######
    equity_sector = get_return(equity_sector_list)
    equity_sector = add_column_name(equity_sector)
    
    Fed_Rate,macro_m_price,macro_m,macro_d_price,macro_d = get_libor()
    
    ###### Globe Plot Data ######
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

    # Plotly
    color1 = 'b'
    color2 = 'b'
    label_color = "rgb(0, 215, 0)"
    
    py.sign_in('fzn0728', '1enskD2UuiVkZbqcMZ5K')
       
    ### Figure 1 Developed Equity Market Cummulative return
    cum_equity_index = (1+equity_index).cumprod()-1
    cum_DM_equity_index = cum_equity_index.loc[:,['ALL_ORDINARIES','FTSE_100','DAX','S&P500','Nikki_225','ESTX50']]
    
    trace1 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['ALL_ORDINARIES'],
        name='ALL_ORDINARIES(Australia)'
    )
    trace2 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['FTSE_100'],
        name='FTSE_100(UK)'
    )
    trace3 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['DAX'],
        name='DAX(Germany)'
    )
    trace4 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['S&P500'],
        name='S&P500(USA)'
    )
    trace5 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['Nikki_225'],
        name='Nikki_225(Japan)'
    )
    trace6 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['ESTX50'],
        name='ESTX50(EU)'
    )

    data = [trace1,trace2,trace3,trace4,trace5,trace6]
    layout = go.Layout(
        title='Cumulative Return of Developed Market Equity Indices',
        yaxis=dict(
            title='Cumulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_1 = go.Figure(data=data, layout=layout)
    plot_url_1 = py.plot(fig_1, filename='Figure 1 Cumulative Return of Developed Market Equity Indices', sharing='public')
    
    
    

    
    ### Figure 2 Developing Equity Market Cummulative return
    cum_EM_equity_index = cum_equity_index.loc[:,['IBOVESPA','S&P_BSE_SENSEX','HANG_SENG_INDEX','SSE_Composite']]
    
    trace1 = go.Scatter(
        x=cum_EM_equity_index.index,
        y=100*cum_EM_equity_index['IBOVESPA'],
        name='IBOVESPA(Brazil)'
    )
    trace2 = go.Scatter(
        x=cum_EM_equity_index.index,
        y=100*cum_EM_equity_index['S&P_BSE_SENSEX'],
        name='P_BSE_SENSEX(India)'
    )
    trace3 = go.Scatter(
        x=cum_EM_equity_index.index,
        y=100*cum_EM_equity_index['HANG_SENG_INDEX'],
        name='HANG_SENG_INDEX(HK)'
    )
    trace4 = go.Scatter(
        x=cum_EM_equity_index.index,
        y=100*cum_EM_equity_index['SSE_Composite'],
        name='S&SSE_Composite(China)'
    )

    data = [trace1,trace2,trace3,trace4]
    layout = go.Layout(
        title='Cumulative Return of Emerging Market Equity Indices',
        yaxis=dict(
            title='Cumulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_2 = go.Figure(data=data, layout=layout)
    plot_url_2 = py.plot(fig_2, filename='Figure 2 Cumulative Return of Emerging Market Equity Indices', sharing='public')    
    
    
    ### Figure 3 S&P500 with top 10 major equity index 12 month rolling
    top_10_list = ['ALL_ORDINARIES','S&P_BSE_SENSEX','IBOVESPA','FTSE_100','DAX','S&P500','HANG_SENG_INDEX','Nikki_225','SSE_Composite','ESTX50']
    equity_corr = equity_index[top_10_list].rolling(window=260).corr()
    mask = np.ones(equity_corr.iloc[0].shape,dtype='bool')
    mask[np.triu_indices(len(equity_corr.iloc[0]))] = False
    equity_avg_corr_l = []
    for i in range(len(equity_corr)):
        equity_avg_corr_l.append(equity_corr.iloc[i][(equity_corr.iloc[i]>-2)&mask].sum().sum()/45)
    equity_avg_corr = pd.DataFrame(equity_avg_corr_l, index=equity_index.index, columns=['Average_Correlation'])
    equity_avg_corr = equity_avg_corr['2000-12-29 00:00:00':]

    trace1 = go.Scatter(
        x=equity_avg_corr.index,
        y=equity_avg_corr['Average_Correlation'],
        name='Avg Correlation'
    ) 
    
    data = [trace1]
    layout = go.Layout(
        title='Average Correlation Between 10 Major Equity Indices',
        showlegend=True,
        yaxis=dict(
            title='Equity Index Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
    fig_3 = go.Figure(data=data, layout=layout)
    plot_url_3 = py.plot(fig_3, filename='Figure 3 Average Correlation Between 10 Major Equity Indices', sharing='public')
    
    
    
    ### Figure 4 Correlation Between DM and EM Countries Equity Index
    DM_avg_equity_index = equity_index.loc[:,['ALL_ORDINARIES','FTSE_100','DAX','S&P500','Nikki_225','ESTX50']].mean(axis=1)
    EM_avg_equity_index = equity_index.loc[:,['IBOVESPA','S&P_BSE_SENSEX','HANG_SENG_INDEX','SSE_Composite']].mean(axis=1)
    
    DM_EM_index = pd.concat([DM_avg_equity_index,EM_avg_equity_index],axis=1)
    DM_EM_index.columns = ['DM Market','EM Market']
    
    DM_EM_corr = DM_EM_index.rolling(window=260).corr(DM_EM_index['DM Market']).ix['2001-01-02 00:00:00':,['EM Market']]
    
    trace1 = go.Scatter(
        x=DM_EM_corr.index,
        y=DM_EM_corr['EM Market'],
        name='DM and EM Correlation'
        )

    data = [trace1]
    layout = go.Layout(
        title='Correlation Between DM and EM Countries Equity Index',
        showlegend=True,
        yaxis=dict(
            title='DM EM Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
            
    fig_4 = go.Figure(data=data, layout=layout)
    plot_url_4 = py.plot(fig_4, filename='Figure 4 Correlation Between DM and EM Countries Equity Index', sharing='public')
    
    
    
    ### Figure 5 Plot the all the yield change curve
    libor = macro_d_price.loc[:,['Libor_1M','Libor_3M','Treasury_1Y','Treasury_5Y','Treasury_10Y','Treasury_20Y','Treasury_30Y']]
    
    trace1 = go.Scatter(
        x=libor.index,
        y=libor['Libor_1M'],
        name='Libor_1M'
    )
    trace2 = go.Scatter(
        x=libor.index,
        y=libor['Libor_3M'],
        name='Libor_3M'
    )
    trace3 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_1Y'],
        name='Treasury_1Y'
    )
    trace4 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_5Y'],
        name='Treasury_5Y'
    )
    trace5 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_10Y'],
        name='Treasury_10Y'
    )
    trace6 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_20Y'],
        name='Treasury_20Y'
    )
    trace7 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_30Y'],
        name='Treasury_30Y'
    )

    data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7]
    layout = go.Layout(
        title='Libor/Treasury Rate',
        yaxis=dict(
            title='Yield',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
    annotations = []   
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Some Short Description',
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))  
                
    layout['annotations'] = annotations   
            
            
    fig_5 = go.Figure(data=data, layout=layout)
    plot_url_5 = py.plot(fig_5, filename='Figure 5 Libor and Treasury Rate', sharing='public')
    #libor.plot()
    
    ### Figure 6 Cumulative Return of Major Currencies
    
    cum_currency = (1+currency_etf).cumprod()-1
    
    trace1 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['AUD/USD'],
        name='AUD/USD'
    )
    trace2 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['GBP/USD'],
        name='GBP/USD'
    )
    trace3 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['EUR/USD'],
        name='EUR/USD'
    )
    trace4 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['CHF/USD'],
        name='CHF/USD'
    )
    trace5 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['JPY/USD'],
        name='JPY/USD'
    )

    data = [trace1,trace2,trace3,trace4,trace5]
    layout = go.Layout(
        title='Cumulative Return of Major Currencies',
        yaxis=dict(
            title='Cummulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_6 = go.Figure(data=data, layout=layout)
    plot_url_6 = py.plot(fig_6, filename='Figure 6 Cumulative Return of Major Currencies', sharing='public')    
    
    
    


    ### Figure 7 Correlation of Currencies with S&P 500
    currency_sp = pd.concat([currency_etf,equity_index['S&P500']],axis=1)
    # deal with nan data
    currency_sp = currency_sp.interpolate()
    currency_sp_avg_corr = currency_sp.rolling(window=260).corr(currency_sp['S&P500']).ix[260:,[\
                        'AUD/USD','GBP/USD','EUR/USD','JPY/USD','CHF/USD']].mean(axis=1)
    currency_sp_avg_corr = currency_sp_avg_corr['2007-01-02 00:00:00':]
    currency_sp_avg_corr.name = 'Average_Correlation'
    
    
    trace1 = go.Scatter(
        x=currency_sp_avg_corr.index,
        y=currency_sp_avg_corr.values,
        name='Average Correlation'
    ) 
    
    data = [trace1]
    layout = go.Layout(
        title='Average Correlation of Major Currencies with S&P 500',
        showlegend=True,
        yaxis=dict(
            title='Average Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
    fig_7 = go.Figure(data=data, layout=layout)
    plot_url_7 = py.plot(fig_7, filename='Figure 7 Average Correlation of Major Currency ETF with S&P 500', sharing='public')
    
    
    ### Figure 8 Correlation of 10Y Treasury Yield and S&P 500
    trea_sp = pd.concat([macro_d_price['Treasury_10Y'],equity_index['S&P500']],axis=1)
    trea_sp = trea_sp.interpolate()
    trea_sp_corr = trea_sp.rolling(window=260).corr(trea_sp['S&P500']).ix[260:,['Treasury_10Y']]
    trea_sp_corr_yield = pd.concat([trea_sp_corr,macro_d_price.ix[260:,'Treasury_10Y']],axis=1)
    trea_sp_corr_yield.columns = ['Correlation','10Y_yield']
    # trea_sp_corr_yield.plot()
    
    
    
    trace1 = go.Scatter(
        x=trea_sp_corr_yield.index,
        y=trea_sp_corr_yield['Correlation'],
        name='Correlation of Treasury&Equity'
    ) 
    
    trace2 = go.Scatter(
        x=trea_sp_corr_yield.index,
        y=trea_sp_corr_yield['10Y_yield'],
        name='Treasury Yield',
        yaxis='y2'
    ) 
    
    data = [trace1, trace2]
    layout = go.Layout(
        title='Correlation 10 Year Treasury & S&P500',
        yaxis=dict(
            title='Correlation'
        ),
        yaxis2=dict(
            title='Treasury_10Y',
            titlefont=dict(
                color=color2
            ),
            tickfont=dict(
                color=color2
            ),
            overlaying='y',
            side='right'
        )
    )
    
    fig8 = go.Figure(data=data, layout=layout)
    plot_url_8 = py.plot(fig8, filename='Figure 8 Correlation 10 Year Treasury & S&P500',sharing='public')
    
    

    ### Figure 9 Cumulative Return of Commodities
    cum_commodity_etf = (1+commodity_etf).cumprod()-1
    # cum_commodity_etf.loc[:,['CORN','GOLD','COPPER','OIL','SILVER','GAS','WEAT']].plot()
    
    trace1 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['CORN'],
        name='CORN'
    )
    trace2 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['GOLD'],
        name='GOLD'
    )
    trace3 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['COPPER'],
        name='COPPER'
    )
    trace4 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['OIL'],
        name='OIL'
    )
    trace5 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['SILVER'],
        name='SILVER'
    )
    trace6 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['GAS'],
        name='GAS'
    )
    trace7 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['WEAT'],
        name='WEAT'
    )

    data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7]
    layout = go.Layout(
        title='Cumulative Return of Major Commodities',
        yaxis=dict(
            title='Cumulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_9 = go.Figure(data=data, layout=layout)
    plot_url_9 = py.plot(fig_9, filename='Figure 9 Cumulative Return of Major Commodities', sharing='public')    
    
    
    
    
    ### Figure 10 Correlation of S&P500 and other commodities
    comm_sp = pd.concat([commodity_etf,equity_index['S&P500']],axis=1)
    comm_sp = comm_sp.interpolate()
    comm_sp_corr = comm_sp.rolling(window=260).corr(comm_sp['S&P500']).ix[260:,['CORN','GOLD','COPPER','OIL','SILVER','GAS','WEAT']]
    comm_sp_corr = comm_sp_corr['2005-11-16 00:00:00':]
    # comm_sp_corr.plot()
    
    trace1 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['CORN'],
        name='CORN'
    )
    trace2 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['GOLD'],
        name='GOLD'
    )
    trace3 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['COPPER'],
        name='COPPER'
    )
    trace4 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['OIL'],
        name='OIL'
    )
    trace5 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['SILVER'],
        name='SILVER'
    )
    trace6 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['GAS'],
        name='GAS'
    )
    trace7 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['WEAT'],
        name='WEAT'
    )

    data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7]
    layout = go.Layout(
        title='Correlation of Commodities with S&P500',
        yaxis=dict(
            title='Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
            
    fig_10 = go.Figure(data=data, layout=layout)
    plot_url_10 = py.plot(fig_10, filename='Figure 10 Correlation of Commodities with S&P500', sharing='public')
    
    
    ### Figure 11 Average Correlation with all Commodities
    comm_corr = commodity_etf.rolling(window=260).corr()
    mask = np.ones(comm_corr.iloc[0].shape,dtype='bool')
    mask[np.triu_indices(len(comm_corr.iloc[0]))] = False
    comm_avg_corr_l = []
    for i in range(len(comm_corr)):
        comm_avg_corr_l.append(comm_corr.iloc[i][(comm_corr.iloc[i]>-2)&mask].sum().sum()/21)
    comm_avg_corr = pd.DataFrame(comm_avg_corr_l, index=commodity_etf.index, columns=['Average_Correlation'])
    comm_avg_corr = comm_avg_corr['2007-05-10 00:00:00':]

    trace1 = go.Scatter(
        x=currency_sp_avg_corr.index,
        y=currency_sp_avg_corr.values,
        name='Average Correlation'
    ) 
    
    data = [trace1]
    layout = go.Layout(
        title='Average Correlation of Major Commodities',
        showlegend=True,
        yaxis=dict(
            title='Average Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
    fig_11 = go.Figure(data=data, layout=layout)
    plot_url_11 = py.plot(fig_11, filename='Figure 11 Average Correlation of Major Commodities', sharing='public')
    
    
    ### Figure 12 Option Adjusted Spread (OAS) and VIX
    oas_vix = pd.concat([equity_index_price['VIX'],macro_d['OAS']],axis=1)
    oas_vix = oas_vix.interpolate()
    
    
    trace1 = go.Scatter(
        x=oas_vix.index,
        y=oas_vix['VIX'],
        name='VIX'
    )
    trace2 = go.Scatter(
        x=oas_vix.index,
        y=oas_vix['OAS'],
        name='OAS',
        yaxis='y2'
    )

    data = [trace1,trace2]
    layout = go.Layout(
        title='Option Adjusted Spread (OAS) and VIX',
        yaxis=dict(
            title='VIX Value',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        ),
        yaxis2=dict(
            title='OAS',
            titlefont=dict(
                color=color1
            ),
            tickfont=dict(
                color=color1
            ),
            overlaying='y',
            side='right'
        )
    )
            
            
    fig_12 = go.Figure(data=data, layout=layout)
    plot_url_12 = py.plot(fig_12, filename='Figure 12 Option Adjusted Spread (OAS) and VIX', sharing='public')
        
 
    ### Figure 13 Correlation of OAS and S&P500
    oas_sp = pd.concat([-equity_index['S&P500'],equity_index['VIX'],macro_d['OAS']],axis=1)
    oas_sp = oas_sp.interpolate()
    oas_sp_corr = oas_sp.rolling(window=260).corr(oas_sp['OAS']).ix[260:,['S&P500','VIX']]
    # oas_sp_corr.plot()
    
    trace1 = go.Scatter(
        x=oas_sp_corr.index,
        y=oas_sp_corr['S&P500'],
        name='OAS to S&P500 (Inverse)'
    )
    trace2 = go.Scatter(
        x=oas_sp_corr.index,
        y=oas_sp_corr['VIX'],
        name='OAS to VIX'
    )

    data = [trace1,trace2]
    layout = go.Layout(
        title='Correlation of High Yield OAS to S&P500 and VIX',
        yaxis=dict(
            title='Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
            
    fig_13 = go.Figure(data=data, layout=layout)
    plot_url_13 = py.plot(fig_13, filename='Figure 13 Correlation of High Yield OAS to S&P500 and VIX', sharing='public')
    
    
    ### Figure 14 Cummulative Return of S&P 500 Sector Index
    cum_equity_sector = (1+equity_sector).cumprod()-1
    
    
    trace1 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Materials'],
        name='Materials'
    )
    trace2 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Energy'],
        name='Energy'
    )
    trace3 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Financials'],
        name='Financials'
    )
    trace4 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Industrials'],
        name='Industrials'
    )
    trace5 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Technology'],
        name='Technology'
    )
    trace6 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Consumer Staples'],
        name='Consumer Staples'
    )
    trace7 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Real Estate'],
        name='Real Estate'
    )
    trace8 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Utilities'],
        name='Utilities'
    )
    trace9 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Health Care'],
        name='Health Care'
    )
    trace10 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Consumer Discretionary'],
        name='Consumer Discretionary'
    )  
    
    
    data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10]
    layout = go.Layout(
        title='Cummulative Return of Major S&P500 Component Indices',
        yaxis=dict(
            title='Cummulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_14 = go.Figure(data=data, layout=layout)
    plot_url_14 = py.plot(fig_14, filename='Figure 14 Cummulative Return of Major S&P500 Component Indices', sharing='public')    
    
    
    ### Figure 15 Correlation between S&P 500 Sectors
    equity_sector_corr = equity_sector.rolling(window=260).corr()
    mask_sector = np.ones(equity_sector_corr.iloc[0].shape,dtype='bool')
    mask_sector[np.triu_indices(len(equity_sector_corr.iloc[0]))] = False
    equity_sector_corr_l = []
    for i in range(len(equity_sector_corr)):
        equity_sector_corr_l.append(equity_sector_corr.iloc[i][(equity_sector_corr.iloc[i]>-2)&mask_sector].sum().sum()/45)
    equity_sector_avg_corr = pd.DataFrame(equity_sector_corr_l, index=equity_sector.index, columns=['Average_Correlation'])
    equity_sector_avg_corr = equity_sector_avg_corr['2001-01-11 00:00:00':]

    # comm_sp_corr.plot()

    trace1 = go.Scatter(
        x=equity_sector_avg_corr.index,
        y=equity_sector_avg_corr['Average_Correlation'],
        name='Average Correlation'
        )

    data = [trace1]
    layout = go.Layout(
        title='Average Correlation of Different Component in S&P500',
        showlegend=True,
        yaxis=dict(
            title='Average Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
            
    fig_15 = go.Figure(data=data, layout=layout)
    plot_url_15 = py.plot(fig_15, filename='Figure 15 Average Correlation of Different Component in S&P500', sharing='public')
    
    ### Figure 16 Globe Major Index and Currency Performance
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
    fig_16 = Figure(data=data, layout=layout)
    plot_url_16 = py.plot(fig_16, filename='Figure 16 Globe Major Index and Currency Performance', sharing='public')    
    ###########################################
    


        