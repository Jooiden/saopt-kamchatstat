c = []
def a(b):
    if((b == 0) or (b == 1)):
        return b
    else:
        return a(b - 1) + a(b - 2)
b = int(input())
for i in range(b + 1):
    c.append(a(i))
for i in range(b + 1):
    print(c[i])