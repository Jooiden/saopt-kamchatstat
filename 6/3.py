import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(111,projection = "3d")
x = np.arange(-5,5,0.25)
y = np.array(x)
x,y = np.meshgrid(x,y)
z = x ** 2 + y ** 2
a = ax.plot_surface(x,y,z,cmap = "GnBu_r")
plt.colorbar(a)
plt.title("x^2+y^2")
plt.show()
