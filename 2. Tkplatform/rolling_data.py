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
    data_file_path = r'C:\Users\ZFang\Desktop\TeamCo\Tkplatform\\'
    os.chdir(data_file_path)
    ### Define constant variable
    # The number of month at the beginning that has no available data
    # Since start from 2007, the first six months doesn't have performance data, 
    # I set the starting gap is 6 months
    start_gap = 6
    columns_name = ['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index', 'Russell 3000']

    ### Read the file
    df_data = i.concat_data('Fund Analysis.xlsx')
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

    ### Output all rolling data to seperated sheet in excel file
    rolling_df_list = [rolling_beta_df,rolling_annual_return_df,cum_return_df,rolling_sortino_ratio_df,rolling_omega_ratio_df,rolling_sharpe_ratio_df,rolling_alpha_df,rolling_corr_df]
    i.multiple_sheets(rolling_df_list, 'Rolling Result.xlsx')