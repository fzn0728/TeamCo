# -*- coding: utf-8 -*-
"""
This is module for rolling financial ratio

@author: ZFang
"""

import numpy as np
from numpy.lib.stride_tricks import as_strided
import pandas as pd
import mod_financial_ratio as r

def time_drawdown(dataframe, index_name, window_length, start_date, end_date, start_gap):
    '''Calculate the drawdown time series number given time parameter
    
    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        window_length is the window time you want to take into account. If you want to check 1 year maximum draw
            down, it should be 12, if checking the hold period, it should be 109.
        start_date shoud be an integer within [0,109), 109 is the length of all available data
        end_date should be an integer within (0,109]
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap
            
    Returns:
        A dataframe that contain drawdown of different index at different time within given time interval and time window
    '''
    sub_dataframe = dataframe[index_name].loc[start_gap:]
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))
    s = np.cumprod(sub_dataframe.loc[start_date:end_date]+1)
    rolling_max = s.rolling(window_length, min_periods=0).max()
    rolling_dd = s - rolling_max
    df = pd.concat([s, rolling_max, rolling_dd], axis=1)
    df.columns = [index_name, 'rol_max_%d' % window_length, 'rol_dd_%d' % window_length]
    # Format decimal point and dataframe name
    df = np.round(df, decimals=3)
    df.name = 'Time Drawdown'
    return df

def max_drawdown(dataframe, index_name, window_length, start_date, end_date, start_gap):
    '''Calculate the maximum drawdown given time parameter
    
    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
            in this case, generally index_name include only one string(index name)
        window_length is the window time you want to take into account. If you want to check 1 year maximum draw
            down, it should be 12, if checking the hold period, it should be 109.
        start_date shoud be an integer within [0,109), 109 is the length of all available data
        end_date should be an integer within (0,109]
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap
            
    Returns:
        A number which is the maximum drawdown within certain time length
    '''
    sub_dataframe = dataframe[index_name].loc[start_gap:]
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))
    s = np.cumprod(sub_dataframe.loc[start_date:end_date]+1)
    rolling_max = s.rolling(window_length, min_periods=0).max()
    rolling_dd = s - rolling_max
    max_dd = min(rolling_dd)
    return print ('The maximum drawdown during %s to %s is %.4f' %(dataframe.loc[start_gap+start_date,'Date'],dataframe.loc[start_gap+end_date,'Date'],max_dd))

def rolling_beta(dataframe,columns_name,window_length,min_periods,start_gap):
    '''Calculate rolling beta given time window and columns name
    
    Args:
        dataframe is the dataframe passed by concat_data() function
        columns_name is the index we want to calculate, which also include the market index
            must be consistent with index name in the excel sheet
        window_length is the window time you want to take into account. If you want to check 1 year maximum draw
            down, it should be 12, if checking the hold period, it should be 109.
        min_periods is the minimum period that you could take into account and make calculation. For example,
            if you set time window to be 36 months, and minimum period is 12, then all remaining interval at the beginning
            or end which has more than 12 months will all be taken into account.
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap
            
    Returns:
        Return a dataframe which include the beta to the market at different time.
    '''
    sub_dataframe = dataframe[columns_name].loc[start_gap:] # skip the start gap
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))
    beta_df = pd.DataFrame(index = range(len(sub_dataframe.index)-min_periods+1), columns = [columns_name[0:3]])
    for j in columns_name[0:3]:
        cov_matrix = sub_dataframe[[j,columns_name[3]]].rolling(window_length, min_periods).cov(sub_dataframe[[j,columns_name[3]]], pairwise = True)
        for i in range(0, len(cov_matrix)-min_periods+1, 1):
            beta_df.loc[i, j] = cov_matrix[i+min_periods-1].iloc[0][1]/cov_matrix[i+min_periods-1].iloc[1][1]
    beta_df.index = dataframe.loc[(min_periods+start_gap-1):,'Date'].values
    # Format decimal point and dataframe name
    beta_df = np.round(beta_df, decimals=3)
    beta_df.name = '36 Month Rolling Beta'
    return beta_df

def rolling_annulized_return(dataframe,columns_name,window_length,min_periods,start_gap):
    '''Calculate annulized return given time window and columns name
    
    Args:
        dataframe is the dataframe passed by concat_data() function
        columns_name is the index we want to calculate, which also include the market index
            must be consistent with index name in the excel sheet
        window_length is the window time you want to take into account. If you want to check 1 year annul return,
            it should be 12, if checking the whole period, it should be 109.
        min_periods is the minimum period that you could take into account and make calculation. For example,
            if you set time window to be 36 months, and minimum period is 12, then all remaining interval at the beginning
            or end which has more than 12 months will all be taken into account.
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap
            
    Returns:
        Return a dataframe which include the annul return for all index include market index at different time.
    '''    
    sub_dataframe = dataframe[columns_name].loc[start_gap:]
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))
    annual_return_df = pd.DataFrame(columns = columns_name)
    for j in columns_name:
        annual_return_df[j] = sub_dataframe[j].rolling(window_length, min_periods).apply(lambda x: np.prod(1+x)**(12/len(x))-1)[min_periods-1:].values
    annual_return_df.index = dataframe.loc[(min_periods+start_gap-1):,'Date'].values
    # Format decimal point and dataframe name
    annual_return_df = np.round(annual_return_df, decimals=3)
    annual_return_df.name = '36 Month Rolling Annual Return'
    return annual_return_df

def cumulative_return(dataframe,columns_name,window_length,min_periods,start_gap):
    '''Calculate cummulative return given time window and columns name
    
    Args:
        dataframe is the dataframe passed by concat_data() function
        columns_name is the index we want to calculate, which also include the market index
            must be consistent with index name in the excel sheet
        window_length is the window time you want to take into account. If you want to check 1 year annul return,
            it should be 12, if checking the hold period, it should be 109.
        min_periods is the minimum period that you could take into account and make calculation. For example,
            if you set time window to be 36 months, and minimum period is 12, then all remaining interval at the beginning
            or end which has more than 12 months will all be taken into account.
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap
            
    Returns:
        Return a dataframe which include the cummulative return for all index include market index at different time.
    ''' 
    # We include start_gap-1 period to force the original date is 0
    sub_dataframe = dataframe[columns_name].loc[(start_gap-1):]
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))
    cum_return_df = pd.DataFrame(columns = columns_name)
    for j in columns_name:
        cum_return_df[j] = np.cumprod(1+sub_dataframe[j])-1
    cum_return_df.index = dataframe.loc[(start_gap-1):,'Date'].values
    # Format decimal point and dataframe name
    cum_return_df = np.round(cum_return_df, decimals=3)  
    cum_return_df.name = 'Cummulative Return'
    return cum_return_df  

def rolling_sortino_ratio(dataframe, columns_name, window_length, min_periods, start_gap, MAR, threshold, order=2):
    '''Calculate the rolling sortino ratio of target index. Sortino ratio is the monthly cumulative return minus MAR and then divided by 
    downside standard deviation, then annulized it. 
    
    Args:
        dataframe is the dataframe passed by concat_data() function
        columns_name is the index we want to calculate, which also include the market index
            must be consistent with index name in the excel sheet
        window_length is the window time you want to take into account. If you want to check 1 year rolling sortino ratio,
            it should be 12, if checking the whole period, it should be 109.
        min_periods is the minimum period that you could take into account and make calculation. For example,
            if you set time window to be 36 months, and minimum period is 12, then all remaining interval at the beginning
            or end which has more than 12 months will all be taken into account.
        MAR is the minimum acceptable return, used for calculating the excess return 
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format
        order is the number of partial moment, int format    
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the sortino ratio dataframe for target index across differnt year length
    '''
    sub_dataframe = dataframe[columns_name].loc[start_gap:]
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))
    sortino_ratio_df = pd.DataFrame(columns = columns_name)
    for j in columns_name:
        sortino_ratio_df[j] = sub_dataframe[j].rolling(window_length, min_periods).apply(lambda x: (np.prod(1+x)**(1/window_length) - (1+MAR)) * 12 / np.sqrt(r.lpm(x, threshold, order)))[min_periods-1:].values
        # sortino_ratio_df[j] = sub_dataframe[j].rolling(window_length, min_periods).apply(lambda x: np.sqrt(r.lpm(x, threshold, order)))[min_periods-1:]
    sortino_ratio_df.index = dataframe.loc[(min_periods+start_gap-1):,'Date'].values
    # Format decimal point and dataframe name
    sortino_ratio_df = np.round(sortino_ratio_df, decimals=3)
    sortino_ratio_df.name = '36 Month Rolling Sortino Ratio'
    return sortino_ratio_df

def rolling_omega_ratio(dataframe, columns_name, window_length, min_periods, start_gap, MAR):
    '''Calculate the rolling omega ratio of target index. Omega ratio is the integral(here we use discrete sum) of return that 
    is larger than MAR divided by integral of return that is smaller than MAR

    Args:
        dataframe is the dataframe passed by concat_data() function
        columns_name is the index we want to calculate, which also include the market index
            must be consistent with index name in the excel sheet
        window_length is the window time you want to take into account. If you want to check 1 year rolling sortino ratio,
            it should be 12, if checking the whole period, it should be 109.
        min_periods is the minimum period that you could take into account and make calculation. For example,
            if you set time window to be 36 months, and minimum period is 12, then all remaining interval at the beginning
            or end which has more than 12 months will all be taken into account.
        MAR is the minimum acceptable return, used for calculating the excess return
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the sortino ratio dataframe for target index across differnt year length
    '''   
    sub_dataframe = dataframe[columns_name].loc[start_gap:]
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))    
    omega_ratio_df = pd.DataFrame(columns = columns_name)
    for j in columns_name:
        omega_ratio_df[j] = sub_dataframe[j].rolling(window_length, min_periods).apply(lambda x: (sum(x[x>MAR]-MAR**(1/12))/-sum(x[x<MAR]-MAR**(1/12))))[min_periods-1:].values
    omega_ratio_df.index = dataframe.loc[(min_periods+start_gap-1):,'Date'].values
    # Format decimal point and dataframe name
    omega_ratio_df = np.round(omega_ratio_df, decimals=3)
    omega_ratio_df.name = '36 Month Rolling Omega Ratio'
    return omega_ratio_df
                                       
                                           
def rolling_sharpe_ratio(dataframe,columns_name,window_length,min_periods,start_gap,benchmark):
    '''Calculate the rolling sharpe ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        columns_name is the index we want to calculate, which also include the market index
            must be consistent with index name in the excel sheet
        window_length is the window time you want to take into account. If you want to check 1 year rolling sharp ratio,
            it should be 12, if checking the whole period, it should be 109.
        min_periods is the minimum period that you could take into account and make calculation. For example,
            if you set time window to be 36 months, and minimum period is 12, then all remaining interval at the beginning
            or end which has more than 12 months will all be taken into account.
        benchmark is the value of risk free return, used for calculating the excess return 
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the sharp ratio dataframe for target index across differnt year length
    '''
    sub_dataframe = dataframe[columns_name].loc[start_gap:]
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))
    sharpe_ratio_df = pd.DataFrame(columns = columns_name)
    for j in columns_name:
        sharpe_ratio_df[j] = sub_dataframe[j].rolling(window_length, min_periods).apply(lambda x: np.mean(x - (1+benchmark) ** (1/12) + 1) * 12 / (r.vol_p(x - (1+benchmark) ** (1/12) + 1) * np.sqrt(12)))[min_periods-1:].values
    sharpe_ratio_df.index = dataframe.loc[(min_periods+start_gap-1):,'Date'].values
    # Format decimal point and dataframe name
    sharpe_ratio_df = np.round(sharpe_ratio_df, decimals=3)
    sharpe_ratio_df.name = '36 Month Rolling Sharpe Ratio'
    return sharpe_ratio_df

def rolling_alpha(dataframe,columns_name,window_length,min_periods,start_gap):
    '''Calculate the rolling alpha of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        columns_name is the index we want to calculate, which also include the market index
            must be consistent with index name in the excel sheet
        window_length is the window time you want to take into account. If you want to check 1 year rolling sharp ratio,
            it should be 12, if checking the whole period, it should be 109.
        min_periods is the minimum period that you could take into account and make calculation. For example,
            if you set time window to be 36 months, and minimum period is 12, then all remaining interval at the beginning
            or end which has more than 12 months will all be taken into account.
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the alpha dataframe for target index across differnt year length
    '''    
    rolling_beta_df = rolling_beta(dataframe, columns_name, window_length, min_periods, start_gap)
    sub_dataframe = dataframe[columns_name].loc[start_gap:]
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))    
    alpha_df = pd.DataFrame(columns = columns_name[0:3])
    # Generate  predicted number with beta and market index mean (russell 3000)
    for j in columns_name[0:3]: 
        alpha_df[j] = sub_dataframe[j].rolling(window_length, min_periods).mean()[min_periods-1:].values \
            - sub_dataframe['Russell 3000'].rolling(window_length, min_periods).mean()[min_periods-1:].values * rolling_beta_df[j].values
    alpha_df.index = dataframe.loc[(min_periods+start_gap-1):,'Date'].values    
    # Get the annulized alpha
    alpha_df = (alpha_df + 1)**12 - 1
    # Format decimal point and dataframe name
    alpha_df = np.round(alpha_df, decimals=3)
    alpha_df.name = '36 Month Rolling Annual Alpha'           
    return alpha_df

def rolling_corr(dataframe,columns_name,target_benchmark,window_length,min_periods,start_gap):
    '''Calculate the rolling correlation of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        columns_name is the index we want to calculate, which also include the market index
            must be consistent with index name in the excel sheet
        window_length is the window time you want to take into account. If you want to check 1 year rolling sharp ratio,
            it should be 12, if checking the whole period, it should be 109.
        min_periods is the minimum period that you could take into account and make calculation. For example,
            if you set time window to be 36 months, and minimum period is 12, then all remaining interval at the beginning
            or end which has more than 12 months will all be taken into account.
        target_benchmark is the target index you want to check with the correlation. Generally, it is market index (Russell 3000) 
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the correlation dataframe for target index across differnt year length
    '''    
    sub_dataframe = dataframe[columns_name].loc[start_gap:] # skip the start gap
    sub_dataframe.index = list(range(0,len(sub_dataframe.index),1))
    corr_df = pd.DataFrame(index = range(len(sub_dataframe.index)-min_periods+1), columns = [columns_name[0:3]])
    corr_df = sub_dataframe.rolling(window_length, min_periods).corr(sub_dataframe[target_benchmark])[min_periods-1:]
    corr_df.index = dataframe.loc[(min_periods+start_gap-1):,'Date'].values
    # Format decimal point and dataframe name
    corr_df = np.round(corr_df, decimals=3)
    corr_df.name = '36 Month Rolling Corr'
    return corr_df

def draw_down(dataframe, columns_name, start_gap):
    '''Give the drawdown dataframe with 100 highest hurdle
    
    Args:
        dataframe is the dataframe passed by concat_data() function
        columns_name is the index we want to calculate, which also include the market index
            must be consistent with index name in the excel sheet        
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap 
    
    Returns:
        This method give the dataframe which contains all cummulative return drawdown below 100
    '''
    return_df = dataframe[columns_name]+1
    cum_df = pd.DataFrame(columns=columns_name, index=dataframe['Date'])
    cum_df.iloc[0,:] = return_df.iloc[0,:]
    for i in range(1,len(return_df),1):
        for j in range(len(columns_name)):
            cum_df.iloc[i,j] = min(cum_df.iloc[i-1,j] * return_df.iloc[i,j],1)
    cum_df = cum_df[start_gap:]
    # Format decimal point and dataframe name
    cum_df = np.round(cum_df, decimals=3)
    cum_df.name = 'draw_down'
    return cum_df
    