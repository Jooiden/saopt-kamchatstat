def a1(a,b,c):
    return b ** 2 - (4 * a * c)
a = float(input())
b = float(input())
c = float(input())
d = a1(a,b,c)
print(d)
if(d < 0):
    print("Нет корней. ")
else:
    if(d == 0):
        e = (-1 * b) / (2 * a)
        print(e)
    else:
        if(d > 0):
            e = (-1 * b + d ** 0.5) / (2 * a)
            f = (-1 * b - d ** 0.5) / (2 * a)
            print(e,f)
