def a(b,c,d,e):
    return b.count(e.upper()) + b.count(e.lower()) + c.count(e.upper()) + c.count(e.lower()) + d.count(e.upper()) + d.count(e.lower())
b = input()
c = input()
d = input()
e = input()
print(a(b,c,d,e))