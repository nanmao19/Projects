""" 			  		 			 	 	 		 		 	  		   	  			  	
Template for implementing QLearner  (c) 2015 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
import random
import QLearner as ql

 			  		 			 	 	 		 		 	  		   	  			  	
class QLearner(object):

    def author(self):
        return 'nmao7'  # Change this to your user ID

    def __init__(self, num_states=100, num_actions = 4, alpha = 0.2, gamma = 0.9, rar = 0.5, radr = 0.99, dyna = 0, verbose = False):

        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.verbose = verbose
        self.s = 0
        self.q = np.zeros((num_states, num_actions))
        self.r = np.zeros((num_states, num_actions))
        self.t = np.zeros((num_states, num_actions, num_states))
        self.tc = np.random.uniform(0.0001, 0.001, [num_states,num_actions,num_states])

    def querysetstate(self, s):

        # set initial state
        if random.uniform(0, 1) < self.rar:
            action = random.randint(0, self.num_actions-1) # choose the random direction
        else:
            action = self.q[s, :].argmax()
        self.s = s
        self.a = action

        return action

    def query(self, s_prime, r):

        #print self.q[s_prime, :]
        # roll the dice to decide if take a random action or not
        if random.uniform(0, 1) < self.rar:
            action = random.randint(0, self.num_actions-1) # choose the random direction
            #print "action1:", action
        else:
            action = self.q[s_prime, :].argmax()
            #print "action2:", action

        # update Q table
        self.q[self.s, self.a] = (1 - self.alpha) * self.q[self.s, self.a] + self.alpha * (r + self.gamma * self.q[s_prime, action])

        #print self.q[self.s, :]
        #print "update action:", self.a

        # Dyna-Q
        if(self.dyna > 0):
            self.dynaModel(self.s, self.a, s_prime, r)

        # update s, a and rar
        self.s = s_prime
        self.a = action
        self.rar = self.rar * self.radr

        return action

    def dynaModel(self, s, a, s_prime, r):

        # update model T
        self.tc[s, a, s_prime] = self.tc[s, a, s_prime] + 1
        #print self.tc[s, a, s_prime]
        self.t = self.tc / self.tc.sum(axis=2, keepdims=True)
        #print self.t

        # update reward model R
        self.r[s, a] = (1 - self.alpha) * self.r[s, a] + self.alpha * r

        for _ in range(self.dyna):

            # randomly set state and action
            s0 = random.randint(0, self.num_states - 1)
            a0 = random.randint(0, self.num_actions - 1)

            # infer s_prime from T model
            s_prime = self.t[s0, a0, :].argmax()

            # infer r from R model
            r0 = self.r[s0, a0]

            action = self.q[s_prime, :].argmax()

            # update Q table
            self.q[s0, a0] = (1 - self.alpha) * self.q[s0, a0] + self.alpha * (r0 + self.gamma * self.q[s_prime, action])
'''
def test_code():

    leaner = ql.QLearner(num_states=100, num_actions = 4, alpha = 0.2, gamma = 0.9, rar = 0.98, radr = 0.999, dyna = 50, verbose = False)
    s = 99
    a = leaner.querysetstate(s)
    print "initial a:", a
    s_prime = 5
    r = 0
    next_action = leaner.query(s_prime, r)
    print next_action
'''

if __name__ == "__main__":

    # test_code()
    print "Remember Q from Star Trek? Well, this isn't him"
