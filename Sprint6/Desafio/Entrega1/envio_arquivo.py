import boto3
from datetime import datetime

# Definição das variáveis
raw_zone = "Raw"
local = "Local"
csv = "CSV"
filmes = "filmes"
series = "series"
current_date = datetime.now().strftime("%Y/%m/%d")
filmes_file_path = "movies.csv"
series_file_path = "series.csv"

bucket_name = "data-lake-edgar-silva"

# Configuração do cliente S3 com token de sessão
s3 = boto3.session.Session(profile_name='edgar-silva').client('s3')

# Função para fazer upload
def upload_to_s3(file_path, s3_path):
    try:
        s3.upload_file(file_path, bucket_name, s3_path)
        print(f"Arquivo {file_path} enviado com sucesso para {s3_path} no bucket {bucket_name}.")
    except Exception as e:
        print(f"Ocorreu um erro ao enviar o arquivo: {e}")

# Caminhos no S3
filmes_s3_path = f"{raw_zone}/{local}/{csv}/{filmes}/{current_date}/filmes.csv"
series_s3_path = f"{raw_zone}/{local}/{csv}/{series}/{current_date}/series.csv"

# Upload dos arquivos
upload_to_s3(filmes_file_path, filmes_s3_path)
upload_to_s3(series_file_path, series_s3_path)