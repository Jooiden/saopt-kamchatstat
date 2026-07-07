a = []
b = 0
c = 1
d = 0
for i in range(20):
    a.append(b)
    d = b + c
    b = c
    c = d
for i in range(20):
    print(a[i],' ',end = ' ')