'''
An improved version of your marketsim code that accepts a "trades" data frame (instead of a file).
More info on the trades data frame below.
It is OK not to submit this file if you have subsumed its functionality into one of your other required code files.
'''

import pandas as pd
import numpy as np
import datetime as dt
import math
import sys

sys.path.insert(0, "/Users/imac/Dropbox/Summer 2019 7646/ML4T_2019Spring")
from util import get_data, plot_data


def author():
    return 'nmao7'  # Change this to your user ID

def compute_portvals(orders, start_val=1000000, commission=9.95, impact=0.005):

    # read order data from orders_file and sort
    #orders = pd.read_csv(orders)
    orders = orders.sort_values(by = ['Date'])
    orders = orders.reset_index(drop=True)
    #print "=======ORDERS======="
    #print orders.head()

    # get start date and end data from orders_file
    start_date = orders.iloc[0, 0]

    end_date = orders.iloc[-1, 0]

    dates = pd.date_range(start_date, end_date)

    # get symbols from order_file
    symbols = orders.Symbol.unique()
    symbols = symbols.tolist()

    # read prices data
    prices = get_data(symbols, dates, addSPY=True)
    prices = prices.iloc[:, 1:]
    #print "=======PRICES======="
    #print prices.head()

    # create prices dataframe with Cash column = 1
    prices['Cash'] = np.ones(prices.shape[0])

    # create traders dateframe by copying prices and set all values = 0
    traders = prices * 0.0
    traders['Date'] = traders.index.date
    traders = traders.reset_index(drop=True)
    cols = traders.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    traders = traders[cols]

    # convert Date column to date string type
    traders['Date'] = traders['Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
    # print traders.head()

    # update order tradings changes
    if orders.ix[0, 'Date'] < traders.ix[0, 'Date']:
        orders.ix[0, 'Date'] = traders.ix[0, 'Date']

    for j in range(0, traders.shape[0]):
        for i in range(0, orders.shape[0]):

            if traders.ix[j, 'Date'] == orders.ix[i, 'Date']:
                if orders.ix[i, 'Order'] == "BUY":
                        symbol = orders.ix[i, 'Symbol']
                        traders.ix[j, symbol] = traders.ix[j, symbol] + orders.ix[i, 'Shares']

                        impact_fee = prices.ix[j, symbol] * orders.ix[i, 'Shares'] * impact
                        fees = commission + impact_fee
                        traders.ix[j, 'Cash'] = traders.ix[j, 'Cash'] - fees

                elif orders.ix[i, 'Order'] == "SELL":  # "SELL" order
                        symbol = orders.ix[i, 'Symbol']
                        traders.ix[j, symbol] = traders.ix[j, symbol] + orders.ix[i, 'Shares']

                        impact_fee = prices.ix[j, symbol] * orders.ix[i, 'Shares'] * impact
                        fees = commission + impact_fee
                        traders.ix[j, 'Cash'] = traders.ix[j, 'Cash'] - fees
    #print "=======TRADERS======="
    #print traders.head()

    # create holdings dataframe with start portfolio value
    holdings = traders * 1
    # print holdings.head()
    holdings.ix[0, 'Cash'] = start_val + holdings.ix[0, 'Cash']

    for i in range(1, holdings.shape[0]):
        holdings.iloc[i, 1:-1] = holdings.iloc[i - 1, 1:-1] + holdings.iloc[i, 1:-1]
        price_change = prices.iloc[i, 0:-1].values - prices.iloc[i - 1, 0:-1].values
        holdings.iloc[i, -1] = holdings.iloc[i - 1, -1] + traders.iloc[i, -1] + np.dot(price_change,
                                                                                       holdings.iloc[i - 1,
                                                                                       1:-1].values)

    #print "=======HOLDINGS======="
    #print holdings.head()

    # Get portfolio stats
    portvals = holdings.iloc[:, -1]
    keys = holdings['Date']

    df = pd.DataFrame(portvals.values, index=keys)

    return df

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-11.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[-1]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"


if __name__ == "__main__":
    test_code()


