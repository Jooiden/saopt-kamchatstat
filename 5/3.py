import matplotlib.pyplot as plt
import numpy as np
labels = ['Nokia', 'Samsung', 'Apple', 'Lumia']
sizes = [10, 30, 45, 15]
colors = ['yellow', 'green', 'red', 'blue']
explode = (0.1, 0, 0, 0)  #
plt.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%', startangle=180)
plt.title("A pie chart")
plt.axis('equal')  
plt.show()
