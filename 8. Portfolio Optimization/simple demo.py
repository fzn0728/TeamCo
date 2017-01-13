# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 10:56:43 2017

@author: ZFang
"""

import numpy as np
import matplotlib.pyplot as plt
# import cvxopt as opt
# from cvxopt import blas, solvers
import pandas as pd



def rand_weights(n):
    '''
    Produces n random weights that sum up to 1
    '''
    k = np.random.rand(n)
    return k/sum(k)
    
def random_portfolio(returns):
    '''
    Returns the mean and standard deviation of returns for a random portfolio
    '''

    p = np.asmatrix(np.mean(returns, axis=1))
    w = np.asmatrix(rand_weights(returns.shape[0]))
    C = np.asmatrix(np.cov(returns))
    
    mu = w*p.T
    sigma = np.sqrt(w*C*w.T)
    
    # This recursion reduces outliers to keep plots pretty
    if sigma>2:
        return random_portfolio(returns)
    return mu, sigma

if __name__ == "__main__":
    np.random.seed(123)
    
    # Turn off progress printing
    # solvers.options['show_progress'] = False

    ### NUMBER OF ASSETS
    n_assets = 4
    
    ### NUMBER OF OBSERVATIONS
    n_obs = 1000
    
    return_vec = np.random.randn(n_assets, n_obs)
    
    plt.plot(return_vec.T, alpha=0.4)
    plt.xlabel('time')
    plt.ylabel('return')
    
    ### GENERATE MEAN AND RETURN FOR 500 PORTFOLIOS
    n_portfolios = 500
    means, stds = np.column_stack([
                                   random_portfolio(return_vec)
                                   for _ in range(n_portfolios)
                                   ])
    
    
    