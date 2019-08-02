'''
Your code that implements your indicators as functions that operate on dataframes.
The "main" code in indicators.py should generate the charts that illustrate your indicators in the report.
'''

def author():
    return 'nmao7' # Change this to your user ID

import pandas as pd
import datetime as dt
import sys
sys.path.insert(0, "/Users/imac/Dropbox/Summer 2019 7646/ML4T_2019Spring")
from util import get_data, plot_data
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def author():
    return 'nmao7' # Change this to your user ID

def test_code():

    train_start_date = dt.datetime(2008,01,01)
    train_end_date = dt.datetime(2009,12,31)
    train_dates = pd.date_range(train_start_date, train_end_date)

    test_start_date = dt.datetime(2010,01,01)
    test_end_date = dt.datetime(2011,12,31)
    test_dates = pd.date_range(test_start_date, test_end_date)

    symbols = ['JPM']

    prices = get_data(symbols, train_dates, addSPY=True)
    prices = prices/prices.iloc[0]
    print prices.head()

    vol(prices, symbols, 10)
    #print prices.head()

    sma_indicator(prices, symbols, 10)
    #print prices.head()

    bb_indicator(prices,symbols,10)
    print prices.head()

    ema_indicator(prices, symbols,10)
    print prices[['JPM','SMA','EMA']].head()

def vol(df, sym, window):

    # calculate std of daily return
    df['STD'] = df[sym].rolling(window=window).std()
    df[[sym[0], 'STD']].plot(figsize=(20, 8))
    plt.savefig('STD Plot.png')
    return df

def sma_indicator(df, sym, window):

    # get Standard Deviation value
    df = vol(df, sym, window)

    # calculate SMA indicator
    df['SMA'] = df[sym].rolling(window=window).mean()
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    df['P_SMA'] = df['JPM']/df['SMA']

    # plot daily price and SMA
    df[[sym[0], 'SMA', 'P_SMA']].plot(figsize=(20,8))
    plt.savefig('SMA Plot.png')
    return df

def bb_indicator(df, sym, window):

    # get SMA value
    df = sma_indicator(df, sym, window)

    # calculte Bollinger Bands
    df['Upper'] = df['SMA'] + 2 * df['STD']
    df['Lower'] = df['SMA'] - 2 * df['STD']

    # plot daily price, SMA and Bollinger Bands
    df[[sym[0], 'SMA', 'Upper', 'Lower']].plot(figsize=(20, 8))
    plt.savefig('Bollinger Bands Plot.png')

    return df

def ema_indicator(df, sym, window):

    # calculate EMA
    multiplier = 2.0/(window + 1)

    df.ix[0,'EMA'] = df.ix[0, 'SMA']
    for i in range(1, df.shape[0]):
        df.ix[i,'EMA'] = df.ix[i,'JPM'] * multiplier + df.ix[i-1, 'EMA'] * (1 - multiplier)

    # plot daily price and EMA
    df[[sym[0], 'SMA', 'EMA']].plot(figsize=(20, 8))
    plt.savefig('EMA Plot.png')
    plt.show()
    return df

if __name__ == "__main__":
    test_code()