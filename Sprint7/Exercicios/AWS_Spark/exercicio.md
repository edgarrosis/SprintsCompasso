# Exercicio Spark
### Etapa 1: Fazer o pull da imagem `jupyter/all-spark-notebook`
Execute o comando abaixo no terminal para baixar a imagem:

```bash
docker pull jupyter/all-spark-notebook
```

![Jupyter spark Image](/Sprint7/Evidencias/Exercicios/jupyter-spark-image.png)

### Etapa 2: Criar o container com a imagem Spark
Após o pull da imagem, você pode criar e iniciar um container com o Jupyter Lab e o Spark. Utilizando o seguinte comando:

```bash
docker run -it --rm -p 8888:8888 -v C:/Users/edgar/Desktop/Compasso:/home/jovyan/work jupyter/all-spark-notebook
```

![criaçao do container](/Sprint7/Evidencias/Exercicios/criacao-container.png)

Copiando o diretorio do repositorio local, e o copiando como volume para o container. Achei melhor dessa forma, pois o wget nao funcionaria para baixar o README com o repositorio sendo privado.

O `-it` garante o modo interativo e o `-p` faz o mapeamento da porta 8888 do container para a porta 8888 da sua máquina.

Quando o container iniciar, ele exibirá logs, e você verá algo como:

```bash
http://127.0.0.1:8888/lab?token=<token_here>
```

![link gerado pelo container](/Sprint7/Evidencias/Exercicios/link-jupyter-spark.png)

Copie e cole esse link no seu navegador para acessar o Jupyter Lab.

### Etapa 3: Acessar o terminal do Spark
Em um novo terminal, execute o comando `docker exec` para abrir o terminal interativo do Spark no container. O comando seria assim:

```bash
docker exec -it <container_id> /bin/bash
```

Em seguida, inicie o `pyspark`:

```bash
pyspark
```

![Acesso ao terminal](/Sprint7/Evidencias/Exercicios/container-spark.png)

Agora, você está no terminal interativo do Spark, onde pode rodar os comandos para a próxima etapa.

### Etapa 4: Contagem de palavras no arquivo `README.md`
Para contar as palavras no arquivo `README.md` usando o Spark, siga esta sequência de comandos no Spark Shell:

1. **Carregar o arquivo no Spark:**

```bash
text_file = sc.textFile("/home/jovyan/work/README.md")
```

2. **Contar as ocorrências de palavras:**

```python
word_counts = text_file.flatMap(lambda line: line.split(" ")) \
                       .map(lambda word: (word, 1)) \
                       .reduceByKey(lambda a, b: a + b)
```

3. **Exibir os resultados:**

```python
word_counts.collect()
```

![Execuçao do script](/Sprint7/Evidencias/Exercicios/contador-palavras.png)