for n in range(0, 101):
    valor = 0
    for i in range(1, int(n/2+1)):
        if n%i == 0:
            valor += 1
        if valor > 1:
            break
    if 0 < valor < 2:
        print(n)        