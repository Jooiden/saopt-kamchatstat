import matplotlib.pyplot as plt
import numpy as np
x = np.arange(-1*np.pi, np.pi, 0.1)
b = lambda x: np.sin(x)
y = b(x)
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('График функции Y = sin(x)')
plt.show()
