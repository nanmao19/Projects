"""MC2-P1: Market simulator. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
 			  		 			 	 	 		 		 	  		   	  			  	
Student Name: Nan Mao (replace with your name)
GT User ID: nmao7 (replace with your User ID)
GT ID: 903363914 (replace with your GT ID)
""" 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
import os
import math
import sys
sys.path.insert(0, "/Users/imac/Dropbox/Summer 2019 7646/ML4T_2019Spring")
from util import get_data, plot_data

def author():
    return 'nmao7' # Change this to your user ID
 			  		 			 	 	 		 		 	  		   	  			  	
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code 			  		 			 	 	 		 		 	  		   	  			  	
    # NOTE: orders_file may be a string, or it may be a file object.
    # Your code should work correctly with either input
    # TODO: Your code here

    # read order data from orders_file and sort
    orders = pd.read_csv(orders_file)
    #orders = orders.sort_values(by = 'Date')
    for n in range(0, orders.shape[0]):
        if orders.ix[n, 'Date'] == '2011-06-15':
            orders = orders.drop([n])
    orders = orders.sort_values(by='Date')
    orders = orders.reset_index(drop=True)
    #print orders

    # get start date and end data from orders_file
    start_date = orders.iloc[0,0]
    #print start_date

    end_date = orders.iloc[-1,0]
    #print end_date

    dates = pd.date_range(start_date, end_date)

    # get symbols from order_file
    symbols = orders.Symbol.unique()
    symbols = symbols.tolist()
    print type(symbols)
    print symbols

    # read prices data
    prices = get_data(symbols, dates, addSPY=True)
    prices = prices.iloc[:, 1:]
    #print prices

    # create prices dataframe with Cash column = 1
    Cash = np.ones(prices.shape[0])
    prices['Cash'] = Cash
    #print "========PRICES======="
    #print prices.head(10)

    # create traders dateframe by copying prices and set all values = 0
    traders = prices * 0.0
    traders['Date'] = traders.index.date
    traders = traders.reset_index(drop=True)
    cols = traders.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    traders = traders[cols]
    # convert Date column to date string type
    traders['Date'] = traders['Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
    #print traders.head()

    # update order tradings changes

    for j in range(0, traders.shape[0]):
        for i in range(0, orders.shape[0]):

            if traders.ix[j,'Date']==orders.ix[i,'Date']:
                if orders.ix[i,'Order']=="BUY":
                    symbol = orders.ix[i, 'Symbol']
                    traders.ix[j, symbol] = traders.ix[j, symbol] + orders.ix[i, 'Shares']

                    impact_fee = prices.ix[j,symbol] * orders.ix[i,'Shares'] * impact
                    fees = commission + impact_fee
                    traders.ix[j, 'Cash'] = traders.ix[j, 'Cash'] - fees

                else: # "SELL" order
                    symbol = orders.ix[i, 'Symbol']
                    traders.ix[j, symbol] = traders.ix[j, symbol] - orders.ix[i, 'Shares']

                    impact_fee = prices.ix[j, symbol] * orders.ix[i, 'Shares'] * impact
                    fees = commission + impact_fee
                    traders.ix[j, 'Cash'] = traders.ix[j, 'Cash'] - fees
    #print "=======TRADERS======="
    #print traders.head()


    # create holdings dataframe with start portfolio value
    holdings = traders * 1
    #print holdings.head()
    holdings.ix[0, 'Cash'] = start_val + holdings.ix[0, 'Cash']

    for i in range(1, holdings.shape[0]):
        holdings.iloc[i, 1:-1] = holdings.iloc[i-1, 1:-1] + holdings.iloc[i, 1:-1]
        price_change = prices.iloc[i, 0:-1].values - prices.iloc[i-1, 0:-1].values
        holdings.iloc[i, -1] = holdings.iloc[i-1, -1] + traders.iloc[i, -1] + np.dot(price_change, holdings.iloc[i-1, 1:-1].values)

    #print "=======HOLDINGS======="
    #print holdings.head()

    # Get portfolio stats
    portvals = holdings.iloc[:, -1]
    keys = holdings['Date']

    df = pd.DataFrame(portvals.values, index=keys)
    #print "number of days:", portvals.shape[0]
    #print "final portfolio value:",df.iloc[-1, -1]

    dr = (portvals / portvals.shift(1)) - 1
    dr = dr[1:]
    adr = dr.mean()
    sddr = dr.std()
    sr = math.sqrt(252) * (adr / sddr)
    #print "sharpe ratio:", sr
    #print "average of daily return:", adr

    return df


def test_code(): 			  		 			 	 	 		 		 	  		   	  			  	
    # this is a helper function you can use to test your code 			  		 			 	 	 		 		 	  		   	  			  	
    # note that during autograding his function will not be called. 			  		 			 	 	 		 		 	  		   	  			  	
    # Define input parameters 			  		 			 	 	 		 		 	  		   	  			  	


    of = "./orders/orders-10.csv"
    sv = 1000000
    print "haha"
 			  		 			 	 	 		 		 	  		   	  			  	
    # Process orders 			  		 			 	 	 		 		 	  		   	  			  	
    portvals = compute_portvals(orders_file = of, start_val = sv) 			  		 			 	 	 		 		 	  		   	  			  	
    if isinstance(portvals, pd.DataFrame): 			  		 			 	 	 		 		 	  		   	  			  	
        portvals = portvals[portvals.columns[-1]] # just get the first column
    else: 			  		 			 	 	 		 		 	  		   	  			  	
        "warning, code did not return a DataFrame" 			  		 			 	 	 		 		 	  		   	  			  	


if __name__ == "__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    test_code() 			  		 			 	 	 		 		 	  		   	  			  	

