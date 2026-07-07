a = []
b = int(input())
c = 0
f = 0
for i in range(b):
    a.append(float(input()))
for i in range(b):
    if(a[i] > 0):
        c = c + a[i]
        f = f + 1
d = len(a)
e = c / f
print(e)