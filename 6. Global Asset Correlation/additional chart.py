# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:16:07 2017

@author: ZFang
"""


from pandas_datareader.famafrench import get_available_datasets
import pandas_datareader.data as wb
from datetime import datetime
import dateutil.relativedelta
import plotly.plotly as py
import plotly.graph_objs as go

if __name__ == '__main__':
    ### Fama French Data ###
    # get fama french available data list
    # get_available_datasets()
    start = datetime(1961,7,1)
    ff = wb.DataReader("F-F_Research_Data_5_Factors_2x3_daily", "famafrench", start=start)
    # Cumulative Return
    ff_df = (ff[0]/100)+1
    cum_ff = ff_df.cumprod()-1
    cum_ff.iloc[0,:] = 0 # force the first index to be zero
    
    # Calendar Return and Bar Chart
    calendar_ff = ff_df.resample('A').prod()-1
    calendar_ff.index = calendar_ff.index.year
    # calendar_ff[-10:].plot(kind='bar')
    
    
    ### RLG and RLV Data ###
    r = wb.DataReader(['^RLG','^RLV'],'yahoo',start,datetime.today())['Close']
    # Cumulative Return
    r_return = (r-r.shift(1))/r.shift(1)+1
    r_return.iloc[0,:] = 1 # force the first index to be one
    cum_r_return = r_return.cumprod()-1
    
    # Calendar Return and Bar Chart
    calendar_r = r_return.resample('A').prod()-1
    calendar_r.index=calendar_r.index.year
    # calendar_r[-10:].plot(kind='bar')
    
    ### MTUM and QUAL Data ###
    mq = wb.DataReader(['MTUM','QUAL'],'yahoo',start,datetime.today())['Close']
    mq_return = (mq-mq.shift(1))/mq.shift(1)+1
    # first_index_m = mq_return.ix[:,'MTUM'].first_valid_index()-dateutil.relativedelta.relativedelta(days=1)
    first_index_q = mq_return.ix[:,'QUAL'].first_valid_index()-dateutil.relativedelta.relativedelta(days=1)
    # force the first day return to be one
    mq_return.ix[first_index_q,'MTUM'] = 1
    mq_return.ix[first_index_q,'QUAL'] = 1
    mq_return = mq_return.loc[first_index_q:]
    cum_mp_return = mq_return.cumprod()-1
    
    # Calendar Return and Bar Chart
    calendar_mq = mq_return.resample('A').prod()-1
    calendar_mq.index=calendar_mq.index.year
    # calendar_mq.plot(kind='bar')
    
    py.sign_in('fzn0728', '1enskD2UuiVkZbqcMZ5K')
    ### Figure 1 Cumulative Return of Fama French Factors
    trace1 = go.Scatter(
                  x=cum_ff.index,
                  y=100*cum_ff['Mkt-RF'],
                  name='Market Minus Risk Free'
    )
    
    trace2 = go.Scatter(
                  x=cum_ff.index,
                  y=100*cum_ff['SMB'],
                  name='Small Minus Big'
    )
    trace3 = go.Scatter(
                  x=cum_ff.index,
                  y=100*cum_ff['HML'],
                  name='High Minus Low'
    )
    trace4 = go.Scatter(
                  x=cum_ff.index,
                  y=100*cum_ff['RMW'],
                  name='Robust Minus Weak'
    )
    trace5 = go.Scatter(
                  x=cum_ff.index,
                  y=100*cum_ff['CMA'],
                  name='Conservative Minus Aggressive'
    )
    
    data = [trace1,trace2,trace3,trace4,trace5]
    layout = go.Layout(
    title='Cumulative Return of Fama French Factors',
    # barmode='group',
    # xaxis=dict(tickangle=-45),
    yaxis=dict(
               title='Cumulative Return',
               ticksuffix='%')
    )
    
    fig_1 = go.Figure(data=data, layout=layout)
    py.plot(fig_1, filename='Figure 1 Cumulative Return of Fama French Factors')   
    
    
    ### Figure 2 Last 10 Years Calendar Return of Fama French Factors
    trace1 = go.Bar(
                  x=calendar_ff.index[-10:],
                  y=100*calendar_ff.ix['2007':,'Mkt-RF'],
                  name='Market Minus Risk Free'
    )
    
    trace2 = go.Bar(
                  x=calendar_ff.index[-10:],
                  y=100*calendar_ff.ix['2007':,'SMB'],
                  name='Small Minus Big'
    )
    trace3 = go.Bar(
                  x=calendar_ff.index[-10:],
                  y=100*calendar_ff.ix['2007':,'HML'],
                  name='High Minus Low'
    )
    trace4 = go.Bar(
                  x=calendar_ff.index[-10:],
                  y=100*calendar_ff.ix['2007':,'RMW'],
                  name='Robust Minus Weak'
    )
    trace5 = go.Bar(
                  x=calendar_ff.index[-10:],
                  y=100*calendar_ff.ix['2007':,'CMA'],
                  name='Conservative Minus Aggressive'
    )

    data = [trace1,trace2,trace3,trace4,trace5]
    layout = go.Layout(
    title='Last 10 Years Calendar Return of Fama French Factors',
    barmode='group',
    # xaxis=dict(tickangle=-45),
    yaxis=dict(
               title='Calendar Return',
               ticksuffix='%')
    )
    
    fig_2 = go.Figure(data=data, layout=layout)
    py.plot(fig_2, filename='Figure 2 Last 10 Years Calendar Return of Fama French Factors')
    
    
    ### Figure 3 Cumulative Return of Russell 1000 Growth and Russell 1000 Value
    trace1 = go.Scatter(
                  x=cum_r_return.index,
                  y=100*cum_r_return['^RLG'],
                  name='Russell 1000 Growth'
    )
    
    trace2 = go.Scatter(
                  x=cum_r_return.index,
                  y=100*cum_r_return['^RLV'],
                  name='Russell 1000 Value'
    )

    
    data = [trace1,trace2]
    layout = go.Layout(
    title='Cumulative Return of Russell 1000 Growth and Russell 1000 Value',
    # barmode='group',
    # xaxis=dict(tickangle=-45),
    yaxis=dict(
               title='Cumulative Return',
               ticksuffix='%')
    )
    
    fig_3 = go.Figure(data=data, layout=layout)
    py.plot(fig_3, filename='Figure 3 Cumulative Return of Russell 1000 Growth and Russell 1000 Value')   
    
    
    ### Figure 4 Last 10 Years Calendar Return of Russell 1000 Growth and Russell 1000 Value
    trace1 = go.Bar(
                  x=calendar_r.index[-10:],
                  y=100*calendar_r.ix['2008':,'^RLG'],
                  name='Russell 1000 Growth'
    )
    
    trace2 = go.Bar(
                  x=calendar_r.index[-10:],
                  y=100*calendar_r.ix['2008'::,'^RLV'],
                  name='Russell 1000 Value'
    )

    
    data = [trace1,trace2]
    layout = go.Layout(
    title='Last 10 Years Calendar Return of Russell 1000 Growth and Russell 1000 Value',
    barmode='group',
    # xaxis=dict(tickangle=-45),
    yaxis=dict(
               title='Calendar Return',
               ticksuffix='%')
    )
    
    fig_4 = go.Figure(data=data, layout=layout)
    py.plot(fig_4, filename='Figure 4 Last 10 Years Calendar Return of Russell 1000 Growth and Russell 1000 Value')

    ### Figure 5 Cumulative Return of iShares MSCI Momentum Factor and iShares MSCI Quality Factor
    trace1 = go.Scatter(
                  x=cum_mp_return.index,
                  y=100*cum_mp_return['MTUM'],
                  name='iShares MSCI Momentum Factor'
    )
    
    trace2 = go.Scatter(
                  x=cum_mp_return.index,
                  y=100*cum_mp_return['QUAL'],
                  name='iShares MSCI Quality Factor'
    )

    
    data = [trace1,trace2]
    layout = go.Layout(
    title='Cumulative Return of iShares MSCI Momentum Factor and iShares MSCI Quality Factor',
    # barmode='group',
    # xaxis=dict(tickangle=-45),
    yaxis=dict(
               title='Cumulative Return',
               ticksuffix='%')
    )
    
    fig_5 = go.Figure(data=data, layout=layout)
    py.plot(fig_5, filename='Figure 5 Cumulative Return of iShares MSCI Momentum Factor and iShares MSCI Quality Factor')
    
    ### Figure 6 Calendar Return of iShares MSCI Momentum Factor and iShares MSCI Quality Factor
    trace1 = go.Bar(
                  x=calendar_mq.index,
                  y=100*calendar_mq['MTUM'],
                  name='iShares MSCI Momentum Factor'
    )
    
    trace2 = go.Bar(
                  x=calendar_mq.index,
                  y=100*calendar_mq['QUAL'],
                  name='iShares MSCI Quality Factor'
    )

    
    data = [trace1,trace2]
    layout = go.Layout(
    title='Calendar Return of iShares MSCI Momentum Factor and iShares MSCI Quality Factor',
    barmode='group',
    # xaxis=dict(tickangle=-45),
    yaxis=dict(
               title='Calendar Return',
               ticksuffix='%')
    )
    
    fig_6 = go.Figure(data=data, layout=layout)
    py.plot(fig_6, filename='Figure 6 Calendar Return of iShares MSCI Momentum Factor and iShares MSCI Quality Factor')