a = []
def b(a,c = 0):
    if(c >= len(a)):
        return 0
    if(a[c] % 2 != 0):
        return a[c] + b(a,c + 1)
    return b(a,c + 1)
n = int(input())
for i in range(n):
    a.append(float(input()))
print(b(a))
