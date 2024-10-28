# 1. Introdução

O desafio dessa sprint necessitou de dois scripts em Python que realizam operações com arquivos CSV armazenados no Amazon S3, e o sql solicitado com as buscas utilizadas na busca. A aplicação demonstra como enviar arquivos para a nuvem e realizar consultas SQL diretamente em dados usando Pandas e PandasQL.

# 2. Pré Requisitos

1. **Instalações**:
   - Python instalado.
   - AWS CLI instalado e configurado, utilizando o comando a seguir e fornecer as informações necessárias.

   ``` win
   aws configure sso
   ```

   - Caso as credenciais expirem (expiram entre 12 e 24 horas), basta utilizar o comando:
   ```
   aws sso login --profile nome_profile
   ```
   - Instalar as bibliotecas `boto3`, `pandas` e `pandasql`, com o comando:

   ```
   pip install boto3 pandas pandasql
   ```

2. **Execução**:
   - Execute o primeiro script para enviar o arquivo ao S3.
   - Execute o segundo script para carregar, processar e exibir os dados.

# 3. Upload de Arquivo para o S3

O script `envio_arquivo.py` faz o upload de um arquivo CSV para o Amazon S3. Ele começa importando a biblioteca `boto3`, usada para interagir com serviços da AWS, e configura o cliente S3 com um perfil específico (`'edgar-silva'`), que usa as credenciais locais.

As variáveis definem o nome do bucket (`bucket_name`) que ja deve estar criado dentro do S3, o caminho local do arquivo (`medicamento_file_path`) e o caminho de destino no S3 (`s3_file_path`).

O upload é feito pela função `s3.upload_file()`, que envia o arquivo para o bucket. Caso o upload seja bem-sucedido, uma mensagem de sucesso é exibida. Se houver falha, uma mensagem de erro aparece.

![Bucket Desafio 5](/Sprint5/Evidencias/Desafio/bucket_desafio5.png)

![Evidencia 1](/Sprint5/Evidencias/Desafio/envio_arquivo_desafio.png)

#### Código Referenciado
```python
import boto3

# Definição das variáveis
bucket_name = "desafio-sprint5-consultas"
medicamento_file_path = "Sprint5/Desafio/Consultasrealizadasporespecialidadesmaio22aoutubro2022_utf8.csv"

# Configuração do cliente S3
s3 = boto3.session.Session(profile_name='edgar-silva').client('s3')

# Caminho completo no S3
s3_file_path = "Consultasrealizadasporespecialidadesmaio22aoutubro2022_utf8.csv"

# Upload do arquivo CSV
try:
    s3.upload_file(medicamento_file_path, bucket_name, s3_file_path)
    print(f"Arquivo {medicamento_file_path} enviado com sucesso para {s3_file_path} no bucket {bucket_name}.")
except Exception as e:
    print(f"Ocorreu um erro ao enviar o arquivo: {e}")
```

---

# 4. Carregamento e Manipulação de Dados do S3

O script `consultas.py` começa importando bibliotecas essenciais como `boto3` para acessar o Amazon S3, `pandas` para manipulação de dados, `StringIO` para tratar o conteúdo do arquivo como uma string e `pandasql` para executar consultas SQL sobre o DataFrame. 

Em seguida, ele define uma função chamada `carregar_csv_s3` que conecta-se ao bucket S3 utilizando o perfil AWS definido (`edgar-silva`). A função faz o download de um arquivo CSV, decodifica o conteúdo para texto e o carrega em um DataFrame usando `pandas`.

Se o arquivo for carregado com sucesso, o código aplica uma consulta SQL no DataFrame para selecionar dados de consultas realizadas entre maio e outubro, adicionando as colunas `classificação` (baseada no número de consultas) e `mes_somente` (extraindo apenas o mês do campo de data), além de classificar os resultados de acordo com as consultas.

Depois, são executadas mais duas consultas SQL. A primeira agrupa os dados por mês e classificação de consultas, somando o total de consultas por essas categorias. A segunda consulta resume o total de consultas por classificação no período inteiro.

Além das consultas SQL, o código calcula o total e a média de consultas realizadas. Esses resultados, junto com os dados agrupados e resumidos, são exibidos no final. Caso o DataFrame não seja carregado corretamente, o código mostra uma mensagem de erro explicando o problema.

As buscao são salvas em arquivos `.csv` e então enviados para o bucket do S3 seguindo o diretorio `s3://desafio-sprint5-consultas/Resultados/`

### Resultados das buscas:
- [Dataframe Filtrado](/Sprint5/Evidencias/Desafio/df_filtrado.png)
- [Total de consultas](/Sprint5/Evidencias/Desafio/buscas.png)
- [Consultas ordenadas por mes e classificacao](/Sprint5/Evidencias/Desafio/consultas_mes_classificacao.png)
- [Consultas por mes](/Sprint5/Evidencias/Desafio/consultas_por_classificacao.png)
- [Buscar Armazenadas no Bucket S3](/Sprint5/Evidencias/Desafio/buscas-armazenadas.png)

#### Código Referenciado
```python
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

```

---

# 5. Funcionalidades e SQL Aplicado

1. **Cláusula de Filtro com Operadores Lógicos**  
   A consulta SQL filtra dados usando operadores lógicos `LIKE` e `OR` para selecionar meses específicos:
   ```sql
   WHERE mês LIKE '%May%' OR mês LIKE '%June%' ...
   ```

2. **Funções de Agregação**  
   - `SUM`: Soma o total de consultas.
   - `AVG`: Calcula a média de consultas.

3. **Função Condicional**  
   A função `CASE` atribui uma classificação (`BAIXA`, `MEDIA`, `ALTA`) com base na quantidade de consultas:
   ```sql
   CASE 
       WHEN numero_consultas < 100 THEN 'BAIXA' 
       WHEN numero_consultas >= 100 AND numero_consultas < 200 THEN 'MEDIA'
       ELSE 'ALTA' 
   END AS classificacao
   ```

4. **Função de Conversão**  
   A consulta usa `SUBSTR` para extrair a parte do mês:
   ```sql
   SUBSTR(mês, INSTR(mês, '-') + 2) AS mes_somente
   ```

5. **Função de Data**  
   A classificação por mês é baseada no mapeamento de nomes para números:
   ```sql
   CASE 
       WHEN mês LIKE '%May%' THEN 1
       ...
   END AS mes_ordenado
   ```

6. **Função de String**  
   A função `SUBSTR` também é usada para manipular strings do campo de mês.