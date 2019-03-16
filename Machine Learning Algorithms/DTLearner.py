import numpy as np
import pandas as pd
import DTLearner as dt


class DTLearner(object):

    def __init__(self, leaf_size, verbose):
        print self.author()
        self.leaf_size = leaf_size
        self.verbose = verbose
        #pass  # move along, these aren't the drones you're looking for

    def author(self):
        id = 'nmao7'
        return id  # replace tb34 with your Georgia Tech username

    def get_splits(self, data):
    
        potential_coef = []
        _, n_columns = data.shape
        for column_index in range(n_columns - 1):  # excluding the last column which is the label
            temp_x = data[:,column_index]
            temp_y = data[:, -1]
            temp_coef = np.corrcoef(temp_x, temp_y)
            coef = temp_coef[0,1]
            potential_coef.append(coef)

        split_column = potential_coef.index(max(potential_coef))

        col_data = data[:,split_column]
        splitVal = np.median(col_data)
        Lout = data[col_data< splitVal, :]
        Rout = data[col_data >= splitVal, :]
        print Lout
        return split_column, splitVal, Lout, Rout

    def addEvidence(self, dataX, dataY):


        #print dataY.head()

        if dataX.shape[0] <= self.leaf_size:  # less than leaf_size row
            value1 = ['leaf', dataY.mean(axis=0), float('NaN'), float('NaN')]
            return value1

        elif len(np.unique(dataY.values)) == 1:
            value2 = ['leaf', dataY.mean(axis=0), float('NaN'), float('NaN')]
            return value2

        else:
            dataWhole = pd.concat([dataX, dataY], axis = 1)
            data = dataWhole.values
            factor, split_val, left, right = self.get_splits(data)

            leftdata = pd.DataFrame(left)
            lefttree = self.addEvidence(leftdata.iloc[:, 0:-1], leftdata.iloc[:, -1])

            rightdata = pd.DataFrame(right)
            righttree = self.addEvidence(rightdata.iloc[:, 0:-1], rightdata.iloc[:, -1])

            root = [factor, split_val, 1, len([lefttree]) + 1]
            #print "root node: ", root
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

#data = pd.read_csv("data/Istanbul.csv")
data = pd.read_csv("data/testdata.csv")

Xtrain = data.iloc[:, 1:-1]
Ytrain = data.iloc[:, -1]

learner = dt.DTLearner(leaf_size=1, verbose=False) # constructor
temp = learner.addEvidence(Xtrain, Ytrain) # training step
print temp
#df = pd.DataFrame(temp, columns=['Factor', 'SplitVal', 'Left', 'Right'])
#print df

Xtest = data.sample(1, axis=0)
Xtest = Xtest.iloc[:, 1:]
#print Xtest
print "label: ", Xtest.iloc[0, -1]
y = learner.query(Xtest)

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
