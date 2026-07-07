a = []
for i in range(10):
    print("Введите " , i + 1," ", end='')
    a.append(int(input()))
print(a)
print(sum(a))
