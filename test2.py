from cmd_parser import *
import time
a = np.zeros([10,10,3])
b = np.zeros([10,10,3])
for i in range(5):
    for j in range(10):
        b[i][j] = (255,255,255)
c = np.zeros([10,10,3])
d = np.zeros([10,10,3])
s = time.clock()
c = a + b
e = time.clock()
print(e-s)
s = time.clock()
for i in range(5):
    for j in range(10):
        d[i][j] = a[i][j]+b[i][j]
e = time.clock()
print(e-s)