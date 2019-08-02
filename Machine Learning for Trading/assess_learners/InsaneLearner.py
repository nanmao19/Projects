import numpy as np
import pandas as pd
import DTLearner as dt
import RTLearner as rt
import LinRegLearner as lrl
import BagLearner as bl
import InsaneLearner as it

class InsaneLearner(object):

    def __init__(self, verbose=False):

        pass

    def author(self):

        return 'nmao7'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):

        self.learner_list = []

        for i in range(0, 20):

            self.learner_list.append(bl.BagLearner(dt.DTLearner, kwargs={"leaf_size": 1}, bags=20))

        for learner in self.learner_list:

            learner.addEvidence(dataX, dataY)

    def query(self, testX):

        pred = []
        #print testX

        for learner in self.learner_list:

            pred.append(learner.query(testX))

        #print pred
        predY = np.array(pred)

        Y = np.mean(predY, axis=0)

        return Y.tolist()

if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

'''
data = pd.read_csv("data/testdata.csv")
data = data.iloc[:, 1:]
print data.head()

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

learner = it.InsaneLearner(verbose=False)

learner.addEvidence(xtrain, ytrain)

# Y = learner.query(xtest)  # query
'''