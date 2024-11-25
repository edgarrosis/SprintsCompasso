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
elenco = "elenco"
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

# Explodir a coluna 'cast' em múltiplas linhas e criar tabela de elenco
# Filtrar para incluir apenas registros com 'order' até 2
df_cast = df_filtered.withColumn("cast", explode("cast")).filter(col("cast.order") < 3).select(
    col("id").alias("movie_id"),
    col("cast.adult"),
    col("cast.gender"),
    col("cast.id").alias("actor_id"),
    col("cast.known_for_department"),
    col("cast.name"),
    col("cast.original_name"),
    col("cast.popularity"),
    col("cast.profile_path"),
    col("cast.cast_id"),
    col("cast.character"),
    col("cast.credit_id"),
    col("cast.order")
)

# Explodir a coluna 'production_countries' em múltiplas linhas para criar a tabela de nacionalidades
df_nationalities = df_filtered.withColumn("production_countries", explode("production_countries")).select(
    col("id").alias("movie_id"),
    col("production_countries.iso_3166_1").alias("country_code"),
    col("production_countries.name").alias("country_name")
)

# Remover as colunas 'cast' e 'production_countries' na tabela de filmes e adicionar coluna de data de criação para particionamento
df_filmes = df_filtered.drop("cast", "production_countries").withColumn("creation_date", col("release_date"))

# Conversão de volta para DynamicFrame
dynamic_frame_filmes = DynamicFrame.fromDF(df_filmes, glueContext, "dynamic_frame_filmes")
dynamic_frame_cast = DynamicFrame.fromDF(df_cast, glueContext, "dynamic_frame_cast")
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

# Tabela de elenco
datasink_cast = glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_cast,
    connection_type="s3",
    connection_options={
        "path": f"s3://{bucket_name}/{trusted_zone}/{tmdb}/{elenco}/{current_date}/",
        "partitionKeys": ["movie_id"]
    },
    format="parquet",
    transformation_ctx="datasink_cast"
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
