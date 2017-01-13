# -*- coding: utf-8 -*-
"""
Module for genearal financial ratio, and output is in dataframe format

@author: ZFang
"""

import pandas as pd
import numpy as np
import mod_basic_fin_ratio as ba




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


def annulized_return_table(dataframe, index_name, target_year):
    '''Calcuate annulized return and output the table for given time interval
    
    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap
        target_year is the target column picked up by names we want to show on the final output table
        

    Returns:
        A Dataframe with given index name as row names, given time interval as column names, annulized return as the cell value
    '''
    # Calculation
    sub_dataframe = dataframe.loc[:,index_name]
    Annulized_Return_df = ba.annulized_return(sub_dataframe)
    # Format dataframe
    Annulized_Return_df.columns = ['1_Year','3_Year','5_Year','7_Year','10_Year','15_Year','Since Inception']
    Annulized_Return_df = Annulized_Return_df[target_year]
    Annulized_Return_df.name = 'Annualized Return'
    return Annulized_Return_df

def calendar_return_table(dataframe, index_name_2):
    '''Calculate the calendar return across all calendar years
    2007 has last six months data, they calendar return for 2007 is the last six month cumulative return.

    Args:
        dataframe is the dataframe passed by concat_data() function

    Returns:
        A Dataframe with given index name as row names, given time interval as column names, calendar return as the cell value    
    '''
    # Select target columns
    dataframe = dataframe.loc[:,index_name_2]
    # Calculation
    Calendar_Return_df = ba.calendar_return(dataframe) 
    # Format and dataframe name
    Calendar_Return_df.name = 'Calendar Return'
    return Calendar_Return_df

def downside_std_table(dataframe, index_name, threshold, target_year):
    ''' Calculate a lower partial moment of the returns given threshold and order

    Args:
        dataframe is the dataframe passed by concat_data() function
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format
        target_year is the target column picked up by names we want to show on the final output table

    Returns:
        A Dataframe with given index name as row names, given time interval as column names, downside deviation as the cell value 
    '''
    # Calculation
    dataframe = dataframe.loc[:,index_name]
    Downside_std_df = ba.downside_std(dataframe, threshold)
    # Format dataframe
    Downside_std_df.columns = ['1_Year','3_Year','5_Year','7_Year','10_Year','15_Year','Since Inception']
    Downside_std_df = Downside_std_df[target_year]
    Downside_std_df.name = 'Downside Deviation'
    return Downside_std_df


def sharpe_ratio_table(dataframe, index_name, benchmark, target_year):
    ''' Calculate the sharpe ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        benchmark is the value of risk free return, used for calculating the excess return

    Returns:
        This method return the sharpe ratio dataframe for target index across differnt year length
    '''
    # Calculation
    dataframe = dataframe.loc[:,index_name]
    Sharpe_df = ba.sharpe_ratio(dataframe, benchmark)
    # Format dataframe
    Sharpe_df.columns = ['1_Year','3_Year','5_Year','7_Year','10_Year','15_Year','Since Inception']
    Sharpe_df = Sharpe_df[target_year]    
    Sharpe_df.name = 'Sharpe Ratio'
    return Sharpe_df



def sortino_ratio_table(dataframe, index_name, MAR, threshold, target_year):
    '''Calculate the sortino ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        MAR is the minimum acceptable return, used for calculating the excess return 
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format

    Returns:
        This method return the sortino ratio dataframe for target index across differnt year length
    '''
    # Calculation
    dataframe = dataframe.loc[:,index_name]
    Sortino_df = ba.sortino_ratio(dataframe, threshold, MAR)
    # Format dataframe
    Sortino_df.columns = ['1_Year','3_Year','5_Year','7_Year','10_Year','15_Year','Since Inception']
    Sortino_df = Sortino_df[target_year]  
    Sortino_df.name = 'Sortino Ratio'
    return Sortino_df
    

def standard_deviation_table(dataframe, index_name, target_year):
    '''Calculate the standard deviation of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap
        year_list is the initial global variable which defines the typical year label for static table output
        end_point is given by get_end_year function, which is the biggest list year in the table [1,3,5,7,10,15]

    Returns:
        This method return the standard devation dataframe for target index across differnt year length  
    '''  
    # Calculation
    dataframe = dataframe.loc[:,index_name]
    Stv_df = ba.standard_deviation(dataframe)
    # Format dataframe
    Stv_df.columns = ['1_Year','3_Year','5_Year','7_Year','10_Year','15_Year','Since Inception']
    Stv_df = Stv_df[target_year] 
    Stv_df.name = 'Standard Devation'
    return Stv_df


def beta_table(dataframe, index_name_3, target_year, condition = None):
    '''Calculate the beta of target index with market index, could do conditional analysis

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name_3 is the index we want to calculate, must be consistent with index name in the excel sheet, the last column
            must be market index
        Condition(None, 'Positive','Non-positive') could do conditional analysis. For example, positive means for those period when market index is 
            positive, the correlation between market index and fund/competitor

    Returns:
        This method return the beta dataframe for target index with given market index across differnt year length  
    '''
    # Calculation
    dataframe = dataframe.loc[:,index_name_3]
    beta_df = ba.beta(dataframe,condition)    
    # Format dataframe
    if condition is None:
        beta_df.columns = ['1_Year','3_Year','5_Year','7_Year','10_Year','15_Year','Since Inception']
        beta_df = beta_df[target_year]
    beta_df = beta_df.iloc[:-1,:] # Delete the last column of market index
    beta_df.name = 'Beta (Russell 3000) with %s Condition' %condition
    return beta_df


def omega_ratio_table(dataframe, index_name, MAR, target_year):
    '''Calculate the Omega ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        MAR is the minimum acceptable return, used for calculating the excess return 

    Returns:
        This method return the Omega ratio dataframe for target index across differnt year length
    '''
    # Calculation
    dataframe = dataframe.loc[:,index_name]
    Omega_df = ba.omega_ratio(dataframe, MAR)

    # Format dataframe
    Omega_df.columns = ['1_Year','3_Year','5_Year','7_Year','10_Year','15_Year','Since Inception']
    Omega_df = Omega_df[target_year] 
    Omega_df.name = 'Omega Ratio'
    return Omega_df

    
def corr_table(dataframe, index_name_3, target_mkt_index, target_year, condition):
    '''Calculate the rolling correlation of target index, could do conditional analysis

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name_3 is the index we want to calculate, must be consistent with index name in the excel sheet, the last column
            must be market index
        target_mkt_index is the target index you want to check with the correlation. Generally, it is market index (Russell 3000) 
        Condition(None, 'Positive','Non-positive') could do conditional analysis. For example, positive means for those period when market index is 
            positive, the correlation between market index and fund/competitor

    Returns:
        This method return the correlation dataframe for target index across differnt year length
    '''
    # Calculation
    dataframe = dataframe.loc[:,index_name_3]
    corr_df = ba.corr(dataframe, target_mkt_index, condition)
    
    # Format dataframe name
    if condition is None:
        corr_df.columns = ['1_Year','3_Year','5_Year','7_Year','10_Year','15_Year','Since Inception']
        corr_df = corr_df[target_year] 
    corr_df = corr_df.iloc[:-1,:] # Delete the last column of market index
    corr_df.name = 'Correlation Table with %s Condition' %condition
    return corr_df
    
    
def summary_table(dataframe, index_name, columns, market_index, MAR):
    '''Give the summary table for target index and describe batting average, omega ratio, up months, 
    down months, slugging ratio, up-capture russell and down-capture russell

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        columns is the target ratio you want to cover, and generally it is fixed, because one-one formula
            was designed for each column
        market_index is the name of market index, which is used to regress with target index return. 
            The market index name should be consistent with the name in the excel sheet
        MAR is the minimum acceptable return, used for calculating the excess return 
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap   

    Returns:
        This method return a summary table which cover the major ratio
    '''
    Summary_df = pd.DataFrame(index = index_name, columns = columns)
    for j in index_name:
        Inception = int(np.count_nonzero(~np.isnan(dataframe[j])))
        # returns = dataframe[j]
        Summary_df.loc[j,'Batting Average'] = 100 * sum(dataframe[j]>0)/Inception
        Summary_df.loc[j,'Omega Ratio'] = sum(dataframe[j].iloc[-Inception:][dataframe[j].iloc[-Inception:]>MAR])\
                                                /abs(sum(dataframe[j].iloc[-Inception:][dataframe[j].iloc[-Inception:]<MAR]))
        Summary_df.loc[j,'Up Months'] = sum(dataframe[j]>0)
        Summary_df.loc[j,'Down Months'] = sum(dataframe[j]<0)
        Summary_df.loc[j,'Slugging Ratio'] = np.mean(dataframe[j][dataframe[j]>0]) / -np.mean(dataframe[j][dataframe[j]<0])
        Summary_df.loc[j,'Up-Capture Russell'] = 100 * np.mean(dataframe[j][dataframe[market_index]>0])/np.mean(dataframe[market_index][dataframe[market_index]>0])
        Summary_df.loc[j,'Down-Capture Russell'] = 100 * np.mean(dataframe[j][dataframe[market_index]<0])/np.mean(dataframe[market_index][dataframe[market_index]<0])
    # Format dataframe name
    Summary_df.name = 'Summary Table'
    return Summary_df