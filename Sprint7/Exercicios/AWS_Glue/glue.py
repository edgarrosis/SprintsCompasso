import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
import pyspark.sql.functions as F

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
bucket_name = 'bucket-exs-gvnn'
s3_file_path = f's3://bucket-exs-gvnn/dados/nomes.csv'
df = spark.read.option("header", "true").csv(s3_file_path)

df.printSchema()

df = df.withColumn('nome', F.upper(F.col('nome')))

print(f"Linhas no DF: {df.count()}")

df_grouped = df.groupBy('ano', 'sexo').count()
df_grouped.show()

df_sorted = df.orderBy(F.col('ano').desc())
df_sorted.show()

female_max = df.filter(F.col('sexo') == 'F').groupBy('nome', 'ano').count().orderBy(F.col('count').desc()).first()
print(f"Nome feminino que mais aparece: {female_max['nome']} in year {female_max['ano']}")

male_max = df.filter(F.col('sexo') == 'M').groupBy('nome', 'ano').count().orderBy(F.col('count').desc()).first()
print(f"Nome masculino que mais aparece: {male_max['nome']} in year {male_max['ano']}")

df_yearly = df.groupBy('ano').count().orderBy(F.col('ano').asc()).limit(10)
df_yearly.show()

output_path = f's3://{bucket_name}/lab-glue/frequencia_registro_nomes_eua'
df.write.partitionBy('sexo', 'ano').json(output_path)