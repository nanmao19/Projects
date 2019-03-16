import numpy as np
import pandas as pd
import RTLearner as rt

class RTLearner(object):

    def __init__(self, leaf_size, verbose):
        print self.author()
        self.leaf_size = leaf_size
        self.verbose = verbose
        #pass  # move along, these aren't the drones you're looking for

    def author(self):
        id = 'nmao7'
        return id  # replace tb34 with your Georgia Tech username

    def get_splits(self, data):

        df = pd.DataFrame(data)
        #print df.head()
        dataX = df.iloc[:, 1:-1]
        dataY = df.iloc[:, -1]

        factor = dataX.sample(1, axis=1)
        #print factor.head()

        # Get selected attribute's name
        att_name = list(factor)
        n = att_name[0]
        print n

        # return the index of selected attribute
        split_column = dataX.columns.get_loc(n)
        print split_column

        # Calculate split value of returned attribute
        temp = factor.sample(2, axis=0)
        #print temp.iloc[:, 0]
        split_val = temp.iloc[:, 0].mean()
        print "split value: ", split_val

        Lout = df[df.iloc[:, split_column] < split_val]
        Rout = df[df.iloc[:, split_column] >= split_val]
        return split_column, split_val, Lout, Rout

    def addEvidence(self, dataX, dataY):

        if dataX.shape[0] <= self.leaf_size:  # less than leaf_size row
            value1 = ['leaf', dataY.mean(axis=0), float('NaN'), float('NaN')]
            return value1

        elif len(np.unique(dataY.values)) == 1:
            value2 = ['leaf', dataY.mean(axis=0), float('NaN'), float('NaN')]
            return value2

        else:
            dataWhole = pd.concat([dataX, dataY], axis=1)
            data = dataWhole.values
            factor, split_val, left, right = self.get_splits(data)

            leftdata = pd.DataFrame(left)
            lefttree = self.addEvidence(leftdata.iloc[:, 0:-1], leftdata.iloc[:, -1])

            rightdata = pd.DataFrame(right)
            righttree = self.addEvidence(rightdata.iloc[:, 0:-1], rightdata.iloc[:, -1])

            root = [factor, split_val, 1, len([lefttree]) + 1]
            # print "root node: ", root
            return (np.vstack((root, lefttree, righttree)))

    def query(self, testX):
        i = 0
        factor = df[df.columns[0]][0]
        # print "factor: ", factor
        # n = int(float(factor))

        while i in range(0, len(df)):

            # print "i= ", i
            if factor == "leaf":
                y = df[df.columns[1]][i]
                # print "leaf: ", y
                break

            else:
                splitV = df[df.columns[1]][i]
                # print "splitV: ", splitV
                # print testX.iloc[0, 0]

                if testX.iloc[0, 0] < int(float(splitV)):
                    goleft = df.iloc[i, 2]
                    # print "go to line: ", int(float(goleft))
                    i = i + int(float(goleft))
                    factor = df[df.columns[0]][i]

                else:
                    goright = df.iloc[i, 3]
                    # print "go to line: ", int(float(goright))
                    i = i + int(float(goright))
                    factor = df[df.columns[0]][i]

        print "prediction: ", y
        return y
data = pd.read_csv("data/Istanbul.csv")


Xtrain = data.iloc[:, 0:-1]
Ytrain = data.iloc[:, -1]

learner = rt.RTLearner(leaf_size = 15, verbose = False) # constructor
temp =  learner.addEvidence(Xtrain, Ytrain) # training step
print temp
df = pd.DataFrame(temp, columns=['Factor', 'SplitVal', 'Left', 'Right'])
Xtest = data.sample(1, axis=0)
Xtest = Xtest.iloc[:, 1:]
#print Xtest
print "label: ", Xtest.iloc[0, -1]
y = learner.query(Xtest)


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"


