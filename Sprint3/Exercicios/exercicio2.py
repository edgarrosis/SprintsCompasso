numeros = list(range(1, 4))

for numero in numeros:
    if numero % 2 == 0 or numero == 0:
        print(f"Par: {numero}")
    elif numero % 3 == 0 or numero == 1:
        print(f"Ímpar: {numero}")
