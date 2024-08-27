def dividir_lista_em_tres(lista):
    tam = len(lista) // 3
     
    parte1 = lista[:tam]
    parte2 = lista[tam:2*tam]
    parte3 = lista[2*tam:]
    
    return parte1, parte2, parte3

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
parte1, parte2, parte3 = dividir_lista_em_tres(lista)

print(parte1, parte2, parte3)
