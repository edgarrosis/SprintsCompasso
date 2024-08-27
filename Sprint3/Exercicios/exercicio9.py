primeirosNomes = ['Joao', 'Douglas', 'Lucas', 'José']
sobreNomes = ['Soares', 'Souza', 'Silveira', 'Pedreira']
idades = [19, 28, 25, 31]

tam = len(idades)
for index, _ in enumerate(idades):
    frase = (f"{primeirosNomes[index]} {sobreNomes[index]} está com {idades[index]} anos")

    print(f"{index} - {frase}")