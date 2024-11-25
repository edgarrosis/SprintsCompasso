# 1. Introdução

Este projeto implementa a Etapa 4 do desafio, consistindo na ingestão, tratamento e análise dos dados de filmes utilizando AWS Glue. O objetivo é processar os dados armazenados na camada Trusted, criando uma camada Refined no bucket S3, com dados organizados e prontos para a etapa final.

Antes de continuar com a execução dessa etapa, foi necessario utilizar o script [nacionalidades.py](/Sprint9/Desafio/Etapa4/nacionalidade.py) e refazer a camada Trusted, complementando o dataframe com dados que serão necessarios para a analise da etapa final do desafio.

# 2. Estrutura do Projeto

O projeto está organizado da seguinte forma:

- Scripts AWS Glue para processar e tratar dados de filmes, criando a camada Refined.
- Crawlers para detectar e catalogar automaticamente os dados no Glue Data Catalog.
- Armazenamento dos dados processados na camada Refined do bucket S3.

Também foi necessario realizar a modelagem dimensional dos dados para a criação da camada Refined, foi utilizado o seguinte padrao utilizando o snowflake schema:

![modelo_dimensional](/Sprint9/Evidencias/modelagem_dimensional.png)

## 2.1 Arquitetura do Bucket S3

Os dados são armazenados no bucket seguindo o seguinte padrão de diretórios:

```
s3://data-lake-edgar-silva/Refined/dim_genero/2024/11/24/
s3://data-lake-edgar-silva/Refined/dim_movie/2024/11/24/
s3://data-lake-edgar-silva/Refined/dim_country/2024/11/24/
s3://data-lake-edgar-silva/Refined/fact_movie_rating/2024/11/24/
s3://data-lake-edgar-silva/Refined/fact_genero_movie/2024/11/24/
s3://data-lake-edgar-silva/Refined/fact_movie_country/2024/11/24/
```
![refined_bucket](/Sprint9/Evidencias/bucket_refined.png)

# 3. Configuração do Projeto

## 3.1 Pré-requisitos

1. **AWS IAM**: Configurado com permissões para acessar o bucket S3 e executar os jobs do Glue.
2. **AWS Glue**: Configurado com os scripts e crawlers necessários para processar os dados.

## 3.2 Script Glue

Para processar e tratar os dados na camada Trusted e armazená-los na camada Refined em formato `.parquet`, foi utilizado um script principal:

### I. Processamento e Criação da Camada Refined

- Este script [refined.py](/Sprint9/Desafio/Etapa4/refined.py) lê os dados da camada Trusted, faz os devidos tratamentos e transforma os dados, criando as tabelas dimensionais e de fatos na camada Refined. O script realiza as seguintes tarefas:
    - Leitura dos dados das tabelas Trusted.
    - Transformações para criar tabelas dimensionais e de fatos.
    - Escrita dos dados na camada Refined no formato `.parquet`.

![refined_glue_job](/Sprint9/Evidencias/refined_glue_job.png)

## 3.3 Configuração dos Crawlers

### I. Crawler para a Camada Refined

Um Crawler foi configurado para varrer os diretórios onde os arquivos PARQUET da camada Refined foram armazenados e criar tabelas no Glue Data Catalog.

![refined_crawler](/Sprint9/Evidencias/refined_crawler.png)

# 4. Estrutura do Código

## 4.1 processa_refined.py

1. **Definição das Variáveis**: O script começa definindo variáveis importantes como `refined_zone`, `bucket_name`, e `current_date`. Essas variáveis determinam onde os dados serão armazenados e como serão estruturados no S3.

2. **Inicialização do Spark e Glue Contexts**: O script inicializa os contextos do Spark e do Glue, necessários para executar o job de ETL (Extração, Transformação e Carga).

3. **Leitura dos Dados Trusted**: O script lê os dados das tabelas Trusted diretamente do Glue Catalog.

4. **Tratamento e Transformação dos Dados**:
    Os tratamentos dos dados incluem a união das tabelas com os dados dos filmes do CSV e do TMDB, assim como adaptar algumas colunas para que essa união seja possível.
    - **Criação de Tabelas Dimensionais**: `dim_genero`, `dim_movie`, `dim_country`.
    - **Criação de Tabelas de Fatos**: `fact_movie_rating`, `fact_genero_movie`, `fact_movie_country`.
    - ![tabelas_refined](/Sprint9/Evidencias/tabelas_refined.png)

5. **Escrita dos Dados na Camada Refined**: Após o tratamento, os dados são escritos no S3 em formato Parquet, utilizando a estrutura de diretórios definida nas variáveis.

6. **Commit do Job do Glue**: Finalmente, o script executa um `commit` para finalizar o job do Glue, garantindo que todas as operações foram concluídas com sucesso.

Código Referenciado:

```python
import sys
from datetime import datetime
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, explode, array, udf
from pyspark.sql.types import ArrayType, StringType
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

# Definição das variáveis
refined_zone = "Refined"
current_date = datetime.now().strftime("%Y/%m/%d")
bucket_name = "data-lake-edgar-silva"

# Obter parâmetros
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Inicializar o Spark e Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Nome do job do Glue
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Ler dados da camada Trusted (CSV)
datasource_csv = glueContext.create_dynamic_frame.from_catalog(
    database = "trusted_db", 
    table_name = "csv_11"
)

# Ler dados da camada Trusted (TMDB Filmes)
datasource_tmdb_filmes = glueContext.create_dynamic_frame.from_catalog(
    database = "trusted_db", 
    table_name = "tmdb_filmes"
)

# Ler dados da camada Trusted (TMDB Nacionalidade)
datasource_tmdb_nacionalidade = glueContext.create_dynamic_frame.from_catalog(
    database = "trusted_db", 
    table_name = "tmdb_nacionalidades"
)

# Conversão para DataFrame para operações adicionais
df_csv = datasource_csv.toDF()
df_tmdb_filmes = datasource_tmdb_filmes.toDF()
df_tmdb_nacionalidade = datasource_tmdb_nacionalidade.toDF()

# Converter movie_id para string e anolancamento de int para string no CSV
df_csv = df_csv.withColumn("id", col("id").cast("string"))
df_csv = df_csv.withColumn("anolancamento", col("anolancamento").cast("string"))

# Converter id para string no TMDB Filmes
df_tmdb_filmes = df_tmdb_filmes.withColumn("id", col("id").cast("string"))

# Mapeamento completo de genres
genre_mapping = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

# Função UDF para mapear genre_ids para strings
def map_genre(genre_ids):
    if genre_ids is None:
        return []
    return [genre_mapping.get(int(genre_id), "Unknown") for genre_id in genre_ids]

# Registrar a função UDF
map_genre_udf = udf(map_genre, ArrayType(StringType()))

# Mapear genre_ids para strings (transforma a coluna em array de strings)
df_tmdb_filmes = df_tmdb_filmes.withColumn("genre_ids", map_genre_udf(col("genre_ids")))

# Unir dados das tabelas CSV e TMDB Filmes
df_combined = df_csv.unionByName(df_tmdb_filmes, allowMissingColumns=True)

# Remover colunas de partição
df_combined = df_combined.drop("partition_0", "partition_1", "partition_2")
df_tmdb_filmes = df_tmdb_filmes.drop("partition_0", "partition_1", "partition_2")
df_tmdb_nacionalidade = df_tmdb_nacionalidade.drop("partition_0", "partition_1", "partition_2")

# Criar dim_genero com ID auto-incremento
df_dim_genero = spark.createDataFrame([(k, v) for k, v in genre_mapping.items()], ["genero_id", "genero"])

# Criar dim_movie
df_dim_movie = df_combined.select(
    col("id").alias("movie_id"),
    col("title"),
    col("original_title"),
    col("release_date")
)

# Criar dim_country
df_dim_country = df_tmdb_nacionalidade.select(
    col("country_code").alias("country_code"),
    col("country_name").alias("country_name")
).distinct()

# Criar fact_movie_rating
df_fact_movie_rating = df_tmdb_filmes.select(
    col("id").alias("movie_id"),
    col("vote_average").alias("rating"),
    col("vote_count")
)

# Explodir genre_ids antes de fazer a comparação
df_exploded = df