import numpy as np
import pandas as pd
import DTLearner as dt
import random
import math
from scipy.stats.stats import pearsonr


class DTLearner(object):

    def __init__(self, leaf_size, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        pass  # move along, these aren't the drones you're looking for

    def author(self):
        return 'nmao7'  # replace tb34 with your Georgia Tech username

    def get_splits(self, dataX, dataY): # determine the best feature by maximum correlation

        data = pd.concat([dataX, dataY], axis=1)
        coef = []

        for column_index in range (data.shape[1]-1):

            temp_x = data.iloc[:, column_index]

            temp_y = data.iloc[:, -1]

            corr = np.corrcoef(temp_x, temp_y)[0,1]

            coef.append(corr)

        split_col = coef.index(max(coef))  ####
        #print "split column:", split_col

        '''
        if coef.isnull:
            a = list(corrdf.columns)
            split_col = random.choice(a) # randomly pick a column if all correlation is NaN
            print "split factor1:", split_col, type(split_col)

        else:
            split_col = corrdf.idxmax(axis=0, skipna=True)  # get maximum correlation column index
            print "split factor2:", int(split_col.values)
        '''

        selection = dataX.iloc[:, split_col]  # select the maximum correlation column data !!!!!!
        #print selection, type(selection)

        split_val = selection.median()  # calculate the split value
        #print "split value:", split_val

        return split_col, split_val

    def addEvidence(self, dataX, dataY):

        dfX = pd.DataFrame(data=dataX) # convert array to dataframe
        dfY = pd.DataFrame(data=dataY)

        if dfX.shape[0] <= self.leaf_size:  # less than leaf_size row

            #print "leaf 1"
            return ['leaf', np.median(dataY), float('NaN'), float('NaN')]

        elif len(np.unique(dfY.values)) == 1:  # if all Y are same

            #print "leaf 2"
            return ['leaf', np.median(dataY), float('NaN'), float('NaN')]

        else:

            split_index, split_val = self.get_splits(dfX, dfY)
            #print "split index:", split_index, type(split_index)
            #print "split value:", split_val, type(split_val)

            data = pd.concat([dfX, dfY], axis=1, ignore_index=True)
            #print data

            ldata = data[data.iloc[:, split_index] < split_val]
            rdata = data[data.iloc[:, split_index] >= split_val]

            lefttree = self.addEvidence(ldata.iloc[:, 0:-1], ldata.iloc[:, -1])
            righttree = self.addEvidence(rdata.iloc[:, 0:-1], rdata.iloc[:, -1])
            print type(lefttree)
            a = np.array([lefttree])

            #root = [split_index, split_val, 1, lefttree.shape[0]+1]
            root = [split_index, split_val, 1, a.shape[-2]+1]

            self.tree = (np.vstack((root, lefttree, righttree)))

            return self.tree


    def query(self, dataX):

        testX = pd.DataFrame(data=dataX)

        pred = np.zeros(1)

        for n in range(0, testX.shape[0]):

            test_tuple = testX.iloc[n,:]  #select each row of test data
            #print test_tuple

            if type(self.tree) is list:

                y = self.tree[1]
                pred = np.append(pred, y)

            else :

                i = 0
                while i in range(0, self.tree.shape[0]):

                    if self.tree[i][0] == "leaf":
                        y = self.tree[i][1]
                        break

                    else:
                        index = int(float(self.tree[i][0]))
                        split_val = float(self.tree[i][1])

                        if test_tuple[index] < split_val:
                            i = i + int(float(self.tree[i][2]))  # go left tree

                        else:
                            i = i + int(float(self.tree[i][3]))  #go right tree

                pred = np.append(pred, y)

            n = n + 1

        pred = pred[1:]

        return pred.astype(float)

'''
######### data prepare #########
#data = pd.read_csv("data/Istanbul.csv")
data = pd.read_csv("data/testdata.csv")
data = data.iloc[:, 1:]
print data.head()

train = data.sample(frac=0.60) # randomly select 60% as training data
#train = data
test = data.loc[data.index.difference(train.index)] # set the rest data as test data

# split data for X and Y
trainX = train.iloc[:, 0:-1]
xtrain = trainX.values # convert dataframe to np array
#print "training data:"
#print trainX

trainY = train.iloc[:, -1]
ytrain = trainY.values # convert dataframe to np array

testX = test.iloc[:, 0:-1]
xtest = testX.values # convert dataframe to np array
testY = test.iloc[:, -1]
ytest = testY.values # convert dataframe to np array

######### train data #########
learner = dt.DTLearner(leaf_size=5, verbose=False)

tree = learner.addEvidence(xtrain, ytrain)  # pass the training arrays
print "tree:"
print tree

######### query from the tree to get prediction #########
#print testX

Y = learner.query(xtest)  # query

#predY = pd.DataFrame(data = Y)
print "prediction from tree:"
#print Y
#print Y.shape
#print type(predY.values), predY.values.shape
print "prediction from data:"
#print ytest
#print type(ytest), ytest.shape
#print ytest - Y


#rmse = math.sqrt(((ytest - Y.astype(float)) ** 2).sum() / testY.shape[0])
#print rmse

'''
if __name__=="__main__":
    print "the secret clue is 'zzyzx'"

