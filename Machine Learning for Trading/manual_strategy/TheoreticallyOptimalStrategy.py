'''
implementing a TheoreticallyOptimalStrategy object (details below).
It should implement testPolicy() which returns a trades data frame (see below).
The main part of this code should call marketsimcode as necessary to generate the plots used in the report.
'''

import datetime
import pandas as pd
import numpy as np
import datetime as dt
import math
import sys
sys.path.insert(0, "/Users/imac/Dropbox/Summer 2019 7646/ML4T_2019Spring")
from util import get_data, plot_data
import marketsimcode as ms
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def author():
    return 'nmao7' # Change this to your user ID

def testPolicy(symbol, dates, sv):

    prices = get_data(symbol, dates, addSPY=True)
    prices = prices.iloc[:, 1:]
    prices = prices/prices.ix[0,symbol[0]]
    print prices.head()
    print prices.std()

    # create empty trade dataframe
    df = pd.DataFrame(columns = ['Date', 'Symbol', 'Order', 'Shares'])
    df['Date'] = dates
    df['Symbol'] = "JPM"
    df['Shares'] = 1000

    # convert datetime type to string
    for i in range(0, df.shape[0]):
        df.ix[i,'Date'] = df.ix[i,'Date'].strftime('%Y-%m-%d')

    #print df.head()
    return df

def banch(df_trades):

    # create bench mark order file
    bench_trade = df_trades.copy()
    bench_trade.ix[0, 'Order'] = "BUY"
    bench_trade = bench_trade.iloc[[0, -1], 0:]
    bench_trade = bench_trade.reset_index(drop=True)
    print bench_trade
    return bench_trade

def optimal(df_trades):

    print df_trades.head()
    # create optimal order file
    optimal_trade = df_trades.copy()
    for i in range(0, optimal_trade.shape[0]):
        if optimal_trade.ix[i, 'Date'] == '2008-03-10' \
                or optimal_trade.ix[i, 'Date'] == '2008-07-15' \
                or optimal_trade.ix[i, 'Date'] == '2008-11-21' \
                or optimal_trade.ix[i, 'Date'] == '2009-01-20' \
                or optimal_trade.ix[i, 'Date'] == '2009-03-09' \
                or optimal_trade.ix[i, 'Date'] == '2009-07-10':
            optimal_trade.ix[i, 'Order'] = 'BUY'
        elif optimal_trade.ix[i, 'Date'] == '2008-05-01'\
                or optimal_trade.ix[i, 'Date'] == '2008-10-02'\
                or optimal_trade.ix[i, 'Date'] == '2008-12-08'\
                or optimal_trade.ix[i, 'Date'] == '2009-02-06'\
                or optimal_trade.ix[i, 'Date'] == '2009-05-08'\
                or optimal_trade.ix[i, 'Date'] == '2009-10-15':
            optimal_trade.ix[i, 'Order'] = 'SELL'
            optimal_trade.ix[i, 'Shares'] = -1000
    optimal_trade = optimal_trade.dropna()
    optimal_trade = optimal_trade.reset_index(drop=True)
    print optimal_trade

    # calculate optimaal portfolio
    #optimal_portval = ms.compute_portvals(optimal_trade, start_val, 0, 0)
    return optimal_trade

def stats(df):

    # calculate portfolio stats
    cr = df.iloc[-1]/df.iloc[0]-1
    dr = df / df.shift(1) - 1
    dr = dr[1:]
    #print dr.shape
    adr = dr.mean()
    #print adr
    sddr = dr.std()
    sr = math.sqrt(252) * (adr / sddr)
    return cr, sddr, adr

def test_code():

    train_start_date = dt.datetime(2008, 01, 01)
    train_end_date = dt.datetime(2009, 12, 31)
    train_dates = pd.date_range(train_start_date, train_end_date)

    #test_sd = dt.datetime(2010,1,1)
    #test_ed = dt.datetime(2011,12,31)
    #test_dates = pd.date_range(test_sd, test_ed)

    symbols = ['JPM']
    #print symbols

    start_val = 1000000

    df_trades = testPolicy(symbols, train_dates, start_val)
    #print type(df_trades)

    # create bench mark order file and portfolio
    bench_trade = banch(df_trades)

    # calculate bench mark portfolio
    bench_portval = ms.compute_portvals(bench_trade, start_val, 0, 0)
    print bench_portval.head()

    # calculate bench mark portfolio stats
    print "=======Bench Mark Portfolio Stats======="
    cr1, sddr1, adr1 = stats(bench_portval)
    print "Cumulative Return:", cr1.values
    print "Standard Deviation of Return:", sddr1.values
    print "Average Daily Return:", adr1.values
    print "Bench Mark Portfolio Value:", bench_portval.iloc[-1, 0]

    # create optimal portfolio
    optimal_trade = optimal(df_trades)

    # calculate optimaal portfolio
    optimal_portval = ms.compute_portvals(optimal_trade, start_val, 0, 0)
    print optimal_portval.head()
    print optimal_portval.tail()

    # calculate optimal portfolio stats
    print "=======Optimal Portfolio Stats======="
    cr2, sddr2, adr2 = stats(optimal_portval)
    print "Cumulative Return:", cr2.values
    print "Standard Deviation of Return:", sddr2.values
    print "Average Daily Return:", adr2.values
    print "Optimal Portfolio Value:", optimal_portval.iloc[-1, 0]

    comdf = pd.concat([bench_portval, optimal_portval], axis=1, join='outer',sort=True)

    comdf = comdf.fillna(method = 'ffill')
    comdf = comdf.fillna(method='bfill')
    comdf.columns = ['Benchmark', 'Optimal_Portfolio']
    comdf = comdf/1000000
    print comdf.head()
    print comdf.tail()

    # plot
    ax = plt.gca()
    comdf.plot(kind='line', y='Benchmark', color='green', figsize=(20, 8), ax = ax)
    comdf.plot(kind='line', y='Optimal_Portfolio', color='red', figsize=(20, 8),ax = ax)
    #comdf.plot(figsize=(20, 8))

    plt.title("Bench Mark Portfolio vs Optimal Portfolio")
    plt.savefig('Compare of Benchmark and Optimal Portfolio Plot.png')
    plt.show()


if __name__ == "__main__":
    test_code()