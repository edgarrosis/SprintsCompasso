# Importação das bibliotecas
import random
import names

# Parâmetros para geração do dataset
random.seed(40)
qtd_nomes_unicos = 3000
qtd_nomes_aleatorios = 10000000

# Gerar os nomes aleatórios
aux = [names.get_full_name() for _ in range(qtd_nomes_unicos)]
print("Gerando {} nomes aleatórios".format(qtd_nomes_unicos))

dados = [random.choice(aux) for _ in range(qtd_nomes_aleatorios)]

# Nome do arquivo csv
csv = "nomes_aleatorios.txt"

#Gerar um arquivo de texto contendo todos os nomes, um a cada linha
with open(csv, "w") as file:
    for nome in dados:
        file.write(nome + "\n")