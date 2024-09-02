import random

def mergeSort(arr):
    tamanho = 1
    n = len(arr)
    resultado = [0] * n

    while tamanho < n:
        for inicio in range(0, n, tamanho * 2):
            meio = min(inicio + tamanho, n)
            fim = min(inicio + tamanho * 2, n)
            merge(arr, resultado, inicio, meio, fim)

        # Troca arr e resultado para evitar cópias
        arr, resultado = resultado, arr

        tamanho *= 2

    return arr

def merge(arr, resultado, inicio, meio, fim):
    i, j = inicio, meio
    for k in range(inicio, fim):
        if i < meio and (j >= fim or arr[i] <= arr[j]):
            resultado[k] = arr[i]
            i += 1
        else:
            resultado[k] = arr[j]
            j += 1

random_list = random.sample(range(500), 50)


tam = len(random_list)
media = sum(random_list)/tam

valor_maximo = max(random_list)

valor_minimo = min(random_list)

ordenado = mergeSort(random_list)
if tam % 2 == 0:
    mediana = (ordenado[tam//2 -1] + ordenado[tam//2]) / 2
else:
    mediana = ordenado[tam//2]

print(f"Media: {media}, Mediana: {mediana}, Mínimo: {valor_minimo}, Máximo: {valor_maximo}")