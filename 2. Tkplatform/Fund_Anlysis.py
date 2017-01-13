# -*- coding: utf-8 -*-
"""
This is the main file to get all major financial ratio and rolling ratio and other important graph
"""
import os
import mod_financial_ratio as r
import mod_rolling as m
import mod_input_output as i
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from pylab import rcParams
rcParams['figure.figsize'] = 18, 12

if __name__ == '__main__':
    ### Change working directory
    # Get working directory
    os.getcwd()
    # Set working director
    data_file_path = r'C:\Users\ZFang\Desktop\TeamCo\Financial Ratio\\'
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
    ### Daily maximum Drawdown for differnt portfolio
    max_dd_df =m.time_drawdown(df_data, 'TeamCo Client Composite', 109, 0, 109, start_gap=6)
    ### Maximum Drawdown for given time window
    max_dd = m.max_drawdown(df_data, 'TeamCo Client Composite', 109, 0, 109, start_gap=6)
    ### Rolling beta
    rolling_beta_df = m.rolling_beta(df_data, 
        columns_name=columns_name, 
        window_length=36, min_periods=36, start_gap=6)
    ### Rolling annulized return
    rolling_annual_return_df = m.rolling_annulized_return(df_data, 
        columns_name=columns_name, 
        window_length=36, min_periods=36, start_gap=6)
    ### Cummulative return
    cum_return_df = m.cumulative_return(df_data, 
        columns_name=columns_name, 
        window_length=36, min_periods=36, start_gap=6)
    ### Rolling sortino ratio
    rolling_sortino_ratio_df = m.rolling_sortino_ratio(df_data, 
        columns_name=columns_name, 
        window_length=36, min_periods=36, start_gap=6, MAR=0, threshold=0, order=2)
    ### Rolling omega ratio
    rolling_omega_ratio_df = m.rolling_omega_ratio(df_data, 
        columns_name=columns_name, 
        window_length=36, min_periods=36, start_gap=6, MAR=0)
    ### Rolling sharp ratio
    rolling_sharpe_ratio_df = m.rolling_sharpe_ratio(df_data, 
        columns_name=columns_name, 
        window_length=36, min_periods=36, start_gap=6, benchmark=0.02)
    ### Rolling alpha
    rolling_alpha_df = m.rolling_alpha(df_data, 
        columns_name=columns_name, 
        window_length=36, min_periods=36, start_gap=6)
    ### Rolling correlation
    rolling_corr_df = m.rolling_corr(df_data, 
        columns_name=columns_name, 
        target_benchmark='Russell 3000', window_length=36, min_periods=36, start_gap=6)
    ### Draw Down
    dd_df = 100* m.draw_down(df_data, columns_name, start_gap)
    
    
    ### Graph for result
    with PdfPages('Rolling Ratio Figure.pdf') as pdf:
        plt.style.use('fivethirtyeight')
        rolling_annual_return_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(title='36 Months Rolling Annual Return')
        plt.legend(prop={'size':12})
        pdf.savefig()
        
        cum_return_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(title='Cummulative Return')
        plt.legend(loc='upper left', prop={'size':12})
        pdf.savefig()
        
        rolling_alpha_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(title='36 Months Rolling Alpha')
        plt.legend(prop={'size':12})
        pdf.savefig()
        
        rolling_beta_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(title='36 Months Rolling Beta')
        plt.legend(prop={'size':12})
        pdf.savefig()
        
        rolling_corr_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(title='36 Months Rolling Correlation')
        plt.legend(prop={'size':12})
        pdf.savefig()        
        
        rolling_sharpe_ratio_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(title='36 Months Rolling Sharpe Ratio')
        plt.legend(loc='upper left',prop={'size':12})
        pdf.savefig()    
        
        rolling_sortino_ratio_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(title='36 Months Rolling Sortino')
        plt.legend(loc='upper left',prop={'size':12})
        pdf.savefig()
        
        rolling_omega_ratio_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(title='36 Months Rolling Omega Ratio')    
        plt.legend(loc='upper left',prop={'size':12})
        pdf.savefig()
        
        dd_fig = dd_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'Russell 3000']].plot(title='Draw Down - Fund vs Competitors vs Benchmark')
        plt.legend(loc='lower left',prop={'size':12})
        pdf.savefig()        
        
        # max_dd_df.plot(title='Current Drawdown Changing Graph')
    
    ### Output all static dataframe into excel file
    dfs = [Annulized_Return_df,Calendar_Return_df,Downside_Deviation_df,Sortino_df,Sharpe_df,Standard_deviation_df,Beta_df,Omega_df,Summary_table_df]
    i.multiple_dfs(dfs, 'Financial Ratio', 'Financial Ratio Table.xlsx', 1)
    
    ### Output all rolling data to seperated sheet in excel file
    rolling_df_list = [rolling_beta_df,rolling_annual_return_df,cum_return_df,rolling_sortino_ratio_df,rolling_omega_ratio_df,rolling_sharpe_ratio_df,rolling_alpha_df,rolling_corr_df]
    i.multiple_sheets(rolling_df_list, 'Rolling Result.xlsx')
    
    '''
        plt.figure(figsize=(8,6))
        fig, axes = plt.subplots(nrows=2, ncols=2)
        rolling_annual_return_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(ax=axes[0,0]); axes[0,0].set_title('36 Months Rolling Annual Return')
        cum_return_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(ax=axes[0,1]); axes[0,1].set_title('Cummulative Return')
        rolling_alpha_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(ax=axes[1,0]); axes[1,0].set_title('36 Months Rolling Alpha')
        rolling_beta_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(ax=axes[1,1]); axes[1,1].set_title('36 Months Rolling Beta')
        plt.title('Test')
        pdf.savefig()
        plt.close()
        
        
        fig, axes = plt.subplots(nrows=2, ncols=2)    
        rolling_corr_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(ax=axes[0,0]); axes[0,0].set_title('36 Months Rolling Correlation')
        rolling_sharpe_ratio_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(ax=axes[0,1]); axes[0,1].set_title('36 Months Rolling Sharpe Ratio')
        rolling_sortino_ratio_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(ax=axes[1,0]); axes[1,0].set_title('36 Months Rolling Sortino')
        rolling_omega_ratio_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(ax=axes[1,1]); axes[1,1].set_title('36 Months Rolling Omega Ratio')    
        pdf.savefig()
        plt.close()
        
        
        dd_fig = dd_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'Russell 3000']].plot(title='Draw Down - Fund vs Competitors vs Benchmark')
        pdf.savefig()
        plt.close()
    '''