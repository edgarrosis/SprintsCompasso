def soma_numeros(string_numeros):
    numeros_inteiros = [int(n) for n in string_numeros.split(',')]
    
    return sum(numeros_inteiros)

string_numeros = "1,3,4,6,10,76"

resultado = soma_numeros(string_numeros)

print(resultado)
