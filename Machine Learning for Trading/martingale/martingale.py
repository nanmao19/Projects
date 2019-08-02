"""Assess a betting strategy. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
Student Name: Nan Mao (replace with your name)
GT User ID: nmao7 (replace with your User ID)
GT ID: 903363914 (replace with your GT ID)
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
 			  		 			     			  	   		   	  			  	
def author(): 			  		 			     			  	   		   	  			  	
    return 'nmao7' # replace tb34 with your Georgia Tech username.
 			  		 			     			  	   		   	  			  	
def gtid(): 			  		 			     			  	   		   	  			  	
	return 903363914 # replace with your GT ID number
 			  		 			     			  	   		   	  			  	
def get_spin_result(win_prob): 			  		 			     			  	   		   	  			  	
	result = False 			  		 			     			  	   		   	  			  	
	if np.random.random() <= win_prob: 			  		 			     			  	   		   	  			  	
		result = True 			  		 			     			  	   		   	  			  	
	return result 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def test_code(): 			  		 			     			  	   		   	  			  	
	win_prob = 0.486 # set appropriately to the probability of a win
	np.random.seed(gtid()) # do this only once
	print get_spin_result(win_prob) # test the roulette spin
 			  		 			     			  	   		   	  			  	
	# add your code here to implement the experiments


	df1 = pd.DataFrame()

	for x in range(1, 11):  # run 10 times of simulator

		winnings = np.zeros(1) # create an empty np array with first element = 0

		while winnings[-1] < 80:

			won = False
			bet_amount = 1 # when won == True, reset bet_amount = 1

			while not won:

				won = get_spin_result(win_prob)

				# print won

				if won == True:

					winnings = np.append(winnings, winnings[-1] + bet_amount)

				else:

					winnings = np.append(winnings, winnings[-1] - bet_amount)

					bet_amount = bet_amount * 2

				# print "winnings = ", winnings, "bet amount = ", bet_amount

		# print winnings

		df_temp = pd.DataFrame({x: winnings})

		df1 = pd.concat([df1, df_temp], axis=1)

	df1.fillna(method='ffill', inplace=True)  # forward fill NaN values with 80

	# print df1

	# plot Figure 1

	ax = df1.plot(kind='line', title="Figure 1", fontsize=12, legend='lower left')
	ax.set_xlabel("bet")
	ax.set_xlim(0, 300)
	ax.set_ylabel("winnings")
	ax.set_ylim(-256, 100)
	plt.savefig('Figure1.png', bbox_inches='tight')
	# plt.show()
	plt.close()
	
	#################################################################################
	
	df2 = pd.DataFrame()

	for x in range(1, 1001):  # run 1000 times of simulator

		winnings = np.zeros(1)  # create an empty np array with first element = 0

		while winnings[-1] < 80:

			won = False
			bet_amount = 1  # when won == True, reset bet_amount = 1

			while not won:

				won = get_spin_result(win_prob)

				# print won

				if won == True:

					winnings = np.append(winnings, winnings[-1] + bet_amount)

				else:

					winnings = np.append(winnings, winnings[-1] - bet_amount)

					bet_amount = bet_amount * 2

		# print winnings

		df_temp = pd.DataFrame({x: winnings})

		df2 = pd.concat([df2, df_temp], axis=1)

	df2.fillna(method='ffill', inplace=True)  # forward fill NaN values with 80

	df2_mean = df2.mean(axis = 1)  # Calculate mean of each row (each spin)
	# print df2_mean

	df2_std = df2.std(axis = 1)  # Calculate std of each row (each spin)
	# print df2_std

	upper_band1 = df2_mean + df2_std
	lower_band1 = df2_mean - df2_std

	# plot Figure 2

	# ax = df2[['mean', 'mean+std', 'mean-std']].plot(kind='line', title="Figure 2", fontsize=12, legend='lower left')
	ax = df2_mean.plot(kind='line', title="Figure 2", fontsize=12, legend='lower left', label='mean')
	upper_band1.plot(label='upper band', ax=ax, legend='lower left', )
	lower_band1.plot(label='lower band', ax=ax, legend='lower left', )
	ax.set_xlabel("bet")
	ax.set_xlim(0, 300)
	ax.set_ylabel("winnings")
	ax.set_ylim(-256, 100)
	plt.savefig('Figure2.png', bbox_inches='tight')
	# plt.show()
	plt.close()
	
	#################################################################################

	# plot Figure 3

	df2_median = df2.median(axis = 1)

	upper_band2 = df2_median + df2_std
	lower_band2 = df2_median - df2_std

	ax = df2_median.plot(kind='line', title="Figure 3", fontsize=12, legend='lower left', label='mean')
	upper_band2.plot(label='upper band', ax=ax, legend='lower left', )
	lower_band2.plot(label='lower band', ax=ax, legend='lower left', )
	ax.set_xlabel("bet")
	ax.set_xlim(0, 300)
	ax.set_ylabel("winnings")
	ax.set_ylim(-256, 100)
	plt.savefig('Figure3.png', bbox_inches='tight')
	# plt.show()
	plt.close()

	'''
	ax = df2_std.plot(kind='line', title="std plot", fontsize=12, legend='lower left',label='std')
	ax.set_xlabel("bet")
	ax.set_ylabel("std")
	plt.show()
	plt.close()
	'''


	#################################################################################
	
	df4 = pd.DataFrame()

	for x in range(1, 1001):  # run 10 times of simulator

		winnings = np.zeros(1)  # create an empty np array with first element = 0

		while winnings[-1] < 80 and winnings[-1] > -256:

			won = False

			bet_amount = 1

			while not won:

				if bet_amount > winnings[-1] + 256:
					bet_amount = winnings[-1] + 256

				else:

					won = get_spin_result(win_prob)

					if won == True:

						winnings = np.append(winnings, winnings[-1] + bet_amount)

					else:

						winnings = np.append(winnings, winnings[-1] - bet_amount)

						bet_amount = bet_amount * 2

		df_temp = pd.DataFrame({x: winnings})

		df4 = pd.concat([df4, df_temp], axis=1)

	df4.fillna(method='ffill', inplace=True)  # forward fill NaN values with 80
	#print df4.head()
	#print df4.shape

	'''
	# Calculate probability of winnings $80 after 1000 sequential bets
	a = df4.iloc[-1, :]
	# print a
	print "expected value: ", a.mean()
	a[a < 80] = 0
	a[a >= 80] = 1
	# print a
	print "total probability of winning $80", a.sum()/len(a)
	'''



	df4_mean = df4.mean(axis=1)  # Calculate mean of each row (each spin)
	# print df4_mean

	df4_std = df4.std(axis=1)  # Calculate std of each row (each spin)
	# print df4_std

	upper_band3 = df4_mean + df4_std
	lower_band3 = df4_mean - df4_std

	'''
	ax = df4_std.plot(kind='line', title="std plot", fontsize=12, legend='lower left', label='std')
	ax.set_xlabel("bet")
	ax.set_ylabel("std")
	plt.show()
	plt.close()
	'''

	# plot Figure 4

	ax = df4_mean.plot(kind='line', title="Figure 4", fontsize=12, legend='lower left', label='mean')
	upper_band3.plot(label='upper band', ax=ax, legend='lower left', )
	lower_band3.plot(label='lower band', ax=ax, legend='lower left', )
	ax.set_xlabel("bet")
	ax.set_xlim(0, 300)
	ax.set_ylabel("winnings")
	ax.set_ylim(-256, 100)
	plt.savefig('Figure4.png', bbox_inches='tight')
	#plt.show()
	plt.close()

	# plot Figure 5

	df4_median = df4.median(axis=1)  # Calculate mean of each row (each spin)

	upper_band4 = df4_median + df4_std
	lower_band4 = df4_median - df4_std

	ax = df4_median.plot(kind='line', title="Figure 5", fontsize=12, legend='lower left', label='mean')
	upper_band4.plot(label='upper band', ax=ax, legend='lower left', )
	lower_band4.plot(label='lower band', ax=ax, legend='lower left', )
	ax.set_xlabel("bet")
	ax.set_xlim(0, 300)
	ax.set_ylabel("winnings")
	ax.set_ylim(-256, 100)
	plt.savefig('Figure5.png', bbox_inches='tight')
	#plt.show()
	plt.close()
	


if __name__ == "__main__":
    test_code() 			  		 			     			  	   		   	  			  	
