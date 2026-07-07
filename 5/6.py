import matplotlib.pyplot as plt
import numpy as np
x = np.arange(-10, 10, 0.1)
b = lambda x: x * x
y = b(x)
plt.figure(figsize=(20, 100))
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('График функции Y = x ^ 2')
plt.show()
