import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  
r = 1  
z = np.linspace(0,15,1000)
x = r * np.cos(z)  
y = r * np.sin(z)  
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, z, color='red')  
plt.title('x = cos(z) y = sin(z)')
plt.show()
