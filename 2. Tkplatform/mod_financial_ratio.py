# -*- coding: utf-8 -*-
"""
Module for genearal financial ratio, and output is in dataframe format

@author: ZFang
"""

import pandas as pd
import numpy as np



def annulized_return(dataframe, index_name, smallest_interval, biggest_interval, interval, start_gap):
    '''Calcuate annulized return and output the table for given time interval
    
    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        smallest_interval is the smallest yearly interval, int format
        biggest_interval is the biggest yearly interval, int format
        interval describe the gap, int format
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap

    Returns:
        A Dataframe with given index name as row names, given time interval as column names, annulized return as the cell value
    '''
    Annulized_Return_df = pd.DataFrame(index = index_name)
    for i in range(smallest_interval,biggest_interval+1,interval):
        for j in index_name:
            Annulized_Return_df.loc[j,'%d_Year' % i] = np.prod(dataframe[j].iloc[-12*i:]+1)**(1/i) - 1
    for j in index_name:
        Annulized_Return_df.loc[j,'Since Inception'] = np.prod(dataframe[j]+1)**(12/(len(dataframe[j])-start_gap)) - 1
    # Format decimal point and dataframe name
    Annulized_Return_df = np.round(Annulized_Return_df, decimals=3)
    Annulized_Return_df.name = 'Annualized Return'
    return Annulized_Return_df

def calendar_return(dataframe, index_name, start_year, end_year, interval):
    '''Calculate the calendar return across all calendar years

    2007 has last six months data, they calendar return for 2007 is the last six month cumulative return.

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        smallest_interval is the smallest yearly interval, int format
        biggest_interval is the biggest yearly interval, int format
        interval describe the gap, int format

    Returns:
        A Dataframe with given index name as row names, given time interval as column names, calendar return as the cell value    
    '''
    Calendar_Return_df = pd.DataFrame(index = index_name)
    for i in range(start_year, end_year+1, interval):
        for j in index_name:
            Calendar_Return_df.loc[j,i] = np.prod(dataframe[j][dataframe['Year']==i]+1) - 1
    for j in index_name:
        Calendar_Return_df.loc[j,'YTD'] = np.prod(dataframe[j][dataframe['Year']==max(dataframe['Year'])]+1) - 1
    # Format decimal point and dataframe name
    Calendar_Return_df = np.round(Calendar_Return_df, decimals=3)
    Calendar_Return_df.name = 'Calendar Return'
    return Calendar_Return_df

def downside_std(dataframe, index_name, smallest_interval, biggest_interval, interval, threshold, order, start_gap):
    ''' Calculate a lower partial moment of the returns given threshold and order

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        smallest_interval is the smallest yearly interval, int format
        biggest_interval is the biggest yearly interval, int format
        interval describe the gap, int format
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format
        order is the number of partial moment, int format    
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap

    Returns:
        A Dataframe with given index name as row names, given time interval as column names, downside deviation as the cell value 
    '''
    Downside_std_df = pd.DataFrame(index = index_name)
    for j in index_name:
        for i in range(smallest_interval,biggest_interval+1,interval):
            returns = dataframe[j].iloc[-12*i:]
            # Create an array he same length as returns containing the minimum return threshold
            threshold_array = np.empty(len(returns)) 
            threshold_array.fill(threshold)
            # Calculate the difference between the threshold and the returns
            diff = threshold_array - returns
            # Set the minimum of each to 0
            diff = np.clip(diff,0,10000)
            # Return the sum of the different to the power of order
            Downside_std_df.loc[j,'%d_Year' % i] = np.sqrt(np.sum(diff ** order) / len(returns)) * np.sqrt(12)
    for j in index_name:
        returns = dataframe[j]
        threshold_array = np.empty(len(returns))
        threshold_array.fill(threshold)
        # Calculate the difference between the threshold and the returns
        diff = threshold_array - returns
        # Set the minimum of each to 0
        diff = np.clip(diff,0,10000)
        Downside_std_df.loc[j,'Since Inception'] = np.sqrt(np.sum(diff ** order) / (len(returns)-start_gap)) * np.sqrt(12)
    # Format decimal point and dataframe name
    Downside_std_df = np.round(Downside_std_df, decimals=3)
    Downside_std_df.name = 'Downside Deviation'
    return Downside_std_df

def lpm(returns, threshold, order):
    '''This method returns a lower partial moment of the returns
    
    Args:
        returns is the pandas.series of return we want to calculate
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format
        order is the number of partial moment, int format    
        
    Returns:
        This method return the lower partial moment of given return series
    '''
    # Create an array he same length as returns containing the minimum return threshold
    threshold_array = np.empty(len(returns))
    threshold_array.fill(threshold)
    # Calculate the difference between the threshold and the returns
    diff = threshold_array - returns
    # Set the minimum of each to 0
    diff = np.clip(diff,0,10000)
    # Return the sum of the different to the power of order
    return np.sum(diff ** order) / len(returns) * 12

def vol_s(returns):
    '''Return the sample standard deviation of returns

    Args:
        returns is the pandas.series of return we want to calculate

    '''
    return np.std(returns, ddof = 1)

def vol_p(returns):
    '''Return the population standard devi foration of returns

    Args:
        returns is the pandas.series of re forturn we want to calculate
    '''
    return np.std(returns)

def sortino_ratio(dataframe, index_name, smallest_interval, biggest_interval, interval, MAR, threshold, order, start_gap):
    '''Calculate the sortino ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        smallest_interval is the smallest yearly interval, int format
        biggest_interval is the biggest yearly interval, int format
        interval describe the gap, int format
        MAR is the minimum acceptable return, used for calculating the excess return 
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format
        order is the number of partial moment, int format    
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the sortino ratio dataframe for target index across differnt year length
    '''
    Sortino_df = pd.DataFrame(index = index_name)
    for j in index_name:
        for i in range(smallest_interval, biggest_interval+1, interval):
            period_excess_returns = np.prod(dataframe[j].iloc[-12*i:]+1)**(1/(i*12)) - (1+MAR)
            # excess_returns = np.clip(excess_returns,0,10000)
            returns = dataframe[j].iloc[-12*i:]
            Sortino_df.loc[j,'%d_Year' % i] = period_excess_returns * 12 / np.sqrt(lpm(returns, threshold, order))
    for j in index_name:
        period_excess_returns = np.prod(dataframe.loc[start_gap:,j]+1)**(1/(len(dataframe[j])-start_gap)) - (1+MAR)
        # excess_returns = np.clip(excess_returns,0,10000)
        returns = dataframe.loc[start_gap:,j]
        Sortino_df.loc[j,'Since Inception'] = period_excess_returns * 12 / np.sqrt(lpm(returns, threshold, order))
    # Format decimal point and dataframe name
    Sortino_df = np.round(Sortino_df, decimals=3)
    Sortino_df.name = 'Sortino Ratio'
    return Sortino_df
    
    
    
def sharpe_ratio(dataframe, index_name, smallest_interval, biggest_interval, interval, benchmark, start_gap):
    '''Calculate the sharpe ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        smallest_interval is the smallest yearly interval, int format
        biggest_interval is the biggest yearly interval, int format
        interval describe the gap, int format
        benchmark is the value of risk free return, used for calculating the excess return
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the sharpe ratio dataframe for target index across differnt year length
    '''    
    Sharpe_df = pd.DataFrame(index = index_name)
    for j in index_name:
        for i in range(smallest_interval, biggest_interval+1, interval):
            excess_returns = dataframe[j].iloc[-12*i:] - (1+benchmark) ** (1/12) + 1
            Sharpe_df.loc[j,'%d_Year' % i] = np.mean(excess_returns) * 12 / (vol_p(excess_returns) * np.sqrt(12))
    for j in index_name:
        excess_returns = dataframe.loc[start_gap:,j] - (1+benchmark) ** (1/12) + 1 # pay attention to first six month gap
        Sharpe_df.loc[j,'Since Inception'] = np.mean(excess_returns) * 12 / (vol_p(excess_returns) * np.sqrt(12))
    # Format decimal point and dataframe name
    Sharpe_df = np.round(Sharpe_df, decimals=3)
    Sharpe_df.name = 'Sharpe Ratio'
    return Sharpe_df

def standard_deviation(dataframe, index_name, smallest_interval, biggest_interval, interval, start_gap):
    '''Calculate the standard deviation of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        smallest_interval is the smallest yearly interval, int format
        biggest_interval is the biggest yearly interval, int format
        interval describe the gap, int format
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the standard devation dataframe for target index across differnt year length  
    '''  
    Stv_df = pd.DataFrame(index = index_name)
    for j in index_name:
        for i in range(smallest_interval, biggest_interval+1, interval):
            Stv_df.loc[j,'%d_Year' % i] = np.std(dataframe[j].iloc[-12*i:], ddof = 1) * np.sqrt(12)
    for j in index_name:
        Stv_df.loc[j,'Since Inception'] = np.std(dataframe.loc[start_gap:,j], ddof = 1) * np.sqrt(12) # pay attention to first six month gap
    # Format decimal point and dataframe name
    Stv_df = np.round(Stv_df, decimals=3)
    Stv_df.name = 'Standard Devation'
    return Stv_df


def beta_table(dataframe, index_name, market_index, smallest_interval, biggest_interval, interval, start_gap):
    '''Calculate the beta of target index with market index

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        market_index is the name of market index, which is used to regress with target index return. 
            The market index name should be consistent with the name in the excel sheet.
        smallest_interval is the smallest yearly interval, int format
        biggest_interval is the biggest yearly interval, int format
        interval describe the gap, int format
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the beta dataframe for target index with given market index across differnt year length  
    '''  
    beta_df = pd.DataFrame(index = index_name)
    for j in index_name:
        for i in range(smallest_interval, biggest_interval+1, interval):
            sub_dataframe = dataframe[[j,market_index]].iloc[-12*i:]
            beta_df.loc[j,'%d_Year' % i] = beta(sub_dataframe)
    for j in index_name:
        sub_dataframe = dataframe[[j,market_index]].loc[start_gap:] # pay attention to first six month gap
        beta_df.loc[j,'Since Inception'] = beta(sub_dataframe)
    # Format decimal point and dataframe name
    beta_df = np.round(beta_df, decimals=3)
    beta_df.name = 'Beta (Russell 3000)'
    return beta_df

def beta(sub_dataframe):
    '''Calculate specific beta value given two series of return in a dataframe format

    Args:
        sub_dataframe should be a dataframe that has two columns, the first column is target index, 
            the second one is market index
    Returns:
        This function return the beta value for specific target index and market index
    '''
    index = sub_dataframe.iloc[:,0].values
    mkt = sub_dataframe.iloc[:,1].values
    m = np.matrix([index,mkt])
    beta_value = np.cov(m)[0][1]/np.cov(m)[1][1]
    return beta_value

def omega_ratio(dataframe, index_name, smallest_interval, biggest_interval, interval, MAR, threshold, order, start_gap):
    '''Calculate the Omega ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        smallest_interval is the smallest yearly interval, int format
        biggest_interval is the biggest yearly interval, int format
        interval describe the gap, int format
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format
        order is the number of partial moment, here is one, int format    
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return the Omega ratio dataframe for target index across differnt year length
    '''
    Omega_df = pd.DataFrame(index = index_name)
    for j in index_name:
        for i in range(smallest_interval, biggest_interval+1, interval):
            Omega_df.loc[j,'%d_Year' % i] = sum(dataframe[j].iloc[-12*i:][dataframe[j].iloc[-12*i:]>MAR]-MAR**(1/12))/-sum(dataframe[j].iloc[-12*i:][dataframe[j].iloc[-12*i:]<MAR]-MAR**(1/12))
    for j in index_name:
        Omega_df.loc[j,'Since Inception'] = sum(dataframe[j].iloc[start_gap:][dataframe[j].iloc[start_gap:]>MAR]-MAR**(1/12))/-sum(dataframe[j].iloc[start_gap:][dataframe[j].iloc[start_gap:]<MAR]-MAR**(1/12))
    # Format decimal point and dataframe name
    Omega_df = np.round(Omega_df, decimals=3)
    Omega_df.name = 'Omega Ratio'
    return Omega_df

def summary_table(dataframe, index_name, columns, market_index, MAR, threshold, order, start_gap):
    '''Give the summary table for target index and describe batting average, omega ratio, up months, 
    down months, slugging ratio, up-capture russell and down-capture russell

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        columns is the target ratio you want to cover, and generally it is fixed, because one-one formula
            was designed for each column
        market_index is the name of market index, which is used to regress with target index return. 
            The market index name should be consistent with the name in the excel sheet.
        benchmark is the value of risk free return, used for calculating the excess return 
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format
        order is the number of partial moment, int format    
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return a summary table which cover the major ratio
    '''
    Summary_df = pd.DataFrame(index = index_name, columns = columns)
    for j in index_name:
        # returns = dataframe[j]
        Summary_df.loc[j,'Batting Average'] = 100 * sum(dataframe[j]>0)/(len(dataframe[j]) - start_gap)
        Summary_df.loc[j,'Omega Ratio'] = sum(dataframe[j].iloc[start_gap:][dataframe[j].iloc[start_gap:]>MAR])/abs(sum(dataframe[j].iloc[start_gap:][dataframe[j].iloc[start_gap:]<MAR]))
        Summary_df.loc[j,'Up Months'] = sum(dataframe[j]>0)
        Summary_df.loc[j,'Down Months'] = sum(dataframe[j]<0)
        Summary_df.loc[j,'Slugging Ratio'] = np.mean(dataframe[j][dataframe[j]>0]) / -np.mean(dataframe[j][dataframe[j]<0])
        Summary_df.loc[j,'Up-Capture Russell'] = 100 * np.mean(dataframe[j][dataframe[market_index]>0])/np.mean(dataframe[market_index][dataframe[market_index]>0])
        Summary_df.loc[j,'Down-Capture Russell'] = 100 * np.mean(dataframe[j][dataframe[market_index]<0])/np.mean(dataframe[market_index][dataframe[market_index]<0])
    # Format decimal point and dataframe name
    Summary_df = np.round(Summary_df, decimals=3)
    Summary_df.name = 'Summary Table'
    return Summary_df