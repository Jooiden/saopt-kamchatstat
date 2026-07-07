def a(b,c):
    d = 2 * 3.14 * b * c
    e = (2 * (3.14 * b ** 2)) + d
    return d,e
b = float(input())
c = float(input())
e,f = a(b,c)
print(e,f)