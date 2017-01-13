# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:52:01 2017

@author: ZFang
"""

import pandas as pd
import os 
import numpy as np
import scipy.optimize as scopt
import matplotlib.pyplot as plt
import pandas.io.data as web

def read_data():
    # os.getcwd()
    os.chdir('C:\\Users\\ZFang\\Desktop\\TeamCo\\Portfolio-Optimization')
    fund_df = pd.read_excel('fund_data.xlsx',index_col='Date')
    return fund_df
    
# calculate annual returns
def calc_annual_returns(daily_returns):
    grouped = np.exp(daily_returns.groupby(
        lambda date: date.year).sum())-1
    return grouped   
    
def get_historical_closes(ticker, start_date, end_date):
    # get the data for the tickers. This will be a panel
    p = web.DataReader(ticker, "yahoo", start_date, end_date)
    # convert the panel to a DataFrame and selection only Adj Close
    # while making all index levels columns
    d = p.to_frame()['Adj Close'].reset_index()
    # remove the columns
    d.rename(columns={'minor':'Ticker','Adj Close':'Close'},
             inplace=True)
    # pivot each ticker to a column
    pivoted = d.pivot(index='Date', columns='Ticker')
    # and drop the one level on the columns
    pivoted.columns = pivoted.columns.droplevel(0)
    return pivoted
    
def calc_daily_returns(closes):
    return np.log(closes/closes.shift(1))
    
def calc_portfolio_var(returns, weights=None):
    if weights is None:
        weights = np.ones(returns.columns.size)/ returns.columns.size
    sigma = np.cov(returns.T, ddof=0)
    var = (weights * sigma * weights.T).sum()
    return var
    
def sharpe_ratio(returns, weights = None, risk_free_rate=0.015):
    n = returns.columns.size
    if weights is None: weights = np.ones(n)/n
    ## print('The weight is ' + str(weights))
    # get the portfolio variance
    var = calc_portfolio_var(returns, weights)
    # and the means of the stocks in the portfolio
    means = returns.mean()
    # and returns the sharpe ratio
    ## print('The Sharpe Ratio is ' + str((means.dot(weights)-risk_free_rate)/np.sqrt(var)))
    return (means.dot(weights)-risk_free_rate)/np.sqrt(var)    
    
def negative_sharpe_ratio(weights, 
                          returns, 
                          risk_free_rate):
    """
    Given n-1 weights, return a negative sharpe ratio
    """
    return -sharpe_ratio(returns, weights, risk_free_rate)   
    
   
def optimize_portfolio(returns, risk_free_rate):
    """ 
    Performs the optimization
    """
    # start with equal weights
    w0 = np.ones(returns.columns.size, 
                 dtype=float) * 1.0 / returns.columns.size
    # minimize the negative sharpe value
    constraints = ({'type': 'ineq', 'fun': lambda w0: w0[0]+w0[1]-0.05},
                   {'type': 'ineq', 'fun': lambda w0: 0.3-w0[0]+w0[1]},
                   {'type': 'eq', 'fun': lambda w0: 1-np.sum(w0)})
    bounds=((0,0.3),(0,0.3),(0.05,0.2),(0.05,0.2),(0.05,0.2),\
            (0.05,0.2),(0.05,0.2),(0.05,0.2),(0.05,0.2),(0.05,0.2))
    w1 = scopt.minimize(negative_sharpe_ratio, 
                    w0, args=(returns, risk_free_rate),
                    method='SLSQP', constraints = constraints,
                    bounds = bounds, options={'disp':True}).x
    print('Reach to the last step: ')
    print('The final w1 is ' + str(w1))
    # and calculate the final, optimized, sharpe ratio
    final_sharpe = sharpe_ratio(returns, w1, risk_free_rate)
    print('The final Sharpe Ratio is ' + str(final_sharpe))
    return (w1, final_sharpe)    
    
def objfun(W,R,target_ret):
    stock_mean = np.mean(R,axis=0)
    port_mean = np.dot(W,stock_mean) # portfolio mean
    cov = np.cov(R.T) # var-cov matrix
    port_var = np.dot(np.dot(W,cov),W.T) # portfolio variance
    penalty = 2000* abs(port_mean-target_ret) # penalty 4 deviation
    return np.sqrt(port_var) + penalty # objective function
    

def calc_efficient_frontier(returns):
    result_means = []
    result_stds = []
    result_weights = []
    
    means = returns.mean()
    min_mean, max_mean = means.min(), means.max()
    
    nstocks = returns.columns.size
    
    for r in np.linspace(min_mean, max_mean, 200):
        weights = np.ones(nstocks)/nstocks
        bounds = [(0,1) for i in np.arange(nstocks)]
        constraints = ({'type': 'eq', 
                        'fun': lambda W: np.sum(W) - 1})
        results = scopt.minimize(objfun, weights, (returns, r), 
                                 method='SLSQP', 
                                 constraints = constraints,
                                 bounds = bounds)
        if not results.success: # handle error
            raise Exception(results.message)
        result_means.append(np.round(r,4)) # 4 decimal places
        std_=np.round(np.std(np.sum(returns*results.x,axis=1)),6)
        result_stds.append(std_)
        
        result_weights.append(np.round(results.x, 5))
    return {'Means': result_means, 
            'Stds': result_stds, 
            'Weights': result_weights}
            
def plot_efficient_frontier(frontier_data):
    plt.figure(figsize=(12,8))
    plt.title('Efficient Frontier')
    plt.xlabel('Standard Deviation of the porfolio (Risk))')
    plt.ylabel('Return of the portfolio')
    plt.plot(frontier_data['Stds'], frontier_data['Means'], 'ro'); 
    plt.savefig('5104OS_09_20.png', bbox_inches='tight', dpi=300)
    
if __name__ == '__main__':    
    ############ Stock ############
    # Stock Data
    closes = get_historical_closes(['AMZN','AAPL','KO','YHOO','GOOG','MSFT','IBM','CSCO','TSM','SAP'], '2008-01-01', '2015-12-31')
    # calculate daily returns
    daily_returns = calc_daily_returns(closes)
    # calculate annual returns
    annual_returns = calc_annual_returns(daily_returns)
    # calculate our portfolio variance (equal weighted)
    calc_portfolio_var(annual_returns)
    # calculate equal weighted sharpe ratio
    eql_sharpe = sharpe_ratio(annual_returns)
    # optimize our portfolio
    ## opt_weight = optimize_portfolio(annual_returns, 0.0003)
    ###### Efficient Frontier ######
    # calculate our frontier
    ## frontier_data = calc_efficient_frontier(annual_returns)
    ## plot_efficient_frontier(frontier_data)
    
    
    ############ Stock with Daily Data ############
    opt_weight_d, final_sharpe_d = optimize_portfolio(daily_returns[1:], 0.0003/252)
    annual_sharpe_d = np.sqrt(252)*final_sharpe_d


    ############ Fund ############
    fund_df = read_data().iloc[:,10:20]
    # Calculate the Annual Return of All Funds
    annual_fund_return = calc_annual_returns(fund_df)
    # calculate our portfolio variance (equal weighted)
    calc_portfolio_var(annual_fund_return)
    # calculate equal weighted sharpe ratio
    eql_fund_sharpe = sharpe_ratio(annual_fund_return)
    # optimize our portfolio
    ## opt_fund_weight = optimize_portfolio(annual_fund_return, 0.0003)
    ###### Efficient Frontier ######
    # calculate our frontier
    ## frontier_fund_data = calc_efficient_frontier(annual_fund_return)
    ## plot_efficient_frontier(frontier_fund_data)
    
    
    ############ Fund with Monthly Data ############
    opt_fund_weight_m, final_fund_sharpe_m = optimize_portfolio(fund_df, 0.0003/12)
    annual_fund_sharpe_m = np.sqrt(12)*final_fund_sharpe_m