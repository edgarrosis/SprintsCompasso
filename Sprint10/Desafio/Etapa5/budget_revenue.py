import json
import requests
import boto3
import os

# Configuração do cliente S3 e das variáveis de ambiente
s3 = boto3.session.Session(profile_name='edgar-silva').client('s3')
bucket_name = 'data-lake-edgar-silva'
api_key_tmdb = os.getenv('API_KEY_TMDB')

def get_movie_budget_revenue(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key_tmdb}&language=pt-BR"
    response = requests.get(url)
    data = response.json()
    return {
        'budget': data.get('budget', 0),
        'revenue': data.get('revenue', 0)
    }

def update_movies_budget_revenue():
    # Listar os arquivos no bucket S3
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix='Raw/TMDB/JSON/2024/10/26/')
    if 'Contents' not in response:
        print("Nenhum arquivo encontrado no bucket.")
        return

    for obj in response['Contents']:
        file_key = obj['Key']
        if file_key.endswith('.json'):
            # Baixar o arquivo JSON
            file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
            movie = json.loads(file_obj['Body'].read().decode('utf-8'))

            # Obter detalhes do filme e adicionar custo e lucro
            movie_id = movie.get('id')
            if movie_id:
                budget_revenue = get_movie_budget_revenue(movie_id)
                movie['budget'] = budget_revenue['budget']
                movie['revenue'] = budget_revenue['revenue']

                # Atualizar o arquivo JSON no S3
                s3.put_object(
                    Body=json.dumps(movie, indent=4),
                    Bucket=bucket_name,
                    Key=file_key
                )
                print(f"Custo e lucro adicionados para o filme ID: {movie_id}")

if __name__ == "__main__":
    update_movies_budget_revenue()
