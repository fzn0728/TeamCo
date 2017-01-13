# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:03:39 2016

@author: ZFang
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:12:11 2016

@author: ZFang
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:01:23 2016

@author: ZFang
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 10:00:12 2016
@author: ZFang
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
import numpy as np
import outliers_influence as ou
import copy


def get_error(df, reg):
    my_ols = sm.ols(formula=reg, data=df).fit()
    resid = my_ols.resid
    return resid
    
def rolling_v_coef(df):
    para_df = pd.DataFrame(columns=['ACWI_err', 'MSCI_World_err', 'Russell_3000', \
    'US_Dollar', 'Bond_Index','HFRI_Relative_Value', 'HFRI_Macro_Total','HFRI_ED_Distressed_Restructuring',\
    'HFRI_EH_Equity_Market_Neutral','HFRI_RV_Fixed_Income_Convertible_Arbitrage','HFRI_RV_Fixed_Income_AB',\
    'HFRI_ED_Activitst_Index','HFRI_Macro_multistrategy','HFRI_EH_Quant_Directional'])
    m_df = pd.DataFrame(columns=['ACWI_err', 'MSCI_World_err', 'Russell_3000', \
    'US_Dollar', 'Bond_Index','HFRI_Relative_Value', 'HFRI_Macro_Total','HFRI_ED_Distressed_Restructuring',\
    'HFRI_EH_Equity_Market_Neutral','HFRI_RV_Fixed_Income_Convertible_Arbitrage','HFRI_RV_Fixed_Income_AB',\
    'HFRI_ED_Activitst_Index','HFRI_Macro_multistrategy','HFRI_EH_Quant_Directional'])
    for i in range(0,len(df.index)-35):
        df_r = df.iloc[i:i+36,:]
        # gen orthogonal error series
        df_r['ACWI_err'] = get_error(df_r, 'ACWI ~ MSCI_World + Russell_3000').values
        df_r['MSCI_World_err'] = get_error(df_r, 'MSCI_World ~ ACWI_err + Russell_3000').values          
        my_ols = sm.ols(formula='FOF ~ ACWI_err + MSCI_World_err + Russell_3000 + US_Dollar + Bond_Index + HFRI_Relative_Value + HFRI_Macro_Total + HFRI_ED_Distressed_Restructuring + HFRI_EH_Equity_Market_Neutral + HFRI_RV_Fixed_Income_Convertible_Arbitrage + HFRI_RV_Fixed_Income_AB + HFRI_ED_Activitst_Index + HFRI_Macro_multistrategy + HFRI_EH_Quant_Directional', data=df_r).fit()
        # concat each rolling param
        s = pd.DataFrame(my_ols.params).T
        m = pd.DataFrame(df_r.loc[:,['ACWI_err','MSCI_World_err','Russell_3000','US_Dollar','Bond_Index','HFRI_Relative_Value','HFRI_Macro_Total','HFRI_ED_Distressed_Restructuring','HFRI_EH_Equity_Market_Neutral','HFRI_RV_Fixed_Income_Convertible_Arbitrage','HFRI_RV_Fixed_Income_AB','HFRI_ED_Activitst_Index','HFRI_Macro_multistrategy','HFRI_EH_Quant_Directional','FOF']].mean(axis=0)).T
        para_df = pd.concat([para_df,s], axis=0)
        m_df = pd.concat([m_df,m], axis=0)
    # chean format of index
    para_df = para_df.reset_index()
    para_df = para_df.set_index(df.index[35:])
    para_df = para_df.drop('index', axis=1)
    m_df = m_df.reset_index()
    m_df = m_df.set_index(df.index[35:])
    m_df = m_df.drop('index', axis=1)
    # m_df.rename(columns={'ACWI_err':'ACWI', 'MSCI_World_err':'MSCI_World'})
    return df_r, m_df, para_df


def plot_v_stack(df):
    date = np.arange(66)
    Intercept = df['Intercept'].values
    ACWI = df['ACWI_err'].values
    MSCI_World = df['MSCI_World_err'].values
    Russell_3000 = df['Russell_3000'].values
    US_Dollar = df['US_Dollar'].values
    Bond_Index = df['Bond_Index'].values
    HFRI_Relative_Value = df['HFRI_Relative_Value'].values
    HFRI_Macro_Total = df['HFRI_Macro_Total'].values
    HFRI_ED_Distressed_Restructuring = df['HFRI_ED_Distressed_Restructuring'].values
    HFRI_EH_Equity_Market_Neutral = df['HFRI_EH_Equity_Market_Neutral'].values
    HFRI_RV_Fixed_Income_Convertible_Arbitrage = df['HFRI_RV_Fixed_Income_Convertible_Arbitrage'].values
    HFRI_RV_Fixed_Income_AB = df['HFRI_RV_Fixed_Income_AB'].values
    HFRI_ED_Activitst_Index = df['HFRI_ED_Activitst_Index'].values
    HFRI_Macro_multistrategy = df['HFRI_Macro_multistrategy'].values
    HFRI_EH_Quant_Directional = df['HFRI_EH_Quant_Directional'].values

    # Generate empty plot to have the label
    fig, ax = plt.subplots()
    plt.plot([],[], label='Intercept', color='#56B4E9')
    plt.plot([],[], label='ACWI', color='m')
    plt.plot([],[], label='MSCI_World', color='c')
    plt.plot([],[], label='Russell_3000', color='r')
    plt.plot([],[], label='US_Dollar', color='k')
    plt.plot([],[], label='Bond_Index', color='b')
    plt.plot([],[], label='HFRI_Relative_Value', color='#92C6FF')
    plt.plot([],[], label='HFRI_Macro_Total', color='#001C7F')
    plt.plot([],[], label='HFRI_ED_Distressed_Restructuring', color='.15')
    plt.plot([],[], label='HFRI_EH_Equity_Market_Neutral', color='#30a2da')
    plt.plot([],[], label='HFRI_RV_Fixed_Income_Convertible_Arbitrage', color='#A60628')
    plt.plot([],[], label='HFRI_RV_Fixed_Income_AB', color='#EAEAF2')
    plt.plot([],[], label='HFRI_ED_Activitst_Index', color='#e5ae38')
    plt.plot([],[], label='HFRI_Macro_multistrategy', color='#FFB5B8')
    plt.plot([],[], label='HFRI_EH_Quant_Directional', color='lime')
    # Gen Stackplot
    plt.stackplot(date,Intercept,ACWI,MSCI_World,Russell_3000,US_Dollar,Bond_Index, 
                  HFRI_Relative_Value,HFRI_Macro_Total,HFRI_ED_Distressed_Restructuring,HFRI_EH_Equity_Market_Neutral,HFRI_RV_Fixed_Income_Convertible_Arbitrage,HFRI_RV_Fixed_Income_AB,HFRI_ED_Activitst_Index,HFRI_Macro_multistrategy,HFRI_EH_Quant_Directional,
                  colors=['#56B4E9','m','c','r','k','b','#92C6FF','#001C7F','.15','#30a2da','#A60628','#EAEAF2','#e5ae38','#FFB5B8','lime'])
    plt.xlabel('Date')
    plt.ylabel('Composition')
    plt.legend(loc='upper right', prop={'size':10})
    plt.title('Evolution of Factor Exposure - VIF Adjusted Method')
    plt.show()

    
    
def cal_vif(df):
    df = df.drop('FOF', axis=1)
    VIF_df = df.corr()
    for i in range(0,14):
        for j in range(0,14):
            df_ = df.iloc[:,(i,j)]
            VIF_df.iloc[i,j] = ou.variance_inflation_factor(df_.values,0)
    return VIF_df
    
   
def plot_pre(para_df, mean_df, title, column_name):
    pred_df = copy.deepcopy(para_df)
    for i in column_name:
        pred_df[i] = para_df[i]*mean_df[i]    
    pred_df['FOF'] = mean_df['FOF']
    pred_df['BETA'] = pred_df.loc[:,column_name].sum(axis=1)
    fig, ax = plt.subplots()
    plt.plot(pred_df['FOF'].values, linestyle="-", linewidth=4, label='FOF')
    plt.plot(pred_df['Intercept'].values, linestyle="--", linewidth=2, label='Intercept')
    plt.plot(pred_df['BETA'].values, linestyle="--", linewidth=2, label='BETA')
    plt.legend()
    plt.title(title)
    return pred_df


    
if __name__ == '__main__':
    # file path
    os.chdir(r'C:\Users\ZFang\Desktop\TeamCo\return and risk attribution project\\')
    file_name = 'data_fof.xlsx'
    df = pd.read_excel(file_name)
    df.index = df['Period']
    df = df.drop('Period', axis=1)
    # Correlation 
    corr_df = df.corr()
    
    ### Calculate VIF Matrix
    VIF_df = cal_vif(df)
    # Rolling 36 months Correlation
    r_36_df = df.rolling(window=36).corr()
    corr_36_df = r_36_df[df.index[35:]].values
    corr_36_FOF_df = r_36_df.iloc[:,5].T
    corr_36_FOF_df = corr_36_FOF_df.iloc[35:]
    # Plot graph
    plt.style.use('fivethirtyeight')
    corr_36_FOF_df.plot()
    plt.legend(loc='lower right',prop={'size':8})
    plt.title('36 Months Rolling Correlation with FOF')

    ### VIF adjusted method
    df_r, mean_v_df, para_v_df = rolling_v_coef(df)
    # para_v_df.plot()
    # plt.title('Evolution of Coefficient - VIF adjusted Method')
    # Calculate Prediction
    pred_v_df = plot_pre(para_v_df, mean_v_df, 'Prediction - VIF Adjusted Method', ['ACWI_err','MSCI_World_err','Russell_3000','US_Dollar','Bond_Index','HFRI_Relative_Value','HFRI_Macro_Total','HFRI_ED_Distressed_Restructuring','HFRI_EH_Equity_Market_Neutral','HFRI_RV_Fixed_Income_Convertible_Arbitrage','HFRI_RV_Fixed_Income_AB','HFRI_ED_Activitst_Index','HFRI_Macro_multistrategy','HFRI_EH_Quant_Directional'])
    # Revise it into proportion
    para_v_abs_df = para_v_df.loc[:,['Intercept','ACWI_err','MSCI_World_err','Russell_3000','US_Dollar','Bond_Index','HFRI_Relative_Value','HFRI_Macro_Total','HFRI_ED_Distressed_Restructuring','HFRI_EH_Equity_Market_Neutral','HFRI_RV_Fixed_Income_Convertible_Arbitrage','HFRI_RV_Fixed_Income_AB','HFRI_ED_Activitst_Index','HFRI_Macro_multistrategy','HFRI_EH_Quant_Directional']].abs()
    para_por_v_abs_df = para_v_abs_df.apply(lambda x: x/x.sum(), axis=1)
    pred_v_abs_df = pred_v_df.loc[:,['Intercept','ACWI_err','MSCI_World_err','Russell_3000','US_Dollar','Bond_Index','HFRI_Relative_Value','HFRI_Macro_Total','HFRI_ED_Distressed_Restructuring','HFRI_EH_Equity_Market_Neutral','HFRI_RV_Fixed_Income_Convertible_Arbitrage','HFRI_RV_Fixed_Income_AB','HFRI_ED_Activitst_Index','HFRI_Macro_multistrategy','HFRI_EH_Quant_Directional']].abs()
    pred_por_v_abs_df = pred_v_abs_df.apply(lambda x: x/x.sum(), axis=1)   
    # plot
    # plot_v_stack(para_por_v_df)
    plot_v_stack(pred_por_v_abs_df)      
    
    ### other more plots
    pred_v_df.plot(linewidth=2)
    plt.legend(loc='upper right',prop={'size':8})
    fig, ax = plt.subplots()
    date = np.arange(66)
    Alpha = pred_v_df['Intercept'].values
    FOF = pred_v_df['FOF'].values
    # plt.plot([],[], label='Intercept', color=')
    # plt.plot([],[], label='FOF', color='r')
    plt.stackplot(date, Alpha, FOF, alpha=0.7)

    
    




    
