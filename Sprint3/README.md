# Sprint 03

# 1. Introdução
Esta sprint utlizou a prática com comandos básicos e avançados de python, destacando a manipulação de arquivos e dados, e também a orientação objeto do mesmo, através de secções do curso [Python 3 - Curso Completo do Básico ao Avançado](https://compassuol.udemy.com/course/curso-python-3-completo/learn/lecture/16099797?course_portion_id=390160&learning_path_id=5948466#overview). Tambem contou com aprendizado sobre vantagens dos serviços de nuvem da AWS, com o curso [AWS Partner: Economias na nuvem AWS](https://explore.skillbuilder.aws/learn/course/13660/AWS%2520Partner%253A%2520Sales%2520Accreditation%2520%28Business%29%2520%28Portuguese%29). 

# 2. Resolução do Desafio
A resolução do desafio final da sprint foi iniciada no dia 28/08/2024 até o dia 30/08/2024 com o desenvolvimento do `desafio.ipynb` utilizando o arquivo `googleplaystore.csv` fornecido.

Seu desenvolvimento e normalização estão detalhados em [README](/Sprint3/Desafio/README.md)

# 3. Exercicios
Os exercicios consistiam basicamente na realização de comandos python, desde as mais simples à mais complexas, em um deles foi utlizado dados fornecidos pelo arquivo [actors.csv](/Sprint3/Exercicios/ETL/actors.csv). 

Os codigos dos exercicios funcionam conforme o esperado, e foi comprovado nas evidencias dos mesmos.

|Exercicio | Evidencia|
| :--- | ---:|
| [Exercicío 1](/Sprint3/Exercicios/exercicio1.py) |  [Evidencia 1](/Sprint3/Evidencias/exercicio/exercicio1.png) |
| [Exercicío 2](/Sprint3/Exercicios/exercicio2.py) | [Evidencia 2](/Sprint3/Evidencias/exercicio/exercicio2.png) |
| [Exercicío 3](/Sprint3/Exercicios/exercicio3.py) |  [Evidencia 3](/Sprint3/Evidencias/exercicio/exercicio3.png) |
| [Exercicío 4](/Sprint3/Exercicios/exercicio4.py) | [Evidencia 4](/Sprint3/Evidencias/exercicio/exercicio4.png) |
| [Exercicío 5](/Sprint3/Exercicios/exercicio5.py) |  [Evidencia 5](/Sprint3/Evidencias/exercicio/exercicio5.png) |
| [Exercicío 6](/Sprint3/Exercicios/exercicio6.py) |  [Evidencia 6](/Sprint3/Evidencias/exercicio/exercicio6.png) |
| [Exercicío 7](/Sprint3/Exercicios/exercicio7.py) | [Evidencia 7](/Sprint3/Evidencias/exercicio/exercicio7.png) |
| [Exercicío 8](/Sprint3/Exercicios/exercicio8.py) | [Evidencia 8](/Sprint3/Evidencias/exercicio/exercicio8.png) |
| [Exercicío 9](/Sprint3/Exercicios/exercicio9.py) | [Evidencia 9](/Sprint3/Evidencias/exercicio/exercicio9.png)
| [Exercicío 10](/Sprint3/Exercicios/exercicio10.py) | [Evidencia 10](/Sprint3/Evidencias/exercicio/exercicio10.png) |
| [Exercicío 11](/Sprint3/Exercicios/exercicio11.py) | [Evidencia 11](/Sprint3/Evidencias/exercicio/exercicio11.png) |
| [Exercicío 12](/Sprint3/Exercicios/exercicio12.py) | [Evidencia 12](/Sprint3/Evidencias/exercicio/exercicio12.png) |
| [Exercicío 13](/Sprint3/Exercicios/exercicio13.py) | [Evidencia 13](/Sprint3/Evidencias/exercicio/exercicio13.png) |
| [Exercicío 14](/Sprint3/Exercicios/exercicio14.py) | [Evidencia 14](/Sprint3/Evidencias/exercicio/exercicio14.png) |
| [Exercicío 15](/Sprint3/Exercicios/exercicio15.py) | [Evidencia 15](/Sprint3/Evidencias/exercicio/exercicio15.png) |
| [Exercicío 16](/Sprint3/Exercicios/exercicio16.py) | [Evidencia 16](/Sprint3/Evidencias/exercicio/exercicio16.png) |
| [Exercicío 17](/Sprint3/Exercicios/exercicio17.py) | [Evidencia 17](/Sprint3/Evidencias/exercicio/exercicio17.png) |
| [Exercicío 18](/Sprint3/Exercicios/exercicio18.py) | [Evidencia 18](/Sprint3/Evidencias/exercicio/exercicio18.png) |
| [Exercicío 19](/Sprint3/Exercicios/exercicio19.py) | [Evidencia 19](/Sprint3/Evidencias/exercicio/exercicio19.png) |
| [Exercicío 20](/Sprint3/Exercicios/exercicio20.py) | [Evidencia 20](/Sprint3/Evidencias/exercicio/exercicio20.png) |
| [Exercicío 21](/Sprint3/Exercicios/exercicio21.py) | [Evidencia 21](/Sprint3/Evidencias/exercicio/exercicio21.png) |
| [Exercicío 22](/Sprint3/Exercicios/exercicio22.py) | [Evidencia 22](/Sprint3/Evidencias/exercicio/exercicio22.png) |
| [Exercicío 23](/Sprint3/Exercicios/exercicio23.py) | [Evidencia 23](/Sprint3/Evidencias/exercicio/exercicio23.png) |
| [Exercicío 24](/Sprint3/Exercicios/exercicio24.py) | [Evidencia 24](/Sprint3/Evidencias/exercicio/exercicio24.png) |
| [Exercicío 25](/Sprint3/Exercicios/exercicio25.py) | [Evidencia 25](/Sprint3/Evidencias/exercicio/exercicio25.png) |


### Exercicio ETL
Este exercicio utilizou o arquivo [actors.csv](/Sprint3/Exercicios/ETL/actors.csv) para que fosse criado um cádigo que respondesse aos questionamento e extraisse os dados necessários propostos. Devido a problemas com a importação do arquivo no código, foi utilizado o caminho relativo completo para a abertura do mesmo

Sua funcionalidade e etapas estão comentados no próprio código, segue o código resolução em questão e os arquivos gerados como resposta: 
```py
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

```
- [exercicioETL.py](/Sprint3/Exercicios/ETL/exericioETL.py)
- [Etapa1](/Sprint3/Exercicios/ETL/etapa_1.txt), [Etapa2](/Sprint3/Exercicios/ETL/etapa_2.txt), [Etapa3](/Sprint3/Exercicios/ETL/etapa_3.txt), [Etapa4](/Sprint4/Exercicios/ETL/etapa_4.txt), [Etapa5](/Sprint3/Exercicios/ETL/etapa_5.txt)



# 4. Resultado Final Desafio
Os dados do arquivo `googleplaystore.csv` foram acessados e trabalhos com sucesso, sendo a principal dificuldade do progresso do desafio com os comandos especificos de ambas bibliotecas utilizado e suas possibilidades de usos, que ao longo do tempo foram exploradas e estudadas, obtendo assim os resultados demonstrados.

# 5. Certificados
- [Aspectos econômicos da nuvem | AWS Partner: Cloud Economics](/Sprint3/Certificados/AWS_Course.pdf)
- [Data & Analytics - PB - AWS - Novo 3/10](/Sprint3/Certificados/Data_analitics.jpg)