import random

# Inicializa a lista com 250 inteiros aleatórios
lista = [random.randint(0, 1000) for _ in range(250)]

# Aplica o método reverse
lista.reverse()

# Imprime o resultado
print(lista)
