# Sprint 08

# 1. Introdução

Essa sprint contou com a pratica de todos os conhecimentos acumulados ao longo do programa de bolsas, focando no uso das ferramentas AWS Glue, AWS Athena e PySpark para análise e formatação de dados em grande escala dos arquivos `.csv` e os filmes filtrados da API `TMDB`, com o objetivo final sendo a criação da camada Trusted dos dados do data lake.

# 2. Resolução do Desafio
Utilizando os dados armazenados na camada RAW do bucket S3, o desafio consistiu na criação da camada Trusted para os dados que serão usados nas proximas sprints.

A resolução da Etapa 3 do desafio esta documentada em: [README.md](/Sprint8/Desafio/README.md).

# 3. Exercicio
Essa sprint contou com 3 exercicios, dois deles abordando usos e funcionalidades do PySpark e Apache Spark, e o ultimo exercicio demonstrando usos da API `TMDB`.

## 3.1 Spark, Geração de Dados 
- O exercicio consistiu de 3 etapas para processamento de dados usando Apache Spark, foram geradas entao 3 scripts e 2 arquivos como resposta.
- Evidencias: 
    - [etapa1.py](/Sprint8/Exercicios/SparkGeracaoDados/etapa1.py)
    - [etapa2.py](/Sprint8/Exercicios/SparkGeracaoDados/etapa2.py) e sua saida [lista_animais.csv](/Sprint8/Exercicios/SparkGeracaoDados/lista_animais.csv)
    - [etapa3.py](/Sprint8/Exercicios/SparkGeracaoDados/etapa1.py) e e sua saida [nomes_aleatorios](/Sprint8/Exercicios/SparkGeracaoDados/nomes_aleatorios.txt)

## 3.2 Apache Spark
- Esse e exercicio consistiu na utilização do arquivo `nomes_aleatorios` do exercicio anterior, e aplicar os tratamentos de dados soicitados a cada etapa.
- Todas as etapas desenvolvidas estão exibidas em [exercicio.ipnyb](/Sprint8/Exercicios/ApacheSpark/exercicio.ipynb)
- Evidencias: 
    - [Etapa1](/Sprint8/Evidencias/Exercicio/etapa1_exercicio_apache.png).
    - [Etapa2](/Sprint8/Evidencias/Exercicio/etapa2_exercicio_apache.png).
    - [Etapa3](/Sprint8/Evidencias/Exercicio/etapa3_exercicio_apache.png).
    - [Etapa4](/Sprint8/Evidencias/Exercicio/etapa4_exercicio_apache.png).
    - [Etapa5](/Sprint8/Evidencias/Exercicio/etapa5_exercicio_apache.png).
    - [Etapa6](/Sprint8/Evidencias/Exercicio/etapa6_exercicio_apache.png).
    - [Etapa7](/Sprint8/Evidencias/Exercicio/etapa7_exercicio_apache.png).
    - [Etapa8](/Sprint8/Evidencias/Exercicio/etapa8_exercicio_apache.png).
    - [Etapa9](/Sprint8/Evidencias/Exercicio/etapa9_exercicio_apache.png).
    - [Etapa10](/Sprint8/Evidencias/Exercicio/etapa10_exercicio_apache.png).

## 3.3 TMDB
- Este exercicio baseava-se em fazer uso da API `TMDB`, necessitando apenas fazer uma busca simples.
- Evidencias:
    - [exercicio_tmdb.py](/Sprint8/Exercicios/TMDB/exercicio_tmdb.py)
    - ![exercicio_tmdb_resultado](/Sprint8/Evidencias/Exercicio/exercicio_tmdb.png)

# 4. Resultado Final Desafio
Os scripts Glue e os Crawlers criados para gerar as tabelas usando os dados da camada Trusted do bucket funcionaram como esperado, apesar dos nomes da tabelas nao terem sido alterados, possuindo nomes aleatorios.

# 5. Certificados
- [Data & Analytics - PB - AWS - Novo - 8/10](/Sprint8/Certificados/sprint8-certificado.jpg)