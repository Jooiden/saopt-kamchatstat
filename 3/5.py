def a(b):
    if(b == 1):
        return 1
    elif(b % 2 == 0):
        return b + a(b - 1)
    elif(b % 2 != 0 and b > 1):
        return 3 * a(b - 2)
print(a(25))
