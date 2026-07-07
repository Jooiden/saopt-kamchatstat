import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
print("Введённые значения не должны быть равны 0")
a = float(input())
b = float(input())
fig = plt.figure()
ax = fig.add_subplot(111,projection = "3d")
x = np.arange(-10,10,0.25)
y = np.array(x)
x,y = np.meshgrid(x,y)
z = x ** 2 / a - y ** 2 / b
ax.plot_surface(x,y,z,color = "red")
plt.title("x^2/a-y^2/b")
plt.show()
