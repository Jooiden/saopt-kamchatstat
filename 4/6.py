from datetime import datetime
a = datetime.today()
b = datetime(2024,3,1)
c = (a - b).days
print(c)