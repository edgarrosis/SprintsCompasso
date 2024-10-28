import json
import requests
import pandas as pd
import boto3
import os

def lambda_handler(event, context):
    # Configuração do cliente S3 e das variáveis de ambiente
    s3_client = boto3.client('s3')
    bucket_name = 'data-lake-edgar-silva'
    api_key_tmdb = os.getenv('API_KEY_TMDB')

    try:
        # Verifica se o bucket existe
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except boto3.exceptions.S3UploadFailedError:
            print(f"Bucket {bucket_name} não encontrado.")
            return {'statusCode': 500, 'body': f"Bucket {bucket_name} não encontrado."}

        # Lê o CSV com filmes do IMDb armazenado no S3 em partes menores
        csv_object = s3_client.get_object(Bucket=bucket_name, Key='Raw/Local/CSV/filmes/2024/10/16/movies.csv')
        chunk_size = 1000
        filtered_movies = []

        for chunk in pd.read_csv(csv_object['Body'], sep='|', chunksize=chunk_size, dtype={'id': str, 'genero': str, 'anoLancamento': str}):
            # Remove filmes duplicados e filtra por Crime ou Guerra e lançados após os anos 70
            chunk = chunk.drop_duplicates(subset=['id'])
            chunk['anoLancamento'] = chunk['anoLancamento'].replace('\\N', '0').astype(int)
            imdb_filtered = chunk[(chunk.genero.str.contains("Crime|War", regex=True)) & (chunk.anoLancamento > 1980)]

            # Processa cada filme filtrado
            for _, movie in imdb_filtered.iterrows():
                imdb_id = movie['id']
                # Requisição para buscar o filme no TMDB usando o ID do IMDb
                url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key_tmdb}&language=pt-BR&external_source=imdb_id"
                response = requests.get(url)
                data = response.json()

                if data.get('movie_results'):
                    movie_details = data['movie_results'][0]
                    movie_id = movie_details['id']
                    # Requisição para buscar o elenco do filme no TMDB
                    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key_tmdb}&language=pt-BR"
                    response = requests.get(url)
                    credits_data = response.json()
                    movie_details['cast'] = credits_data.get('cast', [])
                    filtered_movies.append(movie_details)

        # Ordena os filmes pela popularidade e seleciona os 500 melhores
        filtered_movies = sorted(filtered_movies, key=lambda x: x['popularity'], reverse=True)[:500]

        # Armazena os resultados em arquivos JSON separados no S3
        for index, movie in enumerate(filtered_movies):
            file_path = f'Raw/TMDB/JSON/2024/10/26/filme_{index}.json'
            s3_client.put_object(
                Body=json.dumps(movie, indent=4),
                Bucket=bucket_name,
                Key=file_path
            )

        return {'statusCode': 200, 'body': 'Processamento concluído'}
    
    except Exception as error:
        print(f"Erro ao processar os filmes: {error}")
        return {'statusCode': 500, 'body': f"Erro ao processar os filmes: {error}"}
