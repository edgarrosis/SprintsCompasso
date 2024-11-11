import sys
from datetime import datetime
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, explode
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

# Definição das variáveis
trusted_zone = "Trusted"
tmdb = "TMDB"
filmes = "filmes"
elenco = "elenco"
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

# Explodir a coluna 'cast' em múltiplas linhas e criar tabela de elenco
df_cast = df.withColumn("cast", explode("cast")).select(
    col("id").alias("movie_id"),
    col("cast.adult"),
    col("cast.gender"),
    col("cast.id").alias("cast_id"),
    col("cast.known_for_department"),
    col("cast.name"),
    col("cast.original_name"),
    col("cast.popularity"),
    col("cast.profile_path"),
    col("cast.cast_id").alias("cast_cast_id"),
    col("cast.character"),
    col("cast.credit_id"),
    col("cast.order")
)

# Remover a coluna 'cast' na tabela de filmes e adicionar coluna de data de criação para particionamento
df_filmes = df.drop("cast").withColumn("creation_date", col("release_date"))

# Conversão de volta para DynamicFrame
dynamic_frame_filmes = DynamicFrame.fromDF(df_filmes, glueContext, "dynamic_frame_filmes")
dynamic_frame_cast = DynamicFrame.fromDF(df_cast, glueContext, "dynamic_frame_cast")

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

job.commit()
