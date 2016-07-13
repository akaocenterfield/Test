from matplotlib import pyplot
import pylab
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = pylab.figure()
ax = Axes3D(fig)

x1 = []
y1 = []
for i in range(100):
    x = 0
    while x <= i:
        x1.append(x)
        y1.append(i)
        x = x + 1

x2 = np.asarray(x1)
y2 = np.asarray(y1)
z = 5 * x2 - 3 * y2
ax.scatter(x2, y2, z)
pyplot.show()
