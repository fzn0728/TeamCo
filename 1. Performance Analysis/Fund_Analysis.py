# -*- coding: utf-8 -*-
"""
This is the main file to get all major financial ratio and rolling ratio and other important graph
"""
import os
import mod_financial_ratio as r
import mod_rolling as m
import mod_input_output as put
import mod_plot as p
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


from pylab import rcParams
rcParams['figure.figsize'] = 18, 12

if __name__ == '__main__':
    os.chdir(r'C:\Users\ZFang\Desktop\Zhongnan Fang Internship Project\1. Performance Analysis\\')
    ### Read the file
    df_data = put.concat_data('test_data.xlsx')
    ### Define constant variable
    # Initial value for static ratio calculation
    target_year = ['1_Year','3_Year','5_Year','7_Year','Since Inception']
    benchmark = 0.02 # Benchmark is the risk free return
    threshold = 0 # Threshold for downside deviation - also for sortino ratio
    MAR = 0 # Minimum Accept Return
    market_index = df_data.columns[-1] # For Beta and correlation
    summary_columns = ['Batting Average', 'Omega Ratio', 'Up Months', 'Down Months', 'Slugging Ratio', 'Up-Capture Russell', 'Down-Capture Russell']
    index_name = df_data.columns[1:-1] # No Date and Market Index
    index_name_2 = df_data.columns[0:-1] # No Market Index
    index_name_3 = df_data.columns[1:] # No Date
    columns_name = df_data.columns[1:] # No Date
    # Initial value for rolling data calculation
    window_length = 36 # rolling window is 36 months
    min_periods = 36 # We only take complete 36 month period into consideration

    ### Calculate Annulized Return
    Annulized_Return_df = r.annulized_return_table(df_data, index_name, target_year)
    ### Calculate Calendar Return
    Calendar_Return_df = r.calendar_return_table(df_data, index_name_2)
    ### Calculate Downside Deviation, given order of two
    Downside_Deviation_df = r.downside_std_table(df_data, index_name, threshold, target_year)
    ### Calculate Sortino ratio
    Sortino_df = r.sortino_ratio_table(df_data, index_name, MAR, threshold, target_year)
    ### Calculate Sharp ratio
    Sharpe_df=r.sharpe_ratio_table(df_data, index_name, benchmark, target_year)
    ### Standard Deviation
    Standard_deviation_df = r.standard_deviation_table(df_data, index_name, target_year)
    ### Beta matrix
    Beta_df = r.beta_table(df_data, index_name_3, target_year, condition = None)
    ### Positive Beta matrix
    Beta_df_p = r.beta_table(df_data, index_name_3, target_year, condition = 'Positive')
    ### Non Negative Beta matrix
    Beta_df_np = r.beta_table(df_data, index_name_3, target_year, condition = 'Non-positive')
    ### Omega Ratio
    Omega_df = r.omega_ratio_table(df_data, index_name, MAR, target_year)
    ### Correlation table
    Corr_df = r.corr_table(df_data, index_name_3, market_index, target_year, condition = None)
    ### Positive Correlation table
    Corr_df_p = r.corr_table(df_data, index_name_3, market_index, target_year, condition='Positive')
    ### Positive Correlation table
    Corr_df_np = r.corr_table(df_data, index_name_3, market_index, target_year, condition='Non-positive')    
    ### Summary table
    Summary_table_df = r.summary_table(df_data,index_name, summary_columns, market_index, MAR)
    ### Daily maximum Drawdown for differnt portfolio
    max_dd_df =m.time_drawdown(df_data, 'TeamCo Client Composite')
    ### Maximum Drawdown for given time window
    max_dd = m.max_drawdown(df_data, 'TeamCo Client Composite')
    
    ### Rolling beta
    rolling_beta_df = m.rolling_beta(df_data, columns_name, window_length, min_periods)
    ### Rolling annulized return
    rolling_annual_return_df = m.rolling_annulized_return(df_data, columns_name, window_length, min_periods)
    ### Cummulative return
    cum_return_df = m.cumulative_return(df_data, columns_name, window_length, min_periods)
    ### Rolling sortino ratio
    rolling_sortino_ratio_df = m.rolling_sortino_ratio(df_data, columns_name, window_length, min_periods, MAR, threshold)
    ### Rolling omega ratio
    rolling_omega_ratio_df = m.rolling_omega_ratio(df_data, columns_name, window_length, min_periods, MAR)
    ### Rolling sharp ratio
    rolling_sharpe_ratio_df = m.rolling_sharpe_ratio(df_data, columns_name, window_length, min_periods, benchmark)
    ### Rolling alpha
    rolling_alpha_df = m.rolling_alpha(df_data, columns_name, window_length, min_periods)
    ### Rolling correlation
    rolling_corr_df = m.rolling_corr(df_data, columns_name, market_index, window_length, min_periods)
    ### Draw Down
    dd_df = 100* m.draw_down(df_data, columns_name)
    
    ### Generate graph and save them to the pdf file
    p.graph_gen('Rolling Ratio Figure and Radar Chart Result.pdf', index_name, rolling_annual_return_df, cum_return_df, \
                rolling_alpha_df,rolling_beta_df, rolling_corr_df, rolling_sharpe_ratio_df, \
                rolling_sortino_ratio_df,rolling_omega_ratio_df, dd_df, Beta_df, Beta_df_p, \
                Beta_df_np, Corr_df, Corr_df_p, Corr_df_np)

    
    ### Output all static dataframe into excel file
    dfs = [Annulized_Return_df,Calendar_Return_df,Sharpe_df,Sortino_df,\
           Standard_deviation_df,Downside_Deviation_df,Beta_df,Beta_df_p,\
           Beta_df_np,Omega_df,Corr_df,Corr_df_p,Corr_df_np,Summary_table_df]
    put.multiple_dfs(dfs, 'Financial Ratio', 'Financial Ratio Result.xlsx', 1)
    
    ### Output all rolling data to seperated sheet in excel file
    rolling_df_list = [rolling_beta_df,rolling_annual_return_df,cum_return_df,\
                       rolling_sortino_ratio_df,rolling_omega_ratio_df,rolling_sharpe_ratio_df,\
                       rolling_alpha_df,rolling_corr_df]
    put.multiple_sheets(rolling_df_list, 'Rolling Result.xlsx')
