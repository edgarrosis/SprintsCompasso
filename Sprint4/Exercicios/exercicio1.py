file_path = 'number.txt'

with open(file_path, 'r') as file:
    numeros = list(map(int, file.readlines()))

pares = list(filter(lambda x: x % 2 == 0, numeros))

pares_ordenados = sorted(pares, reverse=True)

top_5_pares = list(map(lambda x: x, pares_ordenados[:5]))

soma_top_5 = sum(top_5_pares)

print(top_5_pares)
print(soma_top_5)
