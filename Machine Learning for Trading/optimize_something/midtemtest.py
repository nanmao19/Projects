import numpy as np
import pandas as pd
import scipy.optimize as spo



from util import get_data





d = {'Portfolio_1': [0.00, 0.24, 0.32, 0.44],

     'Portfolio_2': [0.30, 0.12, 0.33, 0.25],

     'Portfolio_3': [0.13, 0.36, 0.19, 0.32],

     'Portfolio_4': [0.17, 0.16, 0.31, 0.36]}


df = pd.DataFrame(d)

print df

print df.to_string()

threshold = df.iloc[3,2]


print threshold

allocations = np.array([0.41, 0.24, 0.56, 0.31, 0.32, 0.16, 0.33])


print [np.where( allocations > threshold )]

