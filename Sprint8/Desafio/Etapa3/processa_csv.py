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
