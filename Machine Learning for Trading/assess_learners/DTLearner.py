import numpy as np
import pandas as pd

import math
import DTLearner as dt
import RTLearner as rt

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):

        # pass # move along, these aren't the drones you're looking for
        self.leaf_size = leaf_size

    def author(self):

        return 'nmao7'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):

        dataY = np.array([dataY])
        new_dataY = dataY.T  # transpose of dataY

        data = np.append(dataX, new_dataY, axis=1)

        self.tree = self.build_tree(data)

    def build_tree(self, data):

        if data.shape[0] <= self.leaf_size:  # if nodes < leaf-size
            return np.array([["leaf", np.median(data[:, -1]), float('Nan'), float('Nan')]])

        if np.all(data[0, -1] == data[:, -1], axis=0):  # if all dataY are same
            return np.array([["leaf", np.median(data[:, -1]), float('Nan'), float('Nan')]])

        else:
            feature = int(self.split(data))
            split_val = np.median(data[:, feature])  # median of all values in column of best feature

            # when all data less than split value, only build left tree
            if max(data[:, feature]) == split_val:
                return np.array([['leaf', np.mean(data[:, -1]), float('Nan'), float('Nan')]])

            ldata = data[data[:, feature] <= split_val]
            rdata = data[data[:, feature] > split_val]

            lefttree = self.build_tree(ldata)
            righttree = self.build_tree(rdata)

            root = np.array([[feature, split_val, 1, lefttree.shape[0] + 1]])
            temp = np.append(root, lefttree, axis=0)
            self.tree = np.append(temp, righttree, axis=0)

            return self.tree

    def split(self, data):
        # returns index of selected feature column

        df = pd.DataFrame(data=data)
        coef = []

        for column_index in range(df.shape[1] - 1):
            tempX = df.iloc[:, column_index]  # split data to feature parts
            tempY = df.iloc[:, -1]  # split data to label parts

            corr = np.corrcoef(tempX, tempY)[0, 1]  # compute correlation between each feature column and label

            coef.append(corr)  # storage correlations into a list

        split_col = coef.index(max(coef))  # pick the maximum correlation feature column

        return split_col

    def query(self, testX):

        pred = []

        for n in range(0, testX.shape[0]):

            test_tuple = testX[n, :]  # pass the current row to query_tree() to determine corresponding value

            i = 0
            while (self.tree[i, 0] != 'leaf'):  # if track a non-leaf node

                index = self.tree[i, 0]
                split_val = self.tree[i, 1]

                if test_tuple[int(float(index))] <= float(split_val):
                    i = i + int(float(self.tree[i, 2]))  # track in left tree
                else:
                    i = i + int(float(self.tree[i, 3]))  # track in right tree

            pred.append(float(self.tree[i, 1]))  # if track a leaf node

        return pred

if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

'''
data = pd.read_csv("data/istanbul.csv")
#data = pd.read_csv("data/testdata.csv")
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

learner = dt.DTLearner(leaf_size=1, verbose=False)

tree = learner.addEvidence(xtrain, ytrain)  # pass the training arrays
#print type(tree)
print tree

Y = learner.query(xtest)  # query

Yarray = np.asarray(Y)

error1 = []
error2 = []
for i in range(1, 100, 1):
    learner = dt.DTLearner(leaf_size=i, verbose=False)
    tree = learner.addEvidence(xtrain, ytrain)

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

#print "out sample error for different leaf sizes:"
#print error1[0:10]
#print "in sample error for different leaf sizes:"
#print error2[0:10]

x = [i for i in range(100)]
datalist = list(zip(x, error1, error2))

df = pd.DataFrame(datalist, columns = ['leaf size', 'out sample error', 'in sample error'])
print df.head()
ax = df[['out sample error', 'in sample error']].plot()
ax.set_xlabel("leaf size")
ax.set_ylabel("RMSE")
plt.savefig('RMSE.png', bbox_inches='tight')
plt.show()


########## compare out sample error between DT and RT ##########
# out sample error from DT
error1 = []

for i in range(1, 100, 1):

    learner1 = dt.DTLearner(leaf_size=i, verbose=False)
    learner1.addEvidence(xtrain, ytrain)

    Y1 = learner1.query(xtest)
    Yarray1 = np.asarray(Y1)
    rmse1 = math.sqrt(((ytest - Yarray1.astype(float)) ** 2).sum() / testY.shape[0])
    error1.append(rmse1)

# out sample error from RT
error2 = []
for i in range(1, 100, 1):

    learner2 = rt.RTLearner(leaf_size=i, verbose=False)
    learner2.addEvidence(xtrain, ytrain)

    Y2 = learner2.query(xtest)
    Yarray2 = np.asarray(Y2)
    rmse2 = math.sqrt(((ytest - Yarray2.astype(float)) ** 2).sum() / testY.shape[0])
    error2.append(rmse2)

x = [i for i in range(100)]
datalist = list(zip(x, error1, error2))

df = pd.DataFrame(datalist, columns = ['leaf size', 'DT out sample error', 'RT out sample error'])
#print df.head()
ax = df[['DT out sample error', 'RT out sample error']].plot()
ax.set_xlabel("leaf size")
ax.set_ylabel("RMSE")
plt.savefig('3.png', bbox_inches='tight')
plt.show()

import statistics
print "statistics from out sample error of DTLearner:"
print "mean:", sum(error1)/len(error1)
print "standard deviation:", statistics.stdev(error1)
print "max value:", max(error1)
print "min value:", min(error1)

print "statistics from out sample error of RTLearner:"
print "mean:", sum(error2)/len(error2)
print "standard deviation:", statistics.stdev(error2)
print "max value:", max(error2)
print "min value:", min(error2)


########## compare in sample error between DT and RT ##########
# in sample error from DT
error1 = []

for i in range(1, 100, 1):

    learner1 = dt.DTLearner(leaf_size=i, verbose=False)
    learner1.addEvidence(xtrain, ytrain)

    Y1 = learner1.query(xtrain)
    Yarray1 = np.asarray(Y1)
    rmse1 = math.sqrt(((ytrain - Yarray1.astype(float)) ** 2).sum() / trainY.shape[0])
    error1.append(rmse1)

# out sample error from RT
error2 = []
for i in range(1, 100, 1):

    learner2 = rt.RTLearner(leaf_size=i, verbose=False)
    learner2.addEvidence(xtrain, ytrain)

    Y2 = learner2.query(xtrain)
    Yarray2 = np.asarray(Y2)
    rmse2 = math.sqrt(((ytrain - Yarray2.astype(float)) ** 2).sum() / trainY.shape[0])
    error2.append(rmse2)

x = [i for i in range(100)]
datalist = list(zip(x, error1, error2))

df = pd.DataFrame(datalist, columns = ['leaf size', 'DT in sample error', 'RT in sample error'])
#print df.head()
ax = df[['DT in sample error', 'RT in sample error']].plot()
ax.set_xlabel("leaf size")
ax.set_ylabel("RMSE")
plt.savefig('4.png', bbox_inches='tight')
plt.show()

import statistics
print "statistics from in sample error of DTLearner:"
print "mean:", sum(error1)/len(error1)
print "standard deviation:", statistics.stdev(error1)
print "max value:", max(error1)
print "min value:", min(error1)

print "statistics from in sample error of RTLearner:"
print "mean:", sum(error2)/len(error2)
print "standard deviation:", statistics.stdev(error2)
print "max value:", max(error2)
print "min value:", min(error2)
'''