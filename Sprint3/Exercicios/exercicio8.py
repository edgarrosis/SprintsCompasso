a = ['maça', 'arara', 'audio', 'radio', 'radar', 'moto']

for palavra in a:
    tam = len(palavra)
    palindromo = True
    
    for i in range(tam // 2):
        if palavra[i] != palavra[tam - i - 1]:
            palindromo = False
            break
    
    if palindromo:
        print(f'A palavra: {palavra} é um palíndromo')
    else:
        print(f'A palavra: {palavra} não é um palíndromo')