""" 			  		 			 	 	 		 		 	  		   	  			  	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import util as ut
import indicators as id
import RTLearner as rt
import BagLearner as bl
 			  		 			 	 	 		 		 	  		   	  			  	
class StrategyLearner(object):

    def author(self):
        return 'nmao7'  # Change this to your user ID

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose 			  		 			 	 	 		 		 	  		   	  			  	
        self.impact = impact
        self.window = 10
        #self.learner = rt.RTLearner(leaf_size=5)
        self.learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size": 5}, bags = 20, boost = False, verbose = False)
 			  		 			 	 	 		 		 	  		   	  			  	
    # this method should create a QLearner, and train it for trading 			  		 			 	 	 		 		 	  		   	  			  	
    def addEvidence(self, symbol = "IBM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), sv = 10000):

        # get symbol prices
        syms=[symbol]
        n = dt.timedelta(days = self.window)
        dates = pd.date_range(sd-n, ed)
        prices = ut.get_data(syms, dates, addSPY=True)  # automatically adds SPY
        #print prices.head(10)

        df = prices.copy()

        # get SMA indicator
        df = id.sma_indicator(df, syms, self.window)
        std = df['STD'].mean()
        #print std

        # get BB indicator
        df = id.bb_indicator(df, syms, self.window)

        # get EMA indicator
        df = id.ema_indicator(df, syms, self.window)

        # calculate daily return as Y label
        df['dail_return'] = df[symbol]/df[symbol].shift(1) -1
        df= df.dropna()
        #print df.head()

        # prepare training features
        trainX = df[['STD', 'PSMA', 'Bollinger', 'PEMA']]
        #print trainX.head()

        df['Pred'] = 0
        for n in range(1, df.shape[0] - 1):
            if df.ix[n, 'dail_return'] > self.impact + 0.007:  # Long shares
                df.ix[n-1, 'Pred'] = 1

            elif df.ix[n, 'dail_return'] < - self.impact - 0.007:  # Short shares
                df.ix[n-1, 'Pred'] = -1

            else:
                df.ix[n-1, 'Pred'] = 0
        trainY = df.iloc[:, -1]
        #print trainY.head(50)
        #print df
        self.learner.addEvidence(trainX.values, trainY.values)

    # this method should use the existing policy and test it against new data 			  		 			 	 	 		 		 	  		   	  			  	
    def testPolicy(self, symbol = "IBM", sd=dt.datetime(2009,1,1), ed=dt.datetime(2010,1,1), sv=10000):
 			  		 			 	 	 		 		 	  		   	  			  	
        # here we build a fake set of trades. your code should return the same sort of data
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices = ut.get_data(syms, dates, addSPY=True)  # automatically adds SPY

        df_test = prices.copy()
        #print df_test.head()

        # get SMA indicator
        df_test = id.sma_indicator(df_test, syms, self.window)
        #print df_test.head(15)

        # get BB indicator
        df_test = id.bb_indicator(df_test, syms, self.window)
        #print df_test.head(15)

        # get EMA indicator
        df_test = id.ema_indicator(df_test, syms, self.window)
        #print df_test.head()

        # prepare testX
        testX = df_test[['STD', 'PSMA','Bollinger','PEMA']]
        #print "=======test X========"
        #print testX.head()

        # get test Y prediction
        df_test['Pred'] = self.learner.query(testX.values)

        # build trade dataframe
        df_test['Shares'] = 0
        #print df_test.head()
        holding = 0
        df_test.ix[0, 'Shares'] = holding

        for m in range(0, df_test.shape[0] - 1):
            if df_test.ix[m, 'Pred'] > 0:  # Long shares
                if holding == 0:
                    df_test.ix[m, 'Shares'] = 1000
                elif holding == -1000:
                    df_test.ix[m, 'Shares'] = 2000
                elif holding == 1000:
                    df_test.ix[m, 'Shares'] = 0

            elif df_test.ix[m, 'Pred'] < 0:  # Short shares
                if holding == 0:
                    df_test.ix[m, 'Shares'] = -1000
                elif holding == -1000:
                    df_test.ix[m, 'Shares'] = 0
                elif holding == 1000:
                    df_test.ix[m, 'Shares'] = -2000

            else:
                df_test.ix[m, 'Shares'] = 0
            holding = holding + df_test.ix[m, 'Shares']

        #print df_test.head(15)
        trades = df_test.iloc[:, -1:]
        #trades = trades[trades.index > sd]
        trades = trades[trades['Shares'] != 0]
        #print trades.head(10)
        #print trades.shape[0]
        #print df_test

        return trades
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__":

    learner = StrategyLearner(verbose=True, impact=0.000)
    # training period
    sd1 = dt.datetime(2008, 1, 1)
    ed1 = dt.datetime(2009, 12, 31)
    #learner.addEvidence(symbol="AAPL", sd=sd1, ed=ed1, sv=100000)  # training phase
    learner.addEvidence(symbol = "JPM", sd = sd1, ed = ed1, sv = 100000)
    # testing period
    sd2 = dt.datetime(2010, 1, 1)
    ed2 = dt.datetime(2011, 12, 31)
    df_trades = learner.testPolicy(symbol="JPM",sd=sd1,ed=ed1,sv=100000)  # testing phase
    #print "One does not simply think up a strategy"
