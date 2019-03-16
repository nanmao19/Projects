import numpy as np
import pandas as pd
import math

df = pd.DataFrame(columns=['x1', 'x2', 'y'])

d1 = [1,6,7]
df = df.append(pd.Series(d1, index=df.columns), ignore_index=True)
d2 = [2,4,8]
df = df.append(pd.Series(d2, index=df.columns), ignore_index=True)
d3 = [3,7,16]
df = df.append(pd.Series(d3, index=df.columns), ignore_index=True)
d4 = [6,8,44]
df = df.append(pd.Series(d4, index=df.columns), ignore_index=True)
d5 = [7,1,50]
df = df.append(pd.Series(d5, index=df.columns), ignore_index=True)
d6 = [8,4,68]
df = df.append(pd.Series(d6, index=df.columns), ignore_index=True)
print df

q = [4,2]

print abs(-3)

def Edistance(df, q):
    distance = []
    for i in range(0, df.shape[0]):
        d = math.sqrt((df.iloc[i, 0] - q[0])**2 + (df.iloc[i,1] - q[1])**2)
        distance.append(d)
    df.loc[:,'distance'] = pd.Series(distance, index=df.index)
    return df

def Mdistance(df,q):
    distance = []
    for i in range(0, df.shape[0]):
        d = abs(df.iloc[i, 0] - q[0]) + abs(df.iloc[i, 1] - q[1])
        distance.append(d)
    df.loc[:, 'distance'] = pd.Series(distance, index=df.index)
    return df

def Compdistance(df,q):
    distance = []
    for i in range(0, df.shape[0]):
        d = (df.iloc[i, 0] - q[0])**2 + abs(df.iloc[i, 1] - q[1])
        distance.append(d)
    df.loc[:, 'distance'] = pd.Series(distance, index=df.index)
    return df

#newdf = Edistance(df, q)
#newdf = Mdistance(df, q)
newdf = Compdistance(df, q)

sorted_df =  newdf.sort_values(by = ['distance'])
print sorted_df

k = 1
temp = sorted_df.iloc[k-1, -1]
#print temp

df_temp = sorted_df.loc[sorted_df['distance'] <= temp]
#print df_temp
print df_temp['y'].mean(axis=0)