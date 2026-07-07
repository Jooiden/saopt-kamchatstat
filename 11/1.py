from datetime import datetime
a = []
for i in range(3):
    a.append(int(input()))
b = datetime(a[0],a[1],a[2])
for i in range(3):
    a.append(int(input()))
c = datetime(a[3],a[4],a[5])
if (b > c):
    print('Двтв ',b,' более давняя')
elif(c > b):
    print('Двтв ',c,' более давняя')
else:
    print('Даты одинаковые')