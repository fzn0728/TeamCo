# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:26:55 2016

@author: ZFang
"""
import numpy as np
import mod_financial_ratio as r
import mod_rolling as m
import mod_input_output as put
import mod_plot as p
import os
import pandas as pd


os.getcwd()
# Set working directory
data_file_path = r'C:\Users\ZFang\Desktop\TeamCo\Financial Ratio\\'
os.chdir(data_file_path)


# for testing
# df_data = put.concat_data('test_data.xlsx')
# dataframe = df_data[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']]
# dataframe_b = df_data[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index', 'Russell 3000']]
# target_mkt_index = ['Russell 3000']

def get_year_list(dataframe):
    max_len = dataframe.iloc[:,1:].notnull().sum(axis=0).max()
    year_list = [12,36,60,84,120,180]
    update_year_list = year_list[:sum(max_len>year_list)]
    return update_year_list


def annulized_return(dataframe):
    '''Give dataframe and return all possible annulized return
    
    Args:
        dataframe is the dataframe passed by concat_data() function or any return table, with index name as column name
    
    Returns:
        Dataframe of annualized return
    '''
    year_list = [12,36,60,84,120,180]
    annual_r_df = pd.DataFrame(index = dataframe.columns)
    # Force all nan in dataframe to be np.nan
    dataframe = dataframe.fillna(np.nan)
    # Calculation for static year
    for i in year_list:
        annual_r_df['%d_Months' % i] = np.prod(np.array(dataframe.iloc[-i:]+1)**(12/i), axis=0) - 1
    # Calculation for Inception time
    for j in dataframe.columns:
        Inception = int(np.count_nonzero(~np.isnan(dataframe[j])))
        annual_r_df.loc[j,'Since Inception'] = np.prod(np.array(dataframe[j].iloc[-Inception:]+1)**(12/Inception), axis=0) - 1
    return annual_r_df



def calendar_return(dataframe):
    # Force all nan in dataframe to be np.nan
    dataframe = dataframe.fillna(np.nan)
    
    dataframe = dataframe+1
    dataframe.index = pd.DatetimeIndex(dataframe['Date'])
    Calendar_Return_df = (dataframe.resample('A').prod())-1
    Calendar_Return_df = Calendar_Return_df.transpose()
    Calendar_Return_df.columns = Calendar_Return_df.columns.year
    return Calendar_Return_df


def downside_std(dataframe, threshold):
    ''' Calculate the downside standard deviation given dataframe and threshold

    Args:
        dataframe is the dataframe passed by concat_data() function
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format
        year_list is the initial global variable which defines the typical year label for static table output

    Returns:
        A Dataframe with given index name as row names, given time interval as column names, downside deviation as the cell value 
    '''
    year_list = [12,36,60,84,120,180]
    Downside_std_df = pd.DataFrame(index = dataframe.columns)
    # Force all nan in dataframe to be np.nan
    dataframe = dataframe.fillna(np.nan)
    # Calculation for static year
    for i in year_list:
        returns = dataframe.iloc[-i:]
        # Create an array he same length as returns containing the minimum return threshold
        threshold_array = np.empty(np.shape(returns)) 
        threshold_array.fill(threshold)
        # Calculate the difference between the threshold and the returns
        diff = threshold - returns
        # Set the minimum of each to 0
        diff = np.clip(diff,0,10000)
        # Return the sum of the different to the power of order
        Downside_std_df['%d_Months' % i] = np.sqrt(np.sum(np.array(diff ** 2), axis = 0) / len(returns)) * np.sqrt(12) 
    # Calculation for Inception time
    for j in dataframe.columns:
        Inception = int(np.count_nonzero(~np.isnan(dataframe[j])))
        returns = dataframe[j].iloc[-Inception:]
        threshold_array = np.empty(len(returns))
        threshold_array.fill(threshold)
        diff = threshold - returns
        diff = np.clip(diff,0,10000)
        Downside_std_df.loc[j,'Since Inception'] = np.sqrt(np.sum(np.array(diff ** 2), axis = 0) / len(returns)) * np.sqrt(12) 
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
    returns = returns.fillna(np.nan)
    # Create an array he same length as returns containing the minimum return threshold
    threshold_array = np.empty(np.shape(returns))
    threshold_array.fill(threshold)
    # Calculate the difference between the threshold and the returns
    diff = threshold_array - returns
    # Set the minimum of each to 0
    diff = np.clip(diff,0,10000)
    # Return the sum of the different to the power of order
    return np.sum(np.array(diff ** order), axis=0) / len(returns) * 12

def sharpe_ratio(dataframe, benchmark):
    '''Calculate the sharpe ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        benchmark is the value of risk free return, used for calculating the excess return

    Returns:
        This method return the sharpe ratio dataframe for target index across differnt year length
    '''
    year_list = [12,36,60,84,120,180]
    Sharpe_df = pd.DataFrame(index = dataframe.columns)
    # Force all nan in dataframe to be np.nan
    dataframe = dataframe.fillna(np.nan)
    # Calculation
    for i in year_list:
        excess_returns = np.array(dataframe.iloc[-i:]) - (1+benchmark) ** (1/12) + 1
        Sharpe_df['%d_Months' % i] = np.mean(excess_returns, axis=0) * 12 / (np.std(excess_returns, axis=0) * np.sqrt(12))
    for j in dataframe.columns:
        Inception = int(np.count_nonzero(~np.isnan(dataframe[j])))  
        excess_returns = dataframe[j].iloc[-Inception:] - (1+benchmark) ** (1/12) + 1 # pay attention to first six month gap
        Sharpe_df.loc[j,'Since Inception'] = np.mean(excess_returns) * 12 / (np.std(excess_returns) * np.sqrt(12))
    return Sharpe_df
    
    
def sortino_ratio(dataframe, threshold, MAR):
    '''Calculate the sortino ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        MAR is the minimum acceptable return, used for calculating the excess return 
        threshold is the value of threshold for downside deviation calculation, normally is zero, int format

    Returns:
        This method return the sortino ratio dataframe for target index across differnt year length
    '''
    year_list = [12,36,60,84,120,180]
    Sortino_df = pd.DataFrame(index = dataframe.columns)
    # Force all nan in dataframe to be np.nan
    dataframe = dataframe.fillna(np.nan)
    # Calculation
    for i in year_list:
        period_excess_returns = np.array(np.prod(dataframe.iloc[-i:]+1, axis=0)**(1/i) - (1+MAR)**(1/12))
        returns = dataframe.iloc[-i:]
        Sortino_df['%d_Months' % i] = period_excess_returns * 12 / np.sqrt(lpm(returns, threshold, 2))
    for j in dataframe.columns:
        Inception = int(np.count_nonzero(~np.isnan(dataframe[j])))  
        period_excess_returns = np.array(np.prod(dataframe[j].iloc[-Inception:]+1, axis=0)**(1/(Inception)) - (1+MAR)**(1/12))
        # excess_returns = np.clip(excess_returns,0,10000)
        returns = dataframe[j].iloc[-Inception:]
        Sortino_df.loc[j,'Since Inception'] = period_excess_returns * 12 / np.sqrt(lpm(returns, threshold, 2))
    # Format dataframe name
    Sortino_df.name = 'Sortino Ratio'
    return Sortino_df
    
def standard_deviation(dataframe):
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
    year_list = [12,36,60,84,120,180]
    Stv_df = pd.DataFrame(index = dataframe.columns)
    # Force all nan in dataframe to be np.nan
    dataframe = dataframe.fillna(np.nan)
    # Calculation
    for i in year_list:
        Stv_df['%d_Months' % i] = np.std(np.array(dataframe.iloc[-i:]), ddof=1, axis=0) * np.sqrt(12)
    for j in dataframe.columns:
        Inception = int(np.count_nonzero(~np.isnan(dataframe[j]))) 
        Stv_df.loc[j,'Since Inception'] = np.array(np.std(dataframe[j].iloc[-Inception:], ddof = 1, axis=0)) * np.sqrt(12)
    return Stv_df


def beta(dataframe_b,condition = None):
    '''Calculate specific beta value given two series of return in a dataframe format

    Args:
        dataframe_b should be a dataframe that has many columns, the first several columns could be target index, 
            the last one must be market index
    Returns:
        This function return the beta value for specific target index and market index
    '''
    year_list = [12,36,60,84,120,180]
    Beta_df = pd.DataFrame(index = dataframe_b.columns)
    # Force all nan in dataframe to be np.nan
    dataframe_b = dataframe_b.fillna(np.nan)
    
    if condition == None:
        for i in year_list:
            mm = np.matrix(dataframe_b.iloc[-i:,:])
            ma = np.cov(mm, rowvar=False)
            beta_value = ma[:,-1]/ma[-1,-1]
            Beta_df['%d_Months' % i] = beta_value
        for j in dataframe_b.columns:
            Inception = min(int(np.count_nonzero(~np.isnan(dataframe_b[j]))),int(np.count_nonzero(~np.isnan(dataframe_b['Russell 3000']))))
            mm = np.matrix(dataframe_b[[j,'Russell 3000']].iloc[-Inception:])
            ma = np.cov(mm, rowvar=False)
            beta_value = ma[0,1]/ma[1,1]
            Beta_df.loc[j,'Since Inception'] = beta_value
    elif condition == 'Positive':
        for j in dataframe_b.columns:
            Inception = min(int(np.count_nonzero(~np.isnan(dataframe_b[j]))),int(np.count_nonzero(~np.isnan(dataframe_b['Russell 3000']))))
            mm = np.matrix(dataframe_b[[j,'Russell 3000']].iloc[-Inception:][dataframe_b['Russell 3000']>0])
            ma = np.cov(mm, rowvar=False)
            beta_value = ma[0,1]/ma[1,1]
            Beta_df.loc[j,'Since Inception'] = beta_value
    elif condition == 'Non-positive':
        for j in dataframe_b.columns:
            Inception = min(int(np.count_nonzero(~np.isnan(dataframe_b[j]))),int(np.count_nonzero(~np.isnan(dataframe_b['Russell 3000']))))
            mm = np.matrix(dataframe_b[[j,'Russell 3000']].iloc[-Inception:][dataframe_b['Russell 3000']<=0])
            ma = np.cov(mm, rowvar=False)
            beta_value = ma[0,1]/ma[1,1]
            Beta_df.loc[j,'Since Inception'] = beta_value        
    return Beta_df

    
    
def omega_ratio(dataframe, MAR):
    '''Calculate the Omega ratio of target index

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        MAR is the minimum acceptable return, used for calculating the excess return 
        order is the number of partial moment, here is one, int format    
        start_gap is the gap at the beginning of the data, which is a six month blank period without. 
            the value is defined by a global variable start_gap
        year_list is the initial global variable which defines the typical year label for static table output
        end_point is given by get_end_year function, which is the biggest list year in the table [1,3,5,7,10,15]

    Returns:
        This method return the Omega ratio dataframe for target index across differnt year length
    '''
    year_list = [12,36,60,84,120,180]
    Omega_df = pd.DataFrame(index = dataframe.columns)
    # Force all nan in dataframe to be np.nan
    dataframe = dataframe.fillna(np.nan)
    # Calculation
    for i in year_list:
        for j in dataframe.columns:
            # Since np.nan+np.array cannot exclude the NaN scienairo,(due to the >MAR condition), we need to mannually check the NaN problem
            if np.prod(~pd.isnull(dataframe[j].iloc[-i:]))==0: 
                Omega_df.loc[j,'%d_Months' % i] = np.nan
            elif np.prod(~pd.isnull(dataframe[j].iloc[-i:]))!=0:
                Omega_df.loc[j,'%d_Months' % i] = np.sum(dataframe[j].iloc[-i:][dataframe[j].iloc[-i:]>MAR]-MAR**(1/12))\
                                            /-np.sum(dataframe[j].iloc[-i:][dataframe[j].iloc[-i:]<MAR]-MAR**(1/12))
    for j in dataframe.columns:
        Inception = int(np.count_nonzero(~np.isnan(dataframe[j])))
        Omega_df.loc[j,'Since Inception'] = np.sum(dataframe[j].iloc[-Inception:][dataframe[j].iloc[-Inception:]>MAR]-MAR**(1/12),axis=0)\
                                            /-np.sum(dataframe[j].iloc[-Inception:][dataframe[j].iloc[-Inception:]<MAR]-MAR**(1/12),axis=0)
    return Omega_df
    
def corr(dataframe_b, target_mkt_index, condition = None):
    '''Calculate the rolling correlation of target index, could do conditional analysis

    Args:
        dataframe is the dataframe passed by concat_data() function
        index_name is the index we want to calculate, must be consistent with index name in the excel sheet
        target_mkt_index is the target index you want to check with the correlation. Generally, it is market index (Russell 3000)  
        Condition(None, 'Positive','Non-positive') could do conditional analysis. For example, positive means for those period when market index is 
            positive, the correlation between market index and fund/competitor

            
    Returns:
        This method return the correlation dataframe for target index across differnt year length
    '''
    year_list = [12,36,60,84,120,180]
    corr_df = pd.DataFrame(index=dataframe_b.columns)
    # Calculation
    if condition == None:
        for i in year_list:
            corr_df['%d_Year' % i] = np.corrcoef(dataframe_b.iloc[-i:,:-1].values, \
                    dataframe_b[target_mkt_index].iloc[-i:].values, rowvar=0)[:,-1]
        for j in dataframe_b.columns:
            Inception = int(np.count_nonzero(~np.isnan(dataframe_b[j]))) 
            corr_df.loc[j,'Since Inception'] = np.corrcoef(dataframe_b[j].iloc[-Inception:].values, \
                    dataframe_b[target_mkt_index].iloc[-Inception:].values, rowvar=0)[0,1]
    elif condition == 'Positive':
        for j in dataframe_b.columns:
            Inception = int(np.count_nonzero(~np.isnan(dataframe_b[j]))) 
            corr_df.loc[j,'Positive Correaltion'] = np.corrcoef(dataframe_b[j].iloc[-Inception:][dataframe_b[target_mkt_index]>0].values, \
                    dataframe_b[target_mkt_index].iloc[-Inception:][dataframe_b[target_mkt_index]>0].values, rowvar=0)[0,1]        
    elif condition == 'Non-positive':
        for j in dataframe_b.columns:
            Inception = int(np.count_nonzero(~np.isnan(dataframe_b[j]))) 
            corr_df.loc[j,'Non-positive Correaltion'] = np.corrcoef(dataframe_b[j].iloc[-Inception:][dataframe_b[target_mkt_index]<=0].values, \
                    dataframe_b[target_mkt_index].iloc[-Inception:][dataframe_b[target_mkt_index]<=0].values, rowvar=0)[0,1]                
    # Format dataframe name
    corr_df.name = 'Correlation Table with %s Condition' %condition
    return corr_df
