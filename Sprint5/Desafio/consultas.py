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
        df = pd.read_csv(StringIO(data), sep=',', on_bad_lines='skip')
        print("Arquivo carregado com sucesso.")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para enviar DataFrame como CSV para S3
def enviar_csv_s3(dataframe, bucket, caminho_arquivo):
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, index=False)
    s3 = boto3.session.Session(profile_name='edgar-silva').client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=caminho_arquivo, Body=csv_buffer.getvalue())
        print(f"Arquivo {caminho_arquivo} enviado com sucesso para o bucket {bucket}.")
    except Exception as e:
        print(f"Erro ao enviar o arquivo {caminho_arquivo}: {e}")

# Carregar o DataFrame
df = carregar_csv_s3(bucket_name, arquivo)

if df is not None:
    # Consulta SQL para filtrar dados e adicionar classificação e ordem de meses
    query = """
    SELECT 
        * ,
        CASE 
            WHEN numero_consultas < 100 THEN 'BAIXA' 
            WHEN numero_consultas >= 100 AND numero_consultas < 200 THEN 'MEDIA'
            ELSE 'ALTA' 
        END AS classificacao,
        SUBSTR(mês, INSTR(mês, '-') + 2) AS mes_somente,
        CASE 
            WHEN mês LIKE '%May%' THEN 1
            WHEN mês LIKE '%June%' THEN 2
            WHEN mês LIKE '%July%' THEN 3
            WHEN mês LIKE '%August%' THEN 4
            WHEN mês LIKE '%September%' THEN 5
            WHEN mês LIKE '%October%' THEN 6
        END AS mes_ordenado,
        CASE 
            WHEN numero_consultas >= 200 THEN 1
            WHEN numero_consultas >= 100 THEN 2
            ELSE 3
        END AS ordem_classificacao
    FROM df
    WHERE mês LIKE '%May%' OR mês LIKE '%June%' OR mês LIKE '%July%' 
       OR mês LIKE '%August%' OR mês LIKE '%September%' OR mês LIKE '%October%'
    """

    df_filtrado = psql.sqldf(query, locals())

    # Consulta para agrupar e ordenar por mês e classificação
    query_consultas_por_mes_classificacao = """
    SELECT 
        mes_somente, 
        classificacao, 
        SUM(numero_consultas) AS total_consultas
    FROM df_filtrado
    GROUP BY mes_somente, classificacao
    ORDER BY mes_ordenado, ordem_classificacao
    """
    
    # Consulta para totalizar consultas por classificação no período
    query_total_por_classificacao = """
    SELECT 
        classificacao, 
        SUM(numero_consultas) AS total_consultas
    FROM df_filtrado
    GROUP BY classificacao
    ORDER BY ordem_classificacao
    """

    # Executa as consultas e armazena os resultados em DataFrames
    consultas_por_mes_classificacao = psql.sqldf(query_consultas_por_mes_classificacao, locals())
    total_por_classificacao = psql.sqldf(query_total_por_classificacao, locals())

    # Salvar os DataFrames como arquivos .csv e enviar para o S3
    enviar_csv_s3(df_filtrado, bucket_name, "Resultados/filtrado_consultas.csv")
    enviar_csv_s3(consultas_por_mes_classificacao, bucket_name, "Resultados/consultas_por_mes_classificacao.csv")
    enviar_csv_s3(total_por_classificacao, bucket_name, "Resultados/total_consultas_classificacao.csv")

    # Cálculos adicionais
    total_consultas = df_filtrado['numero_consultas'].sum()
    media_consultas = df_filtrado['numero_consultas'].mean()

    # Exibir os resultados adicionais
    print(f"\nTotal de Consultas: {total_consultas}")
    print(f"Média de Consultas: {media_consultas:.2f}")

else:
    print("Erro: O DataFrame não foi carregado.")
