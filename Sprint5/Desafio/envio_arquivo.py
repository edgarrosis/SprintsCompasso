import boto3

# Definição das variáveis
bucket_name = "desafio-sprint5-consultas"
medicamento_file_path = "Sprint5/Desafio/Consultasrealizadasporespecialidadesmaio22aoutubro2022_utf8.csv"

# Configuração do cliente S3
s3 = boto3.session.Session(profile_name='edgar-silva').client('s3')

# Criação do caminho completo no S3
s3_file_path = "Consultasrealizadasporespecialidadesmaio22aoutubro2022_utf8.csv"

# Upload do arquivo CSV para o S3
try:
    s3.upload_file(medicamento_file_path, bucket_name, s3_file_path)
    print(f"Arquivo {medicamento_file_path} enviado com sucesso para {s3_file_path} no bucket {bucket_name}.")
except Exception as e:
    print(f"Ocorreu um erro ao enviar o arquivo: {e}")
