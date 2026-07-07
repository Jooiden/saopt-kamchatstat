from datetime import datetime
a = datetime(2024,3,10)
b = datetime(2024,3,22,hour = 0,minute = 0, second = 0)
c = (b - a).days - 1
print(f"{a.day}.{a.month}.{a.year}")
print(b)
print(c)
