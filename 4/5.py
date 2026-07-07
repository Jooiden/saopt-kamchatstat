from datetime import datetime
a = datetime.today()
b = datetime(2025,1,1)
c = (b - a).days
print(c)