# 1. Introdução

Este projeto implementa a etapa 2 do desafio final e consiste em realizar a ingestão de dados de filmes e séries no formato CSV para um Data Lake na AWS, utilizando uma função AWS Lambda para o processo de carga, com suporte das bibliotecas `pandas`, `boto3`, `tmdbv3api`, e `requests`. Essa função é configurada e executada em um ambiente Docker, com o objetivo de coletar dados complementares sobre filmes, que são armazenados em um bucket S3.

O desafio teve como objetivo praticar a construção de um Data Lake, incluindo ingestão, armazenamento, e enriquecimento de dados através de uma API externa (TMDB). Nesta primeira etapa, a **Ingestão de Batch** faz o upload de arquivos CSV para o S3 e coleta informações adicionais para cada filme da API TMDB.

# 2. Estrutura do Projeto

O projeto está organizado da seguinte forma:

- [Dockerfile](/Sprint7/Desafio/Etapa2/Dockerfile): Configuração do container Docker que será utilizado para executar a função Lambda e preparar as dependências em camadas.

- [desafio.py](/Sprint7/Desafio/Etapa2/desafio.py): Código Python da função AWS Lambda, responsável por processar os arquivos CSV e coletar dados complementares de filmes via API TMDB.

- [minha-camada-pandas.zip](/Sprint7/Desafio/Etapa2/minha-camada-pandas.zip) e [camada-requests.zip](/Sprint7/Desafio/Etapa2/camada-requests.zip): Pacotes com dependências necessários para rodar a função no AWS Lambda.

## 2.1 Arquitetura do Bucket S3

Os dados são armazenados no bucket seguindo o seguinte padrão de diretórios:

```
S3://data-lake-edgar-silva/Raw/TMDB/JSON/2024/10/26/[arquivo]
```

# 3. Configuração do Projeto

### 3.1 Pré-requisitos

1. **AWS CLI**: Instalado e configurado, com permissões para acessar o bucket S3 e executar o Lambda (para testes locais).
2. **Docker**: Instalado para construir o ambiente de execução da função Lambda e camadas.
3. **API Key do TMDB**: Necessária para acessar a API. Configure-a no Lambda como variável de ambiente (`API_KEY_TMDB`).

### 3.2 Configuração das Camadas Lambda

Para incluir as bibliotecas externas (`pandas`, `boto3`, `requests`, `tmdbv3api`) em um ambiente Lambda, utilize o Docker com o seguinte `Dockerfile`:

```dockerfile
FROM amazonlinux:2023
RUN yum update -y
RUN yum install -y \
    python3-pip \
    zip
RUN yum -y clean all
```

#### 3.3 Passos para Criar as Camadas

No terminal do Docker, crie as camadas das dependências com os comandos, foram geradas em containers diferentes.

Foi utilizado 2 .zip para nao atingir o limite de 100mb por camada do AWS Lambda

```bash
mkdir -p layer_dir/python
cd layer_dir/python
pip3 install pandas -t .
cd ..
zip -r pandas-layer.zip

mkdir -p layer_dir/python
cd layer_dir/python
pip3 install boto3 tmdbv3api requests -t .
cd ..
zip -r pandas-layer.zip
```

Suba ambos os arquivos `.zip` como camadas no Lambda.

# 4. Estrutura do Código

### 4.1 Configuração Inicial e Autenticação

- A função configura o cliente S3 e recupera a chave de API do TMDB a partir das variáveis de ambiente.
- Verifica se o bucket S3 especificado (`data-lake-edgar-silva`) está acessível.

### 4.2 Leitura e Filtragem dos Dados CSV no S3

- **Carrega o arquivo CSV**: Obtém o arquivo `movies.csv` do bucket S3 (no caminho `Raw/Local/CSV/filmes/2024/10/16/movies.csv`).
- **Processa o arquivo em chunks**: Para lidar com arquivos grandes, o arquivo é lido em partes (chunks) de 1000 linhas.
- **Filtra os filmes**:
  - Remove duplicados com base na coluna `id`.
  - Ajusta valores ausentes no campo `anoLancamento`, substituindo-os por zero.
  - Filtra os filmes que pertencem aos gêneros **Crime** ou **War** e foram lançados após 1980.

### 4.3 Integração com a API do TMDB

Para cada filme filtrado:
- **Busca detalhes do filme na API do TMDB** usando o `imdb_id`:
  - A API retorna os resultados de filmes relacionados ao ID do IMDb.
  - Se houver resultados, a função captura o primeiro item da lista, que contém as principais informações do filme.
- **Obtém informações de elenco**:
  - Com o `id` do filme na TMDB, a função faz uma segunda chamada à API para obter detalhes do elenco.
  - Adiciona a lista de atores (`cast`) ao dicionário de detalhes do filme.

### 4.4 Armazenamento dos Resultados no S3

- Os filmes filtrados são ordenados pela popularidade (em ordem decrescente), e a função seleciona os **500 filmes mais populares**.
- **Salva os dados em JSON**:
  - Cada filme é armazenado como um arquivo JSON individual no S3, seguindo o caminho `Raw/TMDB/JSON/2024/10/26/filme_{index}.json`.

### 4.5 Retorno

- A função retorna um código `200` e uma mensagem de sucesso se o processamento for concluído com sucesso.
- Em caso de erro, ela retorna um código `500` e a descrição do erro.

### 4.6 Código Referenciado

```python
import json
import requests
import pandas as pd
import boto3
import os

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = 'data-lake-edgar-silva'
    api_key_tmdb = os.getenv('API_KEY_TMDB')

    try:
        s3_client.head_bucket(Bucket=bucket_name)
        
        csv_object = s3_client.get_object(Bucket=bucket_name, Key='Raw/Local/CSV/filmes/2024/10/16/movies.csv')
        chunk_size = 1000
        filtered_movies = []

        for chunk in pd.read_csv(csv_object['Body'], sep='|', chunksize=chunk_size, dtype={'id': str, 'genero': str, 'anoLancamento': str}):
            chunk = chunk.drop_duplicates(subset=['id'])
            chunk['anoLancamento'] = chunk['anoLancamento'].replace('\\N', '0').astype(int)
            imdb_filtered = chunk[(chunk.genero.str.contains("Crime|War", regex=True)) & (chunk.anoLancamento > 1980)]

            for _, movie in imdb_filtered.iterrows():
                imdb_id = movie['id']
                url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key_tmdb}&language=pt-BR&external_source=imdb_id"
                response = requests.get(url)
                data = response.json()

                if data.get('movie_results'):
                    movie_details = data['movie_results'][0]
                    movie_id = movie_details['id']
                    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key_tmdb}&language=pt-BR"
                    response = requests.get(url)
                    credits_data = response.json()
                    movie_details['cast'] = credits_data.get('cast', [])
                    filtered_movies.append(movie_details)

        filtered_movies = sorted(filtered_movies, key=lambda x: x['popularity'], reverse=True)[:500]

        for index, movie in enumerate(filtered_movies):
            file_path = f'Raw/TMDB/JSON/2024/10/26/filme_{index}.json'
            s3_client.put_object(
                Body=json.dumps(movie, indent=4),
                Bucket=bucket_name,
                Key=file_path
            )

        return {'statusCode': 200, 'body': 'Processamento concluído'}
    
    except Exception as error:
        return {'statusCode': 500, 'body': f"Erro ao processar os filmes: {error}"}
```