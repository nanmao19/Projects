'''
implementing a ManualStrategy object (your manual strategy).
It should implement testPolicy() which returns a trades data frame (see below).
The main part of this code should call marketsimcode as necessary to generate the plots used in the report.
'''

import datetime
import time
import pandas as pd
import numpy as np
import datetime as dt
import math
import sys
sys.path.insert(0, "/Users/imac/Dropbox/Summer 2019 7646/ML4T_2019Spring")
from util import get_data, plot_data
import marketsimcode as ms
import indicators as id
import TheoreticallyOptimalStrategy as to
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def author():
    return 'nmao7' # Change this to your user ID

def testPolicy(dates):

    # create empty trade dataframe
    df = pd.DataFrame(columns = ['Date', 'Symbol', 'Order', 'Shares'])
    df['Date'] = dates
    df['Symbol'] = "JPM"
    df['Shares'] = 1000

    # convert datetime type to string
    for i in range(0, df.shape[0]):
        df.ix[i,'Date'] = df.ix[i,'Date'].strftime('%Y-%m-%d')

    return df

def banch(df, start_val):

    # create bench mark order file
    bench_trade = df.copy()
    bench_trade.ix[0, 'Order'] = "BUY"
    bench_trade = bench_trade.iloc[[0, -1], 0:]
    bench_trade = bench_trade.reset_index(drop=True)
    print bench_trade

    # calculate bench mark portfolio
    bench_portval = ms.compute_portvals(bench_trade, start_val, 0, 0)
    return bench_portval

def ManualRule(df, sym, window):

    # get std, SMA and BB values
    df = id.bb_indicator(df, sym, window)
    df = id.ema_indicator(df, sym, window)
    print df.head()

    # set buy/sell order based on bollinger band
    holding = 0

    # set first day value
    df.ix[0, 'Symbol'] = 'JPM'
    df.ix[0, 'Order'] = 'Hold'
    df.ix[0, 'Shares'] = holding

    for i in range(2, df.shape[0]):
        if df.ix[i-1,'JPM'] > df.ix[i-1, 'Upper'] \
                and df.ix[i-1,'P_SMA'] > 1.05 \
                and df.ix[i-1, 'EMA'] > df.ix[i-2, 'EMA']:
            df.ix[i, 'Symbol'] = 'JPM'
            df.ix[i, 'Order'] = 'SELL'
            if holding == 0:
                df.ix[i, 'Shares'] = -1000
            if holding == -1000:
                df.ix[i, 'Shares'] = 0
            if holding == 1000:
                df.ix[i, 'Shares'] = -2000
            holding = holding + df.ix[i, 'Shares']
            #print holding

        if df.ix[i-1, 'JPM'] < df.ix[i-1, 'Lower'] \
                and df.ix[i-1,'P_SMA'] < 0.95\
                and df.ix[i-1, 'EMA'] < df.ix[i-2, 'EMA']:
            df.ix[i, 'Symbol'] = 'JPM'
            df.ix[i, 'Order'] = 'BUY'
            if holding == 0:
                df.ix[i, 'Shares'] = 1000
            if holding == -1000:
                df.ix[i, 'Shares'] = 2000
            if holding == 1000:
                df.ix[i, 'Shares'] = 0
            holding = holding + df.ix[i, 'Shares']
            #print holding

    # set last day value
    df.ix[-1,'Symbol'] = 'JPM'
    df.ix[-1,'Order'] = 'Hold'
    df.ix[-1, 'Shares'] = holding
    df = df.dropna()
    df = df.drop(df[df['Shares'] == 0].index)
    return df.iloc[:, :4]

def test_code():

    train_start_date = dt.datetime(2008, 01, 01)
    train_end_date = dt.datetime(2009, 12, 31)
    train_dates = pd.date_range(train_start_date, train_end_date)

    symbols = ['JPM']
    start_val = 1000000

    prices = get_data(symbols, train_dates, addSPY=True)
    prices = prices.iloc[:, 1:]
    prices = prices / prices.ix[0, symbols[0]]
    print "===========prices=========="
    print prices.head()

    # create empty trade dataframe
    df_trades = testPolicy(train_dates)
    print "===========empty trade==========="
    print df_trades.head()

    # create Benchmark trade and calculate portfolio value
    BM_portval = banch(df_trades, start_val)
    print "===========bench mark portfolio============"
    print BM_portval.head()

    # calculate bench mark portfolio stats
    print "=======Bench Mark Portfolio Stats for Sample period======="
    cr1, sddr1, adr1 = to.stats(BM_portval)
    print "Cumulative Return:", cr1.values
    print "Standard Deviation of Return:", sddr1.values
    print "Average Daily Return:", adr1.values
    print "Bench Mark Portfolio Value:", BM_portval.iloc[-1, 0]

    # create Manual rule based trade dataframe
    # repare the price and trade data columns into one dataframe
    df_trades.set_index('Date', inplace=True)
    df = pd.concat([prices, df_trades], axis=1, join='inner')
    print "===========Manual rule portfolio============"
    print df.head()

    # use price to generate trade orders by using the indicators
    df_MS = ManualRule(df, symbols, 10)

    # process trading order dataframe
    df_MS = df_MS.reset_index()     # reset integer index and save Date column
    #df_MS = df_MS.ix[:, 'index':'Shares']   # slicing the useful columns
    df_MS = df_MS.rename(columns={'index': 'Date'})  # rename Date column
    df_MS['Date'] = df_MS['Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))  # convert Timestamp to Date string
    print "==============="
    print df_MS
    print

    # calculate portfolio value for Manual rule trade
    MS_portval = ms.compute_portvals(df_MS, start_val,9.95,0.005)
    print MS_portval.tail()

    # calculate Manual rule-based portfolio stats
    print "=======Manual rule-based Portfolio Stats for sample period======="
    cr3, sddr3, adr3 = to.stats(MS_portval)
    print "Cumulative Return:", cr3.values
    print "Standard Deviation of Return:", sddr3.values
    print "Average Daily Return:", adr3.values
    print "Manual rule-base Portfolio Value:", MS_portval.iloc[-1, 0]

    # combine benchmark and Manual rule-based portfolio data
    comb_portval = pd.concat([BM_portval, MS_portval], axis=1, join='outer',sort=True)
    comb_portval = comb_portval.fillna(method='ffill')
    comb_portval = comb_portval.fillna(value=start_val)
    comb_portval = comb_portval.fillna(method='bfill')
    comb_portval.columns = ['Benchmark', 'Manual_Strategy']
    comb_portval = comb_portval / 1000000
    comb_portval = comb_portval.set_index(pd.to_datetime(comb_portval.index))  # reset index from date string to datetime
    print comb_portval.head()

    # plot to Compare Benchmark and Manual Strategy portfolio value
    colorslist = ['green', 'red']
    comb_portval[['Benchmark', 'Manual_Strategy']].plot(figsize=(20, 8), color=colorslist)

    # add vertical line to BUY trading dates in color "blue"
    xcoordsBuy = df_MS['Date'].loc[df_MS['Order'] == 'BUY']
    for i in range(0,xcoordsBuy.shape[0]):
        xc = xcoordsBuy.iloc[i]
        plt.axvline(x=xc, color='blue')

    # add vertical line to SELL trading dates in color "black"
    xcoordsSell = df_MS['Date'].loc[df_MS['Order'] == 'SELL']
    for i in range(0,xcoordsSell.shape[0]):
        xc = xcoordsSell.iloc[i]
        plt.axvline(x=xc, color='black')
    plt.title("Bench Mark vs Manual Strategy (sample period)")
    plt.savefig('Compare of Benchmark and Manual Strategy Plot1.png')
    plt.show()

    ########Comparative Analysis##########
    # get testing period dates
    test_start_date = dt.datetime(2010, 01, 01)
    test_end_date = dt.datetime(2011, 12, 31)
    test_dates = pd.date_range(test_start_date, test_end_date)

    # get prices for test period
    prices2 = get_data(symbols, test_dates, addSPY=True)
    prices2 = prices2.iloc[:, 1:]
    prices2 = prices2 / prices2.ix[0, symbols[0]]
    print "======test period prices======"
    print prices2.head()

    df_trades2 = testPolicy(test_dates)
    print "===========test period empty trade==========="
    print df_trades2.head()

    # create Benchmark trade for test period and calculate portfolio value
    BM_portval2 = banch(df_trades2, start_val)
    print "===========test period bench mark============"
    print BM_portval2.tail()

    # calculate bench mark portfolio stats
    print "=======Bench Mark Portfolio Stats for test period======="
    cr2, sddr2, adr2 = to.stats(BM_portval2)
    print "Cumulative Return:", cr2.values
    print "Standard Deviation of Return:", sddr2.values
    print "Average Daily Return:", adr2.values
    print "Bench Mark Portfolio Value:", BM_portval2.iloc[-1, 0]

    # create Manual rule based trade dataframe for test period
    df_trades2.set_index('Date', inplace=True)
    df2 = pd.concat([prices2, df_trades2], axis=1, join='inner')
    print "===========test period Manual rule portfolio============"
    print df2.head()
    # generate rule-based trading orders
    df_MS2 = ManualRule(df2, symbols, 10)
    # process trading order dataframe
    df_MS2 = df_MS2.reset_index()
    df_MS2 = df_MS2.rename(columns={'index': 'Date'})
    df_MS2['Date'] = df_MS2['Date'].apply(
        lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
    print "=======test period trading orders========"
    print df_MS2

    # calculate portfolio value for test period Manual rule trade
    MS_portval2 = ms.compute_portvals(df_MS2, start_val, 9.95, 0.005)
    print MS_portval2.tail()

    # calculate Manual rule-based portfolio stats
    print "=======Manual Rule-based Portfolio Stats for test period======="
    cr4, sddr4, adr4 = to.stats(MS_portval2)
    print "Cumulative Return:", cr4.values
    print "Standard Deviation of Return:", sddr4.values
    print "Average Daily Return:", adr4.values
    print "Manual Rule-based Portfolio Value:", MS_portval2.iloc[-1, 0]

    # combine benchmark and Manual rule-based portfolio data
    comb_portval2 = pd.concat([BM_portval2, MS_portval2], axis=1, join='outer', sort=True)
    comb_portval2 = comb_portval2.fillna(method='ffill')
    comb_portval2 = comb_portval2.fillna(value=start_val)
    comb_portval2 = comb_portval2.fillna(method='bfill')
    comb_portval2.columns = ['Benchmark', 'Manual_Strategy']
    comb_portval2 = comb_portval2 / 1000000
    comb_portval2 = comb_portval2.set_index(pd.to_datetime(comb_portval2.index))
    print comb_portval2.head()

    # plot to Compare Benchmark and Manual Strategy portfolio value for test period
    colorslist = ['green', 'red']
    comb_portval2[['Benchmark', 'Manual_Strategy']].plot(figsize=(20, 8), color=colorslist)

    # add vertical line to BUY trading dates in color "blue"
    xcoordsBuy2 = df_MS2['Date'].loc[df_MS2['Order'] == 'BUY']
    for i in range(0, xcoordsBuy2.shape[0]):
        xc2 = xcoordsBuy2.iloc[i]
        plt.axvline(x=xc2, color='blue')

    # add vertical line to SELL trading dates in color "black"
    xcoordsSell2 = df_MS2['Date'].loc[df_MS2['Order'] == 'SELL']
    for i in range(0, xcoordsSell2.shape[0]):
        xc2 = xcoordsSell2.iloc[i]
        plt.axvline(x=xc2, color='black')
    plt.title("Bench Mark vs Manual Strategy (test period)")
    plt.savefig('Compare of Benchmark and Manual Strategy Plot2.png')
    plt.show()

if __name__ == "__main__":
    test_code()