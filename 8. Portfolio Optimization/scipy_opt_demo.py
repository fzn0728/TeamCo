# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 13:40:08 2017

@author: ZFang
"""

import pandas as pd
import numpy as np
import pandas.io.data as web
from datetime import datetime
import scipy as sp
import scipy.optimize as scopt
import scipy.stats as spstats
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def create_portfolio(tickers, weights=None):
    if weights is None:
        weights = np.ones(len(tickers))/len(tickers)
    portfolio = pd.DataFrame({'Tickers':tickers,
                              'Weights':weights},
                              index=tickers)
    return portfolio
    
    
def calculate_weighted_portfolio_value(portfolio,
                                       returns,
                                       name='Value'):
    total_weights = portfolio.Weights.sum()
    weighted_returns = returns * (portfolio.Weights /
                                 total_weights)
    return pd.DataFrame({name:weighted_returns.sum(axis=1)})
    
    
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

# calculate annual returns
def calc_annual_returns(daily_returns):
    grouped = np.exp(daily_returns.groupby(
        lambda date: date.year).sum())-1
    return grouped    
    
def calc_portfolio_var(returns, weights=None):
    if weights is None:
        weights = np.ones(returns.columns.size)/ returns.columns.size
    sigma = np.cov(returns.T, ddof=0)
    var = (weights * sigma * weights.T).sum()
    return var
    
def sharpe_ratio(returns, weights = None, risk_free_rate=0.015):
    n = returns.columns.size
    if weights is None: weights = np.ones(n)/n
    # get the portfolio variance
    var = calc_portfolio_var(returns, weights)
    # and the means of the stocks in the portfolio
    means = returns.mean()
    # and returns the sharpe ratio
    return (means.dot(weights)-risk_free_rate)/np.sqrt(var)    
    
def negative_sharpe_ratio_n_minus_1_stock(weights, 
                                          returns, 
                                          risk_free_rate):
    """
    Given n-1 weights, return a negative sharpe ratio
    """
    weights2 = sp.append(weights, 1-np.sum(weights))
    return -sharpe_ratio(returns, weights2, risk_free_rate)
    
def optimize_portfolio(returns, risk_free_rate):
    """ 
    Performs the optimization
    """
    # start with equal weights
    w0 = np.ones(returns.columns.size-1, 
                 dtype=float) * 1.0 / returns.columns.size
    # minimize the negative sharpe value
    w1 = scopt.fmin(negative_sharpe_ratio_n_minus_1_stock, 
                    w0, args=(returns, risk_free_rate))
    # build final set of weights
    final_w = sp.append(w1, 1 - np.sum(w1))
    # and calculate the final, optimized, sharpe ratio
    final_sharpe = sharpe_ratio(returns, final_w, risk_free_rate)
    return (final_w, final_sharpe)    
    
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
    
    for r in np.linspace(min_mean, max_mean, 100):
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
    plt.plot(frontier_data['Stds'], frontier_data['Means'], '--'); 
    plt.savefig('5104OS_09_20.png', bbox_inches='tight', dpi=300)
    
    
 
    

if __name__ == '__main__':
    portfolio = create_portfolio(['StockA', 'Stock B'],[1,1])
    
    returns = pd.DataFrame(
        {'Stock A': [0.1, 0.24, 0.05, -0.02, 0.2],
         'Stock B': [-0.15, -0.2, -0.01, 0.04, -0.15]})
    wr = calculate_weighted_portfolio_value(portfolio,
                                            returns,
                                            'Value')
    with_value = pd.concat([returns,wr],axis=1)
    closes = get_historical_closes(['MSFT', 'AAPL', 'KO'], '2010-01-01', '2014-12-31')

    
    # calculate daily returns
    daily_returns = calc_daily_returns(closes)
    # calculate annual returns
    annual_returns = calc_annual_returns(daily_returns)
    # calculate our portfolio variance (equal weighted)
    calc_portfolio_var(annual_returns)
    # calculate equal weighted sharpe ratio
    sharpe_ratio(annual_returns)
                 
    # optimize our portfolio
    optimize_portfolio(annual_returns, 0.0003)
    
    ###### Efficient Frontier ######
    # calculate our frontier
    frontier_data = calc_efficient_frontier(annual_returns)
    plot_efficient_frontier(frontier_data)
    
    ###### Value At Risk ######
    # get adjusted close values for AAPL in 2014
    aapl_closes = get_historical_closes(['AAPL'], 
                                        datetime(2014, 1, 1),
                                        datetime(2014, 12, 31))
    # now convert the daily prices to returns
    returns = calc_daily_returns(aapl_closes)
    # plot the histogram of returns
    plt.figure(figsize=(12,8))
    plt.hist(returns.values[1:], bins=100);
    plt.savefig('5104OS_09_23.png', bbox_inches='tight', dpi=300)
    # get the z-score for 95%
    z = spstats.norm.ppf(0.95)
    # our position is 1000 shares of AAPL at the price
    # on 2014-22-31
    position = 1000 * aapl_closes.ix['2014-12-31'].AAPL
    # what is our VaR
    VaR = position * (z * returns.AAPL.std())
    
    ###### Misc ######
    # draw a 99% one-tail confidence interval
    x = np.linspace(-4,4,101)
    y = np.exp(-x**2/2) / np.sqrt(2*np.pi)
    x2 = np.linspace(-4,-2.33,101)
    y2 = np.exp(-x2**2/2) / np.sqrt(2*np.pi)
    f = plt.figure(figsize=(12,8))
    plt.plot(x,y*100, linewidth=2)
    xf, yf = mlab.poly_between(x2, 0*x2, y2*100)
    plt.fill(xf, yf, facecolor='g', alpha=0.5)
    plt.gca().set_xlabel('z-score')
    plt.gca().set_ylabel('Frequency %')
    plt.title("VaR based on the standard normal distribution")
    bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="w", ec="b", lw=2)
    t = f.text(0.25, 0.35, "99% VaR confidence level", ha="center", va="center", 
               rotation=270,
                size=15,
                bbox=bbox_props)
    plt.savefig('5104OS_09_21.png', bbox_inches='tight', dpi=300)
    
                 