def a1(a, b, c):
    if a > b:
        a, b = b, a
    if b > c:
        b, c = c, b
    if a > b:
        a, b = b, a
    return a, b, c
b = float(input())
c = float(input())
d = float(input())
e,f,g = a1(b,c,d)
print(e,f,g)
