"""MC1-P2: Optimize a portfolio. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			 	 	 		 		 	  		   	  			  	
Atlanta, Georgia 30332 			  		 			 	 	 		 		 	  		   	  			  	
All Rights Reserved 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Template code for CS 4646/7646 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			 	 	 		 		 	  		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			 	 	 		 		 	  		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			 	 	 		 		 	  		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			 	 	 		 		 	  		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			 	 	 		 		 	  		   	  			  	
or edited. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			 	 	 		 		 	  		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			 	 	 		 		 	  		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			 	 	 		 		 	  		   	  			  	
GT honor code violation. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
-----do not edit anything above this line--- 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Student Name: Tucker Balch (replace with your name) 			  		 			 	 	 		 		 	  		   	  			  	
GT User ID: nmao7 (replace with your User ID)
GT ID: 903363914 (replace with your GT ID)
""" 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt
import math
import sys
sys.path.insert(0, "/Users/imac/Dropbox/Summer 2019 7646/ML4T_2019Spring")
from util import get_data, plot_data
from scipy.optimize import minimize

 			  		 			 	 	 		 		 	  		   	  			  	
# This is the function that will be tested by the autograder 			  		 			 	 	 		 		 	  		   	  			  	
# The student must update this code to properly implement the functionality 			  		 			 	 	 		 		 	  		   	  			  	
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=True):
 			  		 			 	 	 		 		 	  		   	  			  	
    # Read in adjusted closing prices for given symbols, date range 			  		 			 	 	 		 		 	  		   	  			  	
    dates = pd.date_range(sd, ed)

    print type(dates)

    print type(syms)

    prices_all = get_data(syms, dates)  # automatically adds SPY
    print prices_all.head()
    prices = prices_all[syms]  # only portfolio symbols 			  		 			 	 	 		 		 	  		   	  			  	
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # find the allocations for the optimal portfolio 			  		 			 	 	 		 		 	  		   	  			  	
    # note that the values here ARE NOT meant to be correct for a test case 			  		 			 	 	 		 		 	  		   	  			  	
    # allocs = np.asarray([0.2, 0.2, 0.3, 0.3])
    # add code here to find the allocations
    n = len(syms)  # degree of the symbols
    # weights = np.random.rand(n)
    # allocs = weights / sum(weights)
 			  		 			 	 	 		 		 	  		   	  			  	
    # Get daily portfolio value 			  		 			 	 	 		 		 	  		   	  			  	
    # port_val = prices_SPY
    # add code here to compute daily portfolio values
    def get_port_val(al):
        # Step 1 normalized portfolio prices
        normalized_prices = prices / prices.ix[0, :]

        # step 2 allocate with daily prices
        allced_prices = normalized_prices * al

        # Step 3 daily portfolio value
        port_v = allced_prices.sum(axis=1)

        return port_v

    def get_stats(port_value):
        # cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1]
        # add code here to compute stats

        cr = port_value.tail(1).iloc[0] / port_value.head(1).iloc[0] - 1

        dr = port_value / port_value.shift(1) - 1
        dr.ix[0] = 0

        adr = dr.mean()

        sddr = dr.std()

        sr = math.sqrt(252) * (adr / sddr)

        return cr, adr, sddr, sr


    # define an inner function to minimize Sharpe Ratio
    def f(all):
        port_val = get_port_val(all)
        dr = port_val / port_val.shift(1) - 1
        dr[0] = 0
        sr = math.sqrt(252) * (dr.mean() / dr.std())
        y = - sr
        return y

    # call minimizer
    initial_guess = np.ones(n) * (1.0 / n)
    print initial_guess

    bounds = ((0.0, 1.0),) * len(syms)
    result = minimize(f, initial_guess, method='SLSQP', options={'disp': True}, bounds=bounds,
                          constraints=({'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs)},))

    # print "Allocates: ", result.x
    # print "Maximium Sharpe Ratio: ", -result.fun

    allocs = result.x
    port_val = get_port_val(allocs)
    cr, adr, sddr, sr = get_stats(port_val)

    # Compare daily portfolio value with SPY using a normalized plot
    prices_SPY = prices_SPY / prices_SPY.ix[0, :]  # normalize SPY

    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        ax = df_temp.plot(title="Daily Portfolio Value and SPY", fontsize=12)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        plt.savefig('plot.png', bbox_inches='tight')
        plt.show()
        plt.close()

    return allocs, cr, adr, sddr, sr
 			  		 			 	 	 		 		 	  		   	  			  	
def test_code(): 			  		 			 	 	 		 		 	  		   	  			  	
    # This function WILL NOT be called by the auto grader 			  		 			 	 	 		 		 	  		   	  			  	
    # Do not assume that any variables defined here are available to your function/code 			  		 			 	 	 		 		 	  		   	  			  	
    # It is only here to help you set up and test your code 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Define input parameters 			  		 			 	 	 		 		 	  		   	  			  	
    # Note that ALL of these values will be set to different values by 			  		 			 	 	 		 		 	  		   	  			  	
    # the autograder! 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X','GLD', 'JPM']
 			  		 			 	 	 		 		 	  		   	  			  	
    # Assess the portfolio 			  		 			 	 	 		 		 	  		   	  			  	
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date, syms = symbols, gen_plot = True)
 			  		 			 	 	 		 		 	  		   	  			  	
    # Print statistics 			  		 			 	 	 		 		 	  		   	  			  	
    print "Start Date:", start_date 			  		 			 	 	 		 		 	  		   	  			  	
    print "End Date:", end_date 			  		 			 	 	 		 		 	  		   	  			  	
    print "Symbols:", symbols

    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__ == "__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    # This code WILL NOT be called by the auto grader 			  		 			 	 	 		 		 	  		   	  			  	
    # Do not assume that it will be called 			  		 			 	 	 		 		 	  		   	  			  	
    test_code() 			  		 			 	 	 		 		 	  		   	  			  	
