import datetime as dt
import numpy as np
import pandas as pd
import util as ut
import random

import marketsimcode as ms
import ManualStrategy as mst
import StrategyLearner as sl
import TheoreticallyOptimalStrategy as to

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

if __name__ == "__main__":

    def author(self):
        return 'nmao7'  # Change this to your user ID

    def ll(imp):

        learner = sl.StrategyLearner(verbose=True, impact=imp)
        # training period
        sd1 = dt.datetime(2008, 1, 1)
        ed1 = dt.datetime(2009, 12, 31)

        symbol = 'JPM'
        syms = [symbol]
        sv = 1000000

        learner.addEvidence(symbol="JPM", sd=sd1, ed=ed1, sv=sv)  # training phase

        # testing period
        sd2 = dt.datetime(2010, 1, 1)
        ed2 = dt.datetime(2011, 12, 31)
        Ltrades = learner.testPolicy(symbol="JPM", sd=sd1, ed=ed1, sv=sv)  # testing phase
        # print df_trades

        # prepare trade dataframe format
        Ltrades = Ltrades.reset_index()
        Ltrades['Symbol'] = 'JPM'
        Ltrades = Ltrades.rename(columns={"index": "Date"})
        Ltrades['Order'] = 'SELL'
        for i in range(0, Ltrades.shape[0]):
            if Ltrades.ix[i, 'Shares'] > 0:
                Ltrades.ix[i, 'Order'] = 'BUY'

        # convert datetime to datetime string
        Ltrades['Date'] = Ltrades['Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
        #print "number of trades for impact rate", imp, ":", Ltrades.shape[0]

        # compute portfolio value for different impact
        pv = ms.compute_portvals(Ltrades, start_val=sv, commission=0, impact=imp)
        #print "ending portfolio value for impact rate", imp, ":", pv.iloc[-1, 0]
        return Ltrades, pv

    df = pd.DataFrame()
    endval = []
    impact_range = np.arange(0.00, 0.101, 0.005)
    print impact_range
    num_trade = []
    for n in impact_range:
        trades, tempPV = ll(n)
        #print trades.head(1)
        endval = np.append(endval, tempPV.iloc[-1, 0])
        num_trade = np.append(num_trade, trades.shape[0])
        df = pd.concat([df, tempPV], axis=1, sort=True)
    df.columns = impact_range
    df.iloc[0,:] = 1000000
    df = df.fillna(method='ffill')
    df = df.fillna(method='bfill')

    plt.plot(impact_range, num_trade)
    plt.title("impact rate VS number of trade")
    plt.xlabel('impact rate')
    plt.ylabel('number of trade')
    plt.savefig('impact rate VS number of trade plot.png')
    plt.show()
    comb = pd.DataFrame({'impact_range': impact_range, 'endval': endval})
    comb.plot(x='impact_range', y='endval', figsize=(20, 8))
    plt.title("impact rate VS ending portfolio values")
    plt.xlabel('impact rate')
    plt.ylabel('ending portfolio value')
    plt.savefig('impact rate VS ending portfolio values plot.png')
    plt.show()