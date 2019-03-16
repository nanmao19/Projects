import numpy as np
import pandas as pd
import LinRegLearner as ll
from sklearn.linear_model import LinearRegression
lm = LinearRegression()

data = pd.read_csv("data/Istanbul.csv")
#print data.head()

dataX = data.iloc[:, 1:-1]
#print dataX.head(2)

dataY = data.iloc[:, -1]
#print dataY.head(3)

lm.fit(dataX, dataY)

class LinRegLearner(object): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def __init__(self, verbose=False):
        pass  # move along, these aren't the drones you're looking for


    def author(self):
        id = 'nmao7'
        return id  # replace tb34 with your Georgia Tech username

 			  		 			     			  	   		   	  			  	
    def addEvidence(self,dataX,dataY): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Add training data to learner 			  		 			     			  	   		   	  			  	
        @param dataX: X values of data to add 			  		 			     			  	   		   	  			  	
        @param dataY: the Y training values 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        # slap on 1s column so linear regression finds a constant term 			  		 			     			  	   		   	  			  	
        #newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
        #newdataX[:,0:dataX.shape[1]]=dataX

        lm.fit(dataX, dataY)
        # build and save the model 			  		 			     			  	   		   	  			  	
        #self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)
 			  		 			     			  	   		   	  			  	
    def query(self,data_test):
        """ 			  		 			     			  	   		   	  			  	
        @summary: Estimate a set of test points given the model we built. 			  		 			     			  	   		   	  			  	
        @param points: should be a numpy array with each row corresponding to a specific query. 			  		 			     			  	   		   	  			  	
        @returns the estimated values according to the saved model. 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        #return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]
        pred = lm.predict(data_test)
        return pred

learner = ll.LinRegLearner(verbose = False) # constructor
learner.addEvidence(dataX, dataY) # training step

Xtest = dataX.sample(frac=0.6)
pred = lm.predict(Xtest)
print pred.shape
 # query

#print learner.author()

if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    print "the secret clue is 'zzyzx'" 			  		 			     			  	   		   	  			  	
