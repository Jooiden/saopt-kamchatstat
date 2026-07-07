import matplotlib.pyplot as plt
labels = ['Nokia', 'Samsung', 'Apple', 'Lumia']
sizes = [10, 30, 45, 15]
colors = ['yellow', 'green', 'red', 'blue']
plt.pie(sizes, labels=labels, colors=colors)
plt.title("Char")
plt.legend()
plt.show()
