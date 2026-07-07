def a(b):
    if(b == 1):
        return 1
    return b * a(b - 1)
b = float(input())
print(a(b))