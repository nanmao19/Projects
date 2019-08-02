import datetime as dt
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

    learner = sl.StrategyLearner(verbose=True, impact=0.000)
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
    #print df_trades

    # prepare trade dataframe format
    Ltrades = Ltrades.reset_index()
    Ltrades['Symbol'] = 'JPM'
    Ltrades = Ltrades.rename(columns = {"index":"Date"})
    Ltrades['Order'] = 'SELL'
    for i in range(0, Ltrades.shape[0]):
        if Ltrades.ix[i, 'Shares'] > 0:
            Ltrades.ix[i, 'Order'] = 'BUY'

    # convert datetime to datetime string
    Ltrades['Date'] = Ltrades['Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
    print Ltrades.head()

    # compute portfolio value
    L_portval = ms.compute_portvals(Ltrades, start_val = sv, commission=0, impact=0.005)
    print L_portval.tail()

    cr, sddr, adr = to.stats(L_portval)
    print "======Experiment 1 report======"
    print "Cumulative Return:", cr.values
    print "Standard Deviation of Return:", sddr.values
    print "Average Daily Return:", adr.values
    print "Experiment1 Portfolio Value:", L_portval.iloc[-1, 0]

    # get Manual Strategy portfolio and stats
    MS_portval = mst.test_code()
    print MS_portval.tail()

    # calculate Manual rule-based portfolio stats
    print "=======Manual rule-based Portfolio Stats for sample period======="
    cr2, sddr2, adr2 = to.stats(MS_portval)
    print "Cumulative Return:", cr2.values
    print "Standard Deviation of Return:", sddr2.values
    print "Average Daily Return:", adr2.values
    print "Manual rule-base Portfolio Value:", MS_portval.iloc[-1, 0]

    # combine benchmark and Manual rule-based portfolio data
    comb_portval = pd.concat([L_portval, MS_portval], axis=1, join='outer', sort=True)
    comb_portval = comb_portval.fillna(method='ffill')
    comb_portval = comb_portval.fillna(value=sv)
    comb_portval = comb_portval.fillna(method='bfill')
    comb_portval.columns = ['RTLearner', 'Manual_Strategy']
    comb_portval = comb_portval / 1000000
    comb_portval = comb_portval.set_index(pd.to_datetime(comb_portval.index))

    # plot to Compare RTLearner Strategy and Manual Strategy portfolio value for training period
    colorslist = ['green', 'red']
    comb_portval[['RTLearner', 'Manual_Strategy']].plot(figsize=(20, 8), color=colorslist)
    plt.title("RTLearner vs Manual Strategy (training period)")
    plt.savefig('Compare RTLearner and Manual Strategy Plot.png')
    plt.show()