# Leitura e tratamento do arquivo CSV
with open("C:/Users/edgar/Desktop/Compasso/Sprint3/Exercicios/ETL/actors.csv", "r") as arquivo:
    dados = arquivo.readlines()

# Remover a linha de cabeçalho
cabecalho = dados[0]
dados = dados[1:]

# Processamento das linhas, considerando as aspas para lidar com campos com vírgulas
def processa_linha(linha):
    import csv
    from io import StringIO
    
    f = StringIO(linha)
    reader = csv.reader(f, delimiter=',')
    return next(reader)

# Transformar dados em uma lista de dicionários para facilitar as operações
lista_atores = []
for linha in dados:
    linha_processada = processa_linha(linha)
    ator = {
        "Actor": linha_processada[0],
        "Total Gross": float(linha_processada[1].strip()),
        "Number of Movies": int(linha_processada[2].strip()),
        "Average per Movie": float(linha_processada[3].strip()),
        "#1 Movie": linha_processada[4].strip(),
        "Gross": float(linha_processada[5].strip())
    }
    lista_atores.append(ator)

#----------------------------------------------- ETAPA 1 ------------------------------------------------
# Encontrar o ator com o maior número de filmes
ator_mais_filmes = max(lista_atores, key=lambda x: x['Number of Movies'])

with open("C:/Users/edgar/Desktop/Compasso/Sprint3/Exercicios/ETL/etapa_1.txt", "w") as f:
    f.write(f"O ator/atriz com maior numero de filmes e {ator_mais_filmes['Actor']} com {ator_mais_filmes['Number of Movies']} filmes.")

#----------------------------------------------- ETAPA 2 ------------------------------------------------
# Calcular a média da receita bruta dos filmes principais
media_receita_bruta = sum(ator['Gross'] for ator in lista_atores) / len(lista_atores)

with open("C:/Users/edgar/Desktop/Compasso/Sprint3/Exercicios/ETL/etapa_2.txt", "w") as f:
    f.write(f"A media de receita de bilheteria bruta dos principais filmes e {media_receita_bruta:.2f} milhoes de dolares.")

#----------------------------------------------- ETAPA 3 ------------------------------------------------
# Encontrar o ator com a maior média de receita bruta por filme
ator_maior_media_receita = max(lista_atores, key=lambda x: x['Average per Movie'])

with open("C:/Users/edgar/Desktop/Compasso/Sprint3/Exercicios/ETL/etapa_3.txt", "w") as f:
    f.write(f"O ator/atriz com a maior media de receita bruta por filme e {ator_maior_media_receita['Actor']} com {ator_maior_media_receita['Average per Movie']:.2f} milhoes de dolares por filme.")

#----------------------------------------------- ETAPA 4 ------------------------------------------------
# Contagem de aparições dos filmes na coluna #1 Movie
from collections import Counter

contagem_filmes = Counter(ator['#1 Movie'] for ator in lista_atores)

with open("C:/Users/edgar/Desktop/Compasso/Sprint3/Exercicios/ETL/etapa_4.txt", "w") as f:
    for filme, contagem in contagem_filmes.most_common():
        f.write(f"O filme {filme} aparece {contagem} vez(es) no dataset.\n")

#----------------------------------------------- ETAPA 5 ------------------------------------------------
# Ordenar atores pela receita total bruta em ordem decrescente
atores_ordenados = sorted(lista_atores, key=lambda x: x['Total Gross'], reverse=True)

with open("C:/Users/edgar/Desktop/Compasso/Sprint3/Exercicios/ETL/etapa_5.txt", "w") as f:
    for ator in atores_ordenados:
        f.write(f"{ator['Actor']} - {ator['Total Gross']:.2f} milhoes de dolares\n")
