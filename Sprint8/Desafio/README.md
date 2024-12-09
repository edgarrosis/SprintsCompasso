# 1. Introdução

Este projeto implementa a etapa 3 do desafio final e consiste em realizar a ingestão e tratamento de dados de filmes utilizando AWS Glue e a criação de uma camada Trusted no bucket S3. O objetivo é processar o arquivo CSV de filmes e arquivos JSON contendo informações de filmes e atores coletadas do TMDB, armazenando os dados tratados em um Data Lake na AWS.

# 2. Estrutura do Projeto

O projeto está organizado da seguinte forma:

- Scripts AWS Glue para processar e tratar dados de filmes e elenco.
- Crawlers para detectar e catalogar automaticamente os dados no Glue Data Catalog.
- Armazenamento dos dados processados na camada Trusted do bucket S3.

## 2.1 Arquitetura do Bucket S3

Os dados são armazenados no bucket seguindo o seguinte padrão de diretórios:

```
s3://data-lake-edgar-silva/Trusted/Local/CSV/filmes/2024/11/08/
```
![trusted_csv](/Sprint8/Evidencias/Desafio/trusted_csv.png)


```
s3://data-lake-edgar-silva/Trusted/TMDB/filmes/2024/12/05/

s3://data-lake-edgar-silva/Trusted/TMDB/nacionalidades/2024/12/05/
```
![trusted_tmdb_filme](/Sprint8/Evidencias/Desafio/trusted_tmdb_filmes.png)
![trusted_tmdb_nacionalidades](/Sprint8/Evidencias/Desafio/trusted_tmdb_nacionalidade.png)


# 3. Configuração do Projeto

## 3.1 Pré-requisitos

1. **AWS IAM**: Configurado com permissões para acessar o bucket S3 e executar os jobs do Glue.
2. **AWS Glue**: Configurado com os scripts e crawlers necessários para processar os dados.

## 3.2 Scripts Glue

Para fazer a leitura e tratamento dos dados, e armazena-los na camada trusted no formato .parquet, foram utilizados 2 scripts:

### I. Processamento do CSV
- Este primeiro script [processa_csv.py](/Sprint8/Desafio/Etapa3/processa_csv.py), faz a leitura do arquivo `moveis.csv` armazenado no bucket, faz o devido tratamentos de dados com linhas com dados faltantes, e em seguida faz a conversão dos dados para o formato `.parquet` e cria a camada Trusted no bucket.
- ![glue_processa_csv](/Sprint8/Evidencias/Desafio/glue_processa_csv.png)

#### II. Processamento dos JSONs
- ja o segundo script [processa_tmdb.py](/Sprint8/Desafio/Etapa3/processa_tmdb.py), faz a leitura dos arquivos `JSONs` criados apartir de dados do TMDB utilizando a API, resultado do desafio anterior, armazenados no bucket, faz o devido tratamentos de dados, e em seguida também faz a conversão dos dados para o formato `.parquet` e cria a camada Trusted no bucket. Os dados foram divididos em 2 diretorios, um para os dados relacionados as nacionalidades dos filmes, e outro para os filmes em si.
- ![glue_processa_tmdb](/Sprint8/Evidencias/Desafio/glue_processa_tmdb.png)

## 3.3 Configuração dos Crawlers

### I. Crawler para CSV
Um Crawler foi configurado para varrer o diretório onde os arquivos PARQUET que o `processa_csv` criou foram armazenados e criar uma tabela no Glue Data Catalog.

![crawler_processa_csv](/Sprint8/Evidencias/Desafio/csv_crawler.png)

### II. Crawler para TMDB
Outro Crawler foi configurado para varrer o diretório onde os arquivos PARQUET que o `processa_tmdb` criou foram armazenados. Este Crawler cria duas tabelas no Glue Data Catalog, uma mapeando os dados dos filmes, e outra mapeando os dados das nacionalidades.

![crawler_processa_tmdb](/Sprint8/Evidencias/Desafio/tmdb_crawler.png)

# 4. Estrutura do Código

## 4.1 processa_csv.py

1. **Definição das Variáveis**: O script começa definindo variáveis importantes como `trusted_zone`, `local`, `csv`, `filmes`, `current_date`, e `bucket_name`. Essas variáveis determinam onde os dados serão armazenados e como serão estruturados no S3.

2. **Inicialização do Spark e Glue Contexts**: Aqui, o script inicializa os contextos do Spark e do Glue, que são necessários para executar o job de ETL (Extração, Transformação e Carga).

3. **Leitura do CSV**: O script lê os dados do arquivo CSV diretamente do S3 utilizando a opção de delimitador `|` e configura o cabeçalho para reconhecer as colunas.

4. **Tratamento dos Dados**: Nesta etapa, o script aplica várias transformações para limpar e preparar os dados:
    - Substitui valores `\N` por strings vazias ou `None` em colunas específicas.
    - Converte tipos de dados, como transformar colunas em inteiros (`int`) ou números de ponto flutuante (`double`), conforme necessário.

5. **Escrita dos Dados no S3**: Após o tratamento, os dados são escritos no S3 em formato Parquet. O script utiliza a estrutura de diretórios definida nas variáveis para particionar os dados por data de criação (`current_date`).

6. **Commit do Job do Glue**: Finalmente, o script executa um `commit` para finalizar o job do Glue, garantindo que todas as operações foram concluídas com sucesso.

Codigo Referenciado:

```python
import sys
from datetime import datetime
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job

# Definição das variáveis
trusted_zone = "Trusted"
local = "Local"
csv = "CSV"
filmes = "filmes"
current_date = datetime.now().strftime("%Y/%m/%d")

bucket_name = "data-lake-edgar-silva"
csv_path = "s3://data-lake-edgar-silva/Raw/Local/CSV/filmes/2024/10/16/movies.csv"

# Obter parâmetros
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Inicializar o Spark e Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Nome do job do Glue
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Ler dados do CSV diretamente do S3
df = spark.read.option("delimiter", "|").csv(csv_path, header=True)

# Aplicar tratamento de dados
df = df.withColumn("titulopincipal", when(col("titulopincipal") != "\\N", col("titulopincipal")).otherwise(""))
df = df.withColumn("anolancamento", when((col("anolancamento") != "\\N") & (col("anolancamento") != ""), col("anolancamento").cast("int")).otherwise(None))
df = df.withColumn("tempominutos", when((col("tempominutos") != "\\N") & (col("tempominutos") != ""), col("tempominutos").cast("int")).otherwise(None))
df = df.withColumn("genero", when(col("genero") != "\\N", col("genero")).otherwise(""))
df = df.withColumn("notamedia", when((col("notamedia") != "\\N") & (col("notamedia") != ""), col("notamedia").cast("double")).otherwise(None))
df = df.withColumn("numerovotos", when((col("numerovotos") != "\\N") & (col("numerovotos") != ""), col("numerovotos").cast("int")).otherwise(None))
df = df.withColumn("generoartista", when(col("generoartista") != "\\N", col("generoartista")).otherwise(""))
df = df.withColumn("personagem", when(col("personagem") != "\\N", col("personagem")).otherwise(""))
df = df.withColumn("nomeartista", when(col("nomeartista") != "\\N", col("nomeartista")).otherwise(""))
df = df.withColumn("anonascimento", when((col("anonascimento") != "\\N") & (col("anonascimento") != ""), col("anonascimento").cast("int")).otherwise(None))
df = df.withColumn("anofalecimento", when((col("anofalecimento") != "\\N") & (col("anofalecimento") != ""), col("anofalecimento").cast("int")).otherwise(None))
df = df.withColumn("profissao", when(col("profissao") != "\\N", col("profissao")).otherwise(""))
df = df.withColumn("titulosmaisconhecidos", when(col("titulosmaisconhecidos") != "\\N", col("titulosmaisconhecidos")).otherwise(""))

# Escrever dados na camada Trusted em formato Parquet
df.write.mode("overwrite").parquet(f"s3://{bucket_name}/{trusted_zone}/{local}/{csv}/{filmes}/{current_date}/")

job.commit()
```

## 4.2 processa_json.py

1. **Definição das Variáveis**: O script começa definindo variáveis importantes como `trusted_zone`, `tmdb`, `filmes`, `elenco`, `current_date`, e `bucket_name`. Essas variáveis determinam onde os dados serão armazenados e como serão estruturados no S3.

2. **Inicialização do Spark e Glue Contexts**: Aqui, o script inicializa os contextos do Spark e do Glue, que são necessários para executar o job de ETL (Extração, Transformação e Carga).

3. **Leitura dos Arquivos JSON**: O script lê os dados de múltiplos arquivos JSON diretamente do S3 utilizando a função `create_dynamic_frame.from_options` do Glue Context. Esta função permite especificar o caminho dos arquivos JSON e seu formato.

4. **Remoção da Coluna `cast` da Tabela de Filmes**: Após a explosão da coluna `cast`, a coluna é removida da tabela de filmes original para evitar redundância. Não foi utilizado na analise final do Desafio.

5. **Conversão para DynamicFrame**: As DataFrames resultantes são convertidas de volta para DynamicFrame, que é o formato necessário para o Glue trabalhar com os dados.

6. **Escrita dos Dados no S3**: Os dados dos filmes e do elenco são escritos no S3 em formato Parquet. O script utiliza a estrutura de diretórios definida nas variáveis para particionar os dados por data de criação (`creation_date`) e pelo identificador do filme (`movie_id`).

7. **Commit do Job do Glue**: Finalmente, o script executa um `commit` para finalizar o job do Glue, garantindo que todas as operações foram concluídas com sucesso.

Código Referenciado:

```python
import sys
from datetime import datetime
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, explode, array_contains
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

# Definição das variáveis
trusted_zone = "Trusted"
tmdb = "TMDB"
filmes = "filmes"
nacionalidades = "nacionalidades"
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

# Ler dados da camada Raw (vários arquivos JSON)
datasource0 = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": ["s3://data-lake-edgar-silva/Raw/TMDB/JSON/2024/10/26/"]
    },
    format="json",
    transformation_ctx="datasource0"
)

# Conversão para DataFrame para operações adicionais
df = datasource0.toDF()

# IDs dos gêneros Crime e Guerra
crime_genre_id = 80
war_genre_id = 10752

# Filtrar filmes das categorias Crime ou Guerra
df_filtered = df.filter(array_contains(col("genre_ids"), crime_genre_id) | array_contains(col("genre_ids"), war_genre_id))

# Explodir a coluna 'production_countries' em múltiplas linhas para criar a tabela de nacionalidades
df_nationalities = df_filtered.withColumn("production_countries", explode("production_countries")).select(
    col("id").alias("movie_id"),
    col("production_countries.iso_3166_1").alias("country_code"),
    col("production_countries.name").alias("country_name")
)

# Remover as colunas 'cast' e 'production_countries' na tabela de filmes, adicionar coluna de data de criação para particionamento e converter `budget` e `revenue` para `bigint`
df_filmes = df_filtered.drop("cast", "production_countries")\
    .withColumn("creation_date", col("release_date"))\
    .withColumn("budget", col("budget").cast("bigint"))\
    .withColumn("revenue", col("revenue").cast("bigint"))

# Conversão de volta para DynamicFrame
dynamic_frame_filmes = DynamicFrame.fromDF(df_filmes, glueContext, "dynamic_frame_filmes")
dynamic_frame_nationalities = DynamicFrame.fromDF(df_nationalities, glueContext, "dynamic_frame_nationalities")

# Escrever dados na camada Trusted em formato Parquet, particionado por data de criação
# Tabela de filmes
datasink_filmes = glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_filmes,
    connection_type="s3",
    connection_options={
        "path": f"s3://{bucket_name}/{trusted_zone}/{tmdb}/{filmes}/{current_date}/",
        "partitionKeys": ["creation_date"]
    },
    format="parquet",
    transformation_ctx="datasink_filmes"
)

# Tabela de nacionalidades
datasink_nationalities = glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_nationalities,
    connection_type="s3",
    connection_options={
        "path": f"s3://{bucket_name}/{trusted_zone}/{tmdb}/{nacionalidades}/{current_date}/",
        "partitionKeys": ["movie_id"]
    },
    format="parquet",
    transformation_ctx="datasink_nationalities"
)

job.commit()
```

# 5. Conclusão
O primeiro script lida com a ingestão e tratamento de dados de um arquivo CSV, convertendo e limpando informações antes de armazená-las na camada Trusted do S3 em formato Parquet. O segundo script, por sua vez, manipula dados de arquivos JSON, explodindo a coluna cast em várias linhas para criar uma tabela separada de elenco e armazenando os dados também em formato Parquet. Por fim, os Crawlers criam as tabelas no Glue Datalog o que possibilita que as buscas ja sejam feitas.

![glue_tables](/Sprint8/Evidencias/Desafio/trusted_tables.png)