# Usa a imagem oficial do Python como base
FROM python

# Define o diretório de trabalho no container
WORKDIR /app

# Instala as dependências listadas no requirements.txt
RUN pip install boto3   

# Copia o arquivo Python para o diretório de trabalho
COPY movies.csv .
COPY series.csv .
COPY envio_arquivo.py .

# Define o comando que será executado quando o container iniciar
CMD ["python", "envio_arquivo.py"]