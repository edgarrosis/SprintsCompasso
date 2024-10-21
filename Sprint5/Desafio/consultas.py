import boto3
import pandas as pd
from io import StringIO
import pandasql as psql

# Definição das variáveis
bucket_name = "desafio-sprint5-consultas"
arquivo = "Consultasrealizadasporespecialidadesmaio22aoutubro2022_utf8.csv"

# Função para carregar o CSV do S3 em um DataFrame Pandas
def carregar_csv_s3(bucket, arquivo):
    s3 = boto3.session.Session(profile_name='edgar-silva').client('s3')
    try:
        obj = s3.get_object(Bucket=bucket, Key=arquivo)
        data = obj['Body'].read().decode('utf-8') 
        df = pd.read_csv(StringIO(data), sep=',', on_bad_lines='skip')  # Lendo o CSV com ',' como delimitador
        print("Arquivo carregado com sucesso.")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None

# Carregar o DataFrame
df = carregar_csv_s3(bucket_name, arquivo)

if df is not None:
    # Usando pandasql para realizar as consultas

    # 4.1 e 4.2 Filtrar dados usando dois operadores lógicos e calcular soma e média
    query = """
    SELECT 
        *,
        CASE 
            WHEN numero_consultas < 100 THEN 'BAIXA' 
            WHEN numero_consultas >= 100 AND numero_consultas < 200 THEN 'MEDIA'
            ELSE 'ALTA' 
        END as classificacao,
        SUBSTR(mês, INSTR(mês, '-') + 2) as mes_somente
    FROM df
    WHERE (mês LIKE '%May%' OR mês LIKE '%June%' OR mês LIKE '%July%' OR mês LIKE '%August%' OR mês LIKE '%September%' OR mês LIKE '%October%')
    """
    
    df_filtrado = psql.sqldf(query, locals())

    # Contagem de consultas por classificação e mês
    consultas_por_mes_classificacao = df_filtrado.groupby(['mes_somente', 'classificacao'])['numero_consultas'].sum().reset_index()

    # Total de consultas por classificação em todo o período
    total_por_classificacao = df_filtrado.groupby('classificacao')['numero_consultas'].sum().reset_index()

    # Exibir resultados
    print("\nDataFrame Filtrado:")
    print(df_filtrado)

    total_consultas = df_filtrado['numero_consultas'].sum()  # Soma total de consultas
    media_consultas = df_filtrado['numero_consultas'].mean()  # Média de consultas

    print(f"\nTotal de Consultas: {total_consultas}")
    print(f"Média de Consultas: {media_consultas:.2f}")

    print("\nConsultas por Mês e Classificação:")
    print(consultas_por_mes_classificacao)

    print("\nTotal de Consultas por Classificação no Período:")
    print(total_por_classificacao)

else:
    print("Erro: O DataFrame não foi carregado.")
