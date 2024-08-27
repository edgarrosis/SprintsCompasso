def remove_duplicado(lista):
    return list(set(lista))

lista = ['abc', 'abc', 'abc', '123', 'abc', '123', '123']
resultado = remove_duplicado(lista)
print(resultado)