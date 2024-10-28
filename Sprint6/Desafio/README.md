# 1. Introdução

Este projeto consiste na ingestão de dados de filmes e séries no formato CSV para um Data Lake na AWS, utilizando um container Docker para executar o processo de carga com a biblioteca `boto3`.

O desafio teve como objetivo praticar a construção de um Data Lake, passando pelas etapas de ingestão, armazenamento, processamento e consumo de dados. Nesta primeira entrega, o foco é a **Ingestão de Batch**, que consiste em fazer o upload dos arquivos CSV para um bucket S3 na AWS.

# 2. Estrutura do Projeto

O projeto está organizado da seguinte forma:

- **`Dockerfile`**: Configuração do container Docker que será utilizado para executar o código Python.

- **`envio_arquivo.py`**: Código Python responsável por ler os arquivos CSV e fazer o upload para o bucket S3.

- **`movies.csv` e `series.csv`**: Arquivos de dados a serem carregados no bucket S3.

## 2.1 Arquitetura do Bucket S3

Os dados são armazenados no bucket seguindo o seguinte padrão de diretórios:

```
S3://data-lake-edgar-silva/Raw/Local/CSV/[Categoria]/[AAAA]/[MM]/[DD]/[arquivo]
```
![Bucket Desafio 6](/Sprint6/Evidencias/Desafio/bucket.png)

## 2.2 Instruções de Execução

### Pré-requisitos

- Docker instalado na máquina.
- Instalar a biblioteca `boto3`:

    ```python
    pip install boto3
    ```

- Acesso configurado à AWS com permissões de gravação no S3 (via `~/.aws/credentials`). Foi utlizado a criação de um perfil SSO pela AWS CLI, assim como foi utilizado na [Sprint 5](/Sprint5/Desafio/README.md):

    ```bash
    aws configure sso
    ```
- Arquivos `movies.csv` e `series.csv` localmente disponíveis.

### Execução

1. **Configurar o ambiente AWS**:
   Certifique-se de que os token de acesso são recentes, realizando o login se necessario.

   ```bash
   aws sso login --profile nome_profile
   ```

2. **Build do Docker**:
   Execute o comando para construir a imagem Docker:
   ```bash
   docker build -t arquivo_datalake .
   ```

   ![Docker image](/Sprint6/Evidencias/Desafio/envio_arquivo_image.png)

3. **Executar o Container**:
   Para rodar o container e fazer o upload dos arquivos para o bucket S3, utilize o comando, que irá acessar o diretorio `~/.aws/credentials`, e enviara uma copia dele como um volume para o conteiner do docker, com os tokens de acesso mais recentes da conta:
   ```bash
   docker run -it --rm -v ${env:USERPROFILE}\.aws:/root/.aws -v ${PWD}:/app -w /app arquivo_datalake
   ```

    ![Docker container](/Sprint6/Evidencias/Desafio/envio_arquivo_container.png)

5. **Verificar o Upload**:
   Após a execução, você poderá verificar no bucket S3 se os arquivos foram carregados corretamente.

    ![Diretorio com movies.csv](/Sprint6/Evidencias/Desafio/bucket_filmes.png)

    ![Diretorio com series.csv](/Sprint6/Evidencias/Desafio/bucket_series.png)

# 3. Estrutura do Código

### envio_arquivo.py

Este script realiza o upload de dois arquivos CSV (filmes e séries) para o bucket S3 na AWS. Abaixo está um resumo do que ele faz:

- Lê os arquivos CSV localmente.
- Utiliza a biblioteca `boto3` para fazer o upload dos arquivos para o bucket S3.
- O caminho no S3 segue o padrão definido pelo desafio, incluindo a data de processamento.

```python
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
```

### Dockerfile

O `Dockerfile` define as instruções para criar a imagem Docker, incluindo a instalação das dependências e a cópia dos arquivos necessários para o container.

```dockerfile
# Usa a imagem oficial do Python como base
FROM python

# Define o diretório de trabalho no container
WORKDIR /app

# Instala as dependências
RUN pip install boto3

# Copia o arquivo Python para o diretório de trabalho
COPY movies.csv .
COPY series.csv .
COPY envio_arquivo.py .

# Define o comando que será executado quando o container iniciar
CMD ["python", "envio_arquivo.py"]
```