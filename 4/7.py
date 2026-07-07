from datetime import datetime,timedelta
a = datetime.today()
b = a + timedelta(weeks = 3, days = 5)
print(f"{b.day}.{b.month}.{b.year}")
