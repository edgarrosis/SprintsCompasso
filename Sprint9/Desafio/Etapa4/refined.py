import sys
from datetime import datetime
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, explode, array, udf, lit
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
df_exploded = df_combined.withColumn("genre_id", explode(col("genre_ids")))

# Criar fact_genero_movie
df_fact_genero_movie = df_exploded.join(
    df_dim_genero, 
    df_exploded["genre_id"] == df_dim_genero["genero"]
).select(
    col("id").alias("movie_id"),
    col("genero_id")
)

# Criar fact_movie_country apenas com informações do TMDB Filmes
df_fact_movie_country = df_tmdb_filmes.join(
    df_tmdb_nacionalidade, 
    df_tmdb_filmes["id"] == df_tmdb_nacionalidade["movie_id"]
).select(
    col("id").alias("movie_id"),
    col("country_code")
)

# Salvar as tabelas na camada Refined em formato Parquet
# Tabela dim_genero
df_dim_genero.write.mode("overwrite").parquet(f"s3://{bucket_name}/{refined_zone}/dim_genero/{current_date}/")

# Tabela dim_movie
df_dim_movie.write.mode("overwrite").parquet(f"s3://{bucket_name}/{refined_zone}/dim_movie/{current_date}/")

# Tabela dim_country
df_dim_country.write.mode("overwrite").parquet(f"s3://{bucket_name}/{refined_zone}/dim_country/{current_date}/")

# Tabela fact_movie_rating
df_fact_movie_rating.write.mode("overwrite").parquet(f"s3://{bucket_name}/{refined_zone}/fact_movie_rating/{current_date}/")

# Tabela fact_genero_movie
df_fact_genero_movie.write.mode("overwrite").parquet(f"s3://{bucket_name}/{refined_zone}/fact_genero_movie/{current_date}/")

# Tabela fact_movie_country
df_fact_movie_country.write.mode("overwrite").parquet(f"s3://{bucket_name}/{refined_zone}/fact_movie_country/{current_date}/")

# Encerrar sessão Spark
job.commit()
