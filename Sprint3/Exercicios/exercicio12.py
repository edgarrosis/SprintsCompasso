def my_map(list, f):
    nova_lista = []
    for n in list:
        nova_lista.append(f(n))
    
    return nova_lista

def potencia(n):
    return n ** 2

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(my_map(lista, potencia))