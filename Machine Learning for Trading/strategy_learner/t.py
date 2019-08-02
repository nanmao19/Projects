import numpy as np

a=np.arange(6)
print a

b=a
b.shape = 3,2
print a

b.reshape(2,3)
print a