import numpy as np
import pandas as pd
import random
import math
import DTLearner as dt
import RTLearner as rt
import LinRegLearner as lrl
import BagLearner as bl
import InsaneLearner as it

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class BagLearner(object):

    def __init__(self, learner, kwargs, bags=20, boost=False, verbose=False):

        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.learnerList = []

    def author(self):

        return 'nmao7'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):

        # get learners and leanrer argument from key arguments
        #self.learnerList = []

        for i in range(0, self.bags):
            self.learnerList.append(self.learner(**self.kwargs))

        n = dataX.shape[0]  # compute the sample size

        for learner in self.learnerList:

            # randomly sample n tuple indeces from data
            index = []

            while len(index) < n:

                temp = random.randint(0, n - 1)

                index.append(temp)

            learner.addEvidence(dataX.take(index, axis=0), dataY.take(index, axis=0))

    def query(self, testX):

        pred = []
        #print testX

        for learner in self.learnerList:

            pred.append(learner.query(testX))

        #print pred
        predY = np.array(pred)

        Y = np.mean(predY, axis=0)

        return Y.tolist()


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

'''
data = pd.read_csv("data/istanbul.csv")
# data = pd.read_csv("data/testdata.csv")
data = data.iloc[:, 1:]
#print data.head()

train = data.sample(frac=0.60)  # randomly select 60% as training data
test = data.loc[data.index.difference(train.index)]  # set the rest data as test data

# split data for X and Y
trainX = train.iloc[:, 0:-1]
xtrain = trainX.values  # convert dataframe to np array

trainY = train.iloc[:, -1]
ytrain = trainY.values  # convert dataframe to np array

testX = test.iloc[:, 0:-1]
xtest = testX.values  # convert dataframe to np array

testY = test.iloc[:, -1]
ytest = testY.values  # convert dataframe to np array


learner = bl.BagLearner(learner = dt.DTLearner, kwargs = {"leaf_size": 1}, bags = 20, boost = False, verbose = False)

learner.addEvidence(xtrain, ytrain)

Y1 = learner.query(xtest)

print Y1


error1 = []
error2 = []

for i in range(1, 100, 1):
    learner = bl.BagLearner(learner = dt.DTLearner, kwargs = {"leaf_size": i}, bags = 20, boost = False, verbose = False)
    learner.addEvidence(xtrain, ytrain)

    # out sample error
    Y1 = learner.query(xtest)
    Yarray1 = np.asarray(Y1)
    rmse1 = math.sqrt(((ytest - Yarray1.astype(float)) ** 2).sum() / testY.shape[0])
    error1.append(rmse1)

    # in sample error
    Y2 = learner.query(xtrain)
    Yarray2 = np.asarray(Y2)
    rmse2 = math.sqrt(((ytrain - Yarray2.astype(float)) ** 2).sum() / trainY.shape[0])
    error2.append(rmse2)

x = [i for i in range(100)]
datalist = list(zip(x, error1, error2))

df = pd.DataFrame(datalist, columns = ['leaf size', 'out sample error', 'in sample error'])
#print df.head()
ax = df[['out sample error', 'in sample error']].plot()
ax.set_xlabel("leaf size")
ax.set_ylabel("RMSE")
plt.savefig('5.png', bbox_inches='tight')
plt.show()

'''



