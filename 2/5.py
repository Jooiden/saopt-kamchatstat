def a ():
    c = 1
    while True:
        d = float(input())
        if(d == 0):
            print(c)
            break
        else:
            c = c * d
a()