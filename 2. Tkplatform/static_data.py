# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 08:46:35 2016

@author: ZFang
"""

import os
import mod_financial_ratio as r
import mod_rolling as m
import mod_input_output as i
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == '__main__':
    ### Change working directory
    # Get working directory
    os.getcwd()
    # Set working director
    data_file_path = r'C:\Users\ZFang\Desktop\TeamCo\Tkplatform\\'
    os.chdir(data_file_path)
    ### Define constant variable
    # The number of month at the beginning that has no available data
    # Since start from 2007, the first six months doesn't have performance data, 
    # I set the starting gap is 6 months
    start_gap = 6
    index_name = ('TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index')
    columns_name = ['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index', 'Russell 3000']
    ### Plotting stype
    
    ### Read the file
    df_data = i.concat_data('Fund Analysis.xlsx')
    ### Calculate Annulized Return
    Annulized_Return_df = r.annulized_return(df_data, index_name, 
        smallest_interval=1, biggest_interval=7, interval=2, start_gap=start_gap)
    ### Calculate Calendar Return
    Calendar_Return_df = r.calendar_return(df_data, index_name, 2007, 2015, 1)
    ### Calculate Downside Deviation, given order of two
    Downside_Deviation_df = r.downside_std(df_data, index_name, 
        smallest_interval=3, biggest_interval=7, interval=2, threshold=0, order=2, start_gap=start_gap)
    ### Calculate Sortino ratio
    Sortino_df = r.sortino_ratio(df_data, index_name, 
        smallest_interval=3, biggest_interval=7, interval=2, MAR=0, threshold=0, order=2, start_gap=start_gap)
    ### Calculate Sharp ratio
    Sharpe_df=r.sharpe_ratio(df_data, index_name, 
        smallest_interval=3, biggest_interval=7, interval=2, benchmark=0.02, start_gap=start_gap)
    ### Standard Deviation
    Standard_deviation_df = r.standard_deviation(df_data, index_name, 
        smallest_interval=3, biggest_interval=7, interval=2, start_gap=start_gap)
    ### Beta matrix
    Beta_df = r.beta_table(df_data, index_name, 
        market_index='Russell 3000',smallest_interval=3, biggest_interval=7, interval=2, start_gap=start_gap)
    ### Omega Ratio
    Omega_df = r.omega_ratio(df_data, index_name, 
        smallest_interval=3, biggest_interval=7, interval=2, MAR=0, threshold=0, order=1, start_gap=start_gap)
    ### Summary table
    Summary_table_df = r.summary_table(df_data,index_name, 
        columns=['Batting Average', 'Omega Ratio', 'Up Months', 'Down Months', 'Slugging Ratio', 'Up-Capture Russell', 'Down-Capture Russell'], 
        market_index='Russell 3000',MAR=0, threshold=0, order=1, start_gap=start_gap)
    
    
    ### Output all static dataframe into excel file
    dfs = [Annulized_Return_df,Calendar_Return_df,Downside_Deviation_df,Sortino_df,Sharpe_df,Standard_deviation_df,Beta_df,Omega_df,Summary_table_df]
    i.multiple_dfs(dfs, 'Static Ratio Result', 'Financial Ratio Table.xlsx', 1)