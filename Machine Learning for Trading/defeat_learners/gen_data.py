""" 			  		 			 	 	 		 		 	  		   	  			  	
template for generating data to fool learners (c) 2016 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
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
import math

 			  		 			 	 	 		 		 	  		   	  			  	
# this function should return a dataset (X and Y) that will work 			  		 			 	 	 		 		 	  		   	  			  	
# better for linear regression than decision trees 			  		 			 	 	 		 		 	  		   	  			  	
def best4LinReg(seed=6):

    np.random.seed(seed)
    X = np.random.rand(10,10)
    Y = (X[:,0])*10 + (X[:,1])*9 + X[:,2]*8 + X[:,3]*7 + X[:,4]*6 + X[:,5]*5 + X[:,6]*4 + X[:,7]*3 + X[:,8]*2 + X[:,9]

    return X, Y 			  		 			 	 	 		 		 	  		   	  			  	

def best4DT(seed=6):
    np.random.seed(seed) 			  		 			 	 	 		 		 	  		   	  			  	
    X = np.random.rand(10, 10)
    Y = 2**X[:,0]

    return X, np.array(Y)

def author(): 			  		 			 	 	 		 		 	  		   	  			  	
    return 'nmao7' # Change this to your user ID
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "they call me Tim."

'''
X1, Y1 = best4LinReg(seed = 5)
print X1.shape
print Y1.shape
print X1
print Y1
X2, Y2 = best4DT(seed = 6)
print X2.shape
print Y2.shape
print X2
print Y2
'''

