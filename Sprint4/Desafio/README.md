# 1. Instruções
O desafio dessa sprint foi dividido em 3 etapas, a `Etapa 1` para o desenvolvimento de um `Dockerfile` para criar um container que iria executar o script python [carguru.py](/Sprint4/Desafio/Etapa1/carguru.py). Em seguida a `Etapa 2` trata-se de apenas um questionamento, e por fim a `Etapa 3` com o desenvolvimento de um script em python, [mascara_dados.py](/Sprint4/Desafio/Etapa3/mascara_dados.py), e um `Dockerfile` para o script.

# 2. Etapa 1

Nesta etapa foi necessário a criação de um [Dockerfile](/Sprint4/Desafio/Etapa1/Dockerfile) para a reunilização conteinerizada do arquivo [carguru.py](/Sprint4/Desafio/Etapa1/carguru.py), e ficou da seguinte forma:
 
``` Dockerfile
FROM python

WORKDIR /app

COPY mascara_dados.py .

CMD ["python", "mascara_dados.py"]
```

Em que, a primeira linha seleciona uma imagem do `docker.hub` que será utilizada no container, neste caso usaremos `python`, em seguida é definido o diretório de trabalho, depois é copiado o arquivo python que sera utilizado no container e, por fim, o comando para executar o script Python com a inicialização do container.

## 2.1 Passos para Execução

Os comandos para criação e execução do container consistem em:

1. **Criação da Imagem**

    O comando `docker build` é utilizado para criar a imagens docker, e a tag `-t` seguida de um nome para nomear a imagem criada, e por fim um `.` para referenciar o arquivo `Dockerfile` que vai ser utilizado.

    ```docker
    docker build -t carguru_image .
    ```

    ![Criação da imagem docker](/Sprint4/Evidencias/Desafio/carguru_image.png)

2. **Criação do Container**

    O comando `docker run` é utilizado para a criar um container novo, `--name` seguido de um nome, para nomear o container novo, em seguida o nome da imagem que sera utilizada no container.

    ```docker
    docker run --name carguru carguru_image
    ```

    ![Criação do Container utilizando a imagem](/Sprint4/Evidencias/Desafio/carguru_container.png)

3. **Execução do Container**

    O comando `docker start` é utilizado para iniciar um container, a tag `-i` mantem o container interativo, podendo assim exibir o conteudo gerado pela sua execução, e por fim o nome do container será iniciado.

    ```docker
    docker start -i carguru
    ```

    ![Execução do container criado](/Sprint4/Evidencias/Desafio/carguru_start.png)

As linhas referenciadas e o arquivo estáo disponiveis em: [Dockerfile](/Sprint4/Desafio/Etapa1/Dockerfile)

# 3. Etapa 2
Consistia em responder e justificar a pergunta:
-  *É possivel reutilizar containers ? Em caso positivo, apresente o comando necessário para reiniciar um dos containers parados em seu ambiente Docker ? Não sendo possível reutilizar, justifique sua resposta.*

Como mostrado nas evidencias das outras etapas, a resposta a essa pergunta é `SIM`, é possivel reutilizar containers.

- ![Reiniciando Containers 1](/Sprint4/Desafio/Etapa2/etapa2.png)
- ![Reiniciando Containers 2](/Sprint4/Evidencias/Desafio/mascara_dados_run.png)
- ![Reiniciando Containers 3](/Sprint4/Evidencias/Desafio/mascara_dados_start.png)

A primeira evidencia trata-se de um container antigo sendo reinicializado, a tag `-a` faz com sejam exibidos os containers que estao desligados. Já a segunda imagem é a criação do container `mascara-dados` e a terceira sua reinicialização.

# 4. Etapa 3

A etapa 3 do desafio consistiu no desenvolvimento de um `Dockerfile` e um `script python`, seguido da criação de uma imagem docker com o Dockerfile, um container e a execução do mesmo. 

## 4.1 Dockerfile

O Dockerfile criado para essa etapa foi similiar ao criado na `Etapa 1`, tendo como resultado:

```Dockerfile
FROM python

WORKDIR /app

COPY mascara_dados.py .

CMD ["python", "mascara_dados.py"]
```

## 4.2 Script Python

O desenvolvimento do script python teve como objetivo criar um código capaz de receber um número indetermidado de entradas (via input) e gerar uma hash da string utilizando o algoritmo `SHA-1` e depois exibir a hash obtida através do metodo `hexdigest`. Teve como resultado o seguinte código:

Inicialmente é feito o importe da biblioteca que vai ser usada pra a conversão das strings para hash.
```python
import hashlib
```

Seguido de um laço infinito contendo o input() para o usuario e um break encerra o laço quando um usuario insere como input `exit()`.
```python
while True:
    # Receber input do usuário
    entrada = input("Digite uma string para mascarar (ou 'exit()' para encerrar): ")
    if entrada.lower() == 'exit()':
        break
```

A string que foi recebida entao convertida em hash, utilizando a função `hashlib.sha1()`, e preparada para ser exibidia com a função `.hexdigest()`
```python
    # Gerar a hash SHA-1
    hash_object = hashlib.sha1(entrada.encode())
    hex_dig = hash_object.hexdigest()

    # Imprimir a hash
    print(f"Hash SHA-1: {hex_dig}")
```

## 4.3 Criação do Container

Os passos para a criação da imagem e do conteiner serão similares com as da Etapa 1, contendo apenas algumas tags diferentes.

1. **Criação da Imagem**

    Este comando sera igual ao da Etapa 1:

    ```docker
    docker build -t mascara_dados-image .
    ```

    ![Criação da imagem docker](/Sprint4/Evidencias/Desafio/mascara_dados_image.png)

2. **Criação do Container**

    Novamente um comando parecido com o da Etapa 1, com o adicional da tag `-it`, que faz com que um terminal interativo do container seja aberto após a execução, permitindo a entrada de dados para o usuario no terminal.

    ```docker
    docker run -it --name mascara-dados mascara_dados_image
    ```

    ![Criação do Container utilizando a imagem](/Sprint4/Evidencias/Desafio/mascara_dados_run.png)

3. **Execução do Container**

    Por fim, esse comando tambem se repete como na Etapa 1.

    ```docker
    docker start -i mascara-dados
    ```

    ![Execução do container criado](/Sprint4/Evidencias/Desafio/mascara_dados_start.png)

As linhas referenciadas e o arquivo estáo disponiveis em: [Dockerfile](/Sprint4/Desafio/Etapa3/Dockerfile) e [mascara_dados.py](/Sprint4/Desafio/Etapa3/mascara_dados.py)