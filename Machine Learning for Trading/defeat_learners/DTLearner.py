""" 			  		 			 	 	 		 		 	  		   	  			  	
A simple wrapper for linear regression.  (c) 2015 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
Note, this is NOT a correct DTLearner; Replace with your own implementation. 			  		 			 	 	 		 		 	  		   	  			  	
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
 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np
import pandas as pd
import warnings
import DTLearner as dt


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
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
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

learner = dt.DTLearner(leaf_size=1, verbose=False)
learner.addEvidence(xtrain, ytrain)

predY = learner.query(xtest)
print predY

'''