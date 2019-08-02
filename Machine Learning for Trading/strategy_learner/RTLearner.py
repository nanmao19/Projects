import numpy as np
import pandas as pd
import random
from scipy import stats

class RTLearner(object):

    def __init__(self, leaf_size=5, verbose=False):
        # pass # move along, these aren't the drones you're looking for
        self.tree = None
        self.leaf_size = leaf_size

    def author(self):

        return 'nmao7'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):

        dataY = np.array([dataY])
        new_dataY = dataY.T  # transpose of dataY

        data = np.append(dataX, new_dataY, axis=1)

        if data.shape[0] <= self.leaf_size:  # if nodes < leaf-size
            mode = stats.mode(data[:, -1])
            #mode = np.bincount(data[:, -1]).argmax()
            return np.array([["leaf", mode[0][0], float('Nan'), float('Nan')]])

        if np.all(data[0, -1] == data[:, -1], axis=0):  # if all dataY are same
            mode = stats.mode(data[:, -1])
            #mode = np.bincount(data[:, -1]).argmax()

            return np.array([["leaf", mode[0][0], float('Nan'), float('Nan')]])

        else:
            feature = int(self.random_split(data))

            mode = stats.mode(data[:, feature])
            #mode = np.bincount(data[:, feature]).argmax()

            split_val = mode[0][0]  # median of all values in column of best feature

            # when all data less than split value, only build left tree
            if max(data[:, feature]) == split_val:
                mode = stats.mode(data[:, -1])
                #mode = np.bincount(data[:, -1]).argmax()
                #print mode

                return np.array([['leaf', mode[0][0], float('Nan'), float('Nan')]])

            ldata = data[data[:, feature] <= split_val]
            rdata = data[data[:, feature] > split_val]

            lefttree = self.addEvidence(ldata[:, 0:-1], ldata[:, -1])
            righttree = self.addEvidence(rdata[:, 0:-1], rdata[:, -1])

            root = np.array([[feature, split_val, 1, lefttree.shape[0] + 1]])
            temp = np.append(root, lefttree, axis=0)
            self.tree = np.append(temp, righttree, axis=0)

            return self.tree

    def random_split(self, data):

        dataX = data[:, 0:-1] # count the feature column

        return random.randint(0, dataX.shape[1]-1) # randomly return a integer from 0 to # of all feature columns

    def query(self, testX):

        pred = []

        for n in range(0, testX.shape[0]):

            test_tuple = testX[n, :]# pass the current row to query_tree() to determine corresponding value

            i = 0
            while (self.tree[i, 0] != 'leaf'): # if track a non-leaf node

                index = self.tree[i, 0]
                split_val = self.tree[i, 1]

                if test_tuple[int(float(index))] <= float(split_val):
                    i = i + int(float(self.tree[i, 2]))  # track in left tree
                else:
                    i = i + int(float(self.tree[i, 3]))  # track in right tree

            pred.append(float(self.tree[i, 1])) # if track a leaf node

        return pred

if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

'''
data = pd.read_csv("data/testdata.csv")
data = data.iloc[:, 1:]
#print data.head()

train = data.sample(frac=0.60) # randomly select 60% as training data
test = data.loc[data.index.difference(train.index)] # set the rest data as test data

# split data for X and Y
trainX = train.iloc[:, 0:-1]
xtrain = trainX.values # convert dataframe to np array

trainY = train.iloc[:, -1]
ytrain = trainY.values # convert dataframe to np array

testX = test.iloc[:, 0:-1]
xtest = testX.values # convert dataframe to np array

testY = test.iloc[:, -1]
ytest = testY.values # convert dataframe to np array

import RTLearner as rt
learner = rt.RTLearner(leaf_size=1, verbose=False)

tree = learner.addEvidence(xtrain, ytrain)  # pass the training arrays
#print type(tree)
print tree

Y = learner.query(xtest)  # query

predY = pd.DataFrame(data = Y)

print predY

'''

