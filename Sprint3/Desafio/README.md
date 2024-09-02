# 1. Instruções
Para a solução do desafio final da sprint foi criado um Notebook utilizando Jupyter como sugerido pelo próprio desafio, armazenado no arquivo `desafio.ipynb`. O ambiente Jupyter foi testado utilizando-se do plug-in disponivel para VsCode [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

Também foi disponibilizado o arquivo [desafio.py](/Sprint3/Desafio/desafio.py) com todos os codigo utilizados agregados e comentados.

Inicialmente é necessario instalar as bibliotecas `pandas`, `matplotlib` e `notebook`

```
pip install pandas matplotlib notebook
```

## 1.1 Carregando o Arquivo e Tratando os Dados

1. **Importação das Bibliotecas**:
    - Inicialmente deve-se importar as bibliotecas que foram instaladas e que foram utilizadas para a resolução:

    ``` py
    import pandas as pd
    import matplotlib.pyplot as plt
    ```

2. **Leitura dos Dados**:
    - Em seguida foi feita a leitura do arquivo contendo os dados que foram manipulados:

    ``` py
    dados = pd.read_csv('googleplaystore.csv')
    dados.head()
    ```

    - O comando `dados.head` nos permite visualizar a forma como os dados estao armazenados no arquivo `.csv`.
![dados_head](/Sprint3/Evidencias/desafio/dados_head.png)

3. **Tratamento dos Dados**:
    - Para garantir que as informações estejam coesas, foi necessario fazer o tratamento dos dados, inicialmente eliminando linhas duplicadas de dados, filtrando os dados de mesmo nome que continham mais `Reviews`.

    ``` py
    dados = dados.sort_values('Reviews', ascending=False).drop_duplicates(subset='App', keep='first')
    ```

    - Seguido do tratamento dos dados em si:
    ``` py
    dados['Installs'] = dados['Installs'].str.replace('+', '').str.replace(',', '')
    dados = dados[dados['Installs'].str.isdigit()]
    dados['Installs'] = dados['Installs'].astype(int)

    dados['Reviews'] = dados['Reviews'].str.replace(',', '')
    dados['Reviews'] = pd.to_numeric(dados['Reviews'], errors='coerce')

    dados['Price'] = dados['Price'].str.replace('$', '').astype(float)
    ```

## 1.2 Grafico de Barras e Grafico de Pizza

1. **Grafico de Barras:**
    - Foi gerado o grafico de barras, selecionando o Top 5 aplicativos com o maior número de instalações:

    ```py
    top5_apps = dados.nlargest(5, 'Installs')

    plt.figure(figsize=(17, 6))
    plt.bar(top5_apps['App'], top5_apps['Installs'], color='skyblue')
    plt.title('Top 5 Apps por Número de Instalação')
    plt.xlabel('App')
    plt.ylabel('Número de Instalações')
    plt.yscale('log')
    plt.show()
    ```
    ![Grafico de Barras](/Sprint3/Evidencias/desafio/grafico_barras.png)

2. **Grafico de Pizza:**
    - Foi gerado o grafico de pizza, mostrando a distribuição das categorias de aplicativos:

    ```py
    category_count = dados['Category'].value_counts()
    plt.figure(figsize=(18, 13))
    plt.pie(category_count, labels=category_count.index, autopct='%1.1f%%', startangle=0)
    plt.title('Distribuição das Categorias de Apps')
    plt.axis('equal')
    plt.show()
    ```
    ![Grafico de Pizza](/Sprint3/Evidencias/desafio/grafico_pizza.png)

## 1.3 Buscas
1. **App Mais Caro**
    - Foi criado uma busca que retorna os dados do App mais caro presente nos dados:

    ```py
    app_mais_caro = dados.loc[dados['Price'].idxmax()]
    app_mais_caro
    ```
    ![App mais caro](/Sprint3/Evidencias/desafio/app_mais_caro.png)

2. **Apps Mature +17**
    - Foi criado uma busca que retorna a quantidade de Apps Mature+17 presentes nos dados:

    ```py
    mature_apps = dados[dados['Content Rating'] == 'Mature 17+'].shape[0]
    print(f"Quantidade de apps classificados como 'Mature 17+': {mature_apps}")
    ```
    ![Quantidade de Apps Mature](/Sprint3/Evidencias/desafio/qtd_apps_mature.png)

3. **Apps com mais Avaliações**
    - Foi criado uma busca que retorna o top 10 apps com maior numero de `Reviews` presentes nos dados:

    ```py
    top10_reviews = dados.nlargest(10, 'Reviews')[['App', 'Reviews']]
    top10_reviews
    ```
    ![Top10 app mais avaliados](/Sprint3/Evidencias/desafio/top10_apps_reviews.png)

    - Para uma melhor visualização e dimensão da diferença entre os apps também foi gerada um gráfico de barras horizontais:
    ```py
    plt.figure(figsize=(15, 6))
    plt.barh(top10_reviews['App'], top10_reviews['Reviews'], color='blue')
    plt.xlabel('Número de Reviews')
    plt.ylabel('Aplicativos')
    plt.title('Top 10 Apps por Número de Reviews')
    plt.gca().invert_yaxis()  # Inverter o eixo y para que o maior valor fique no topo
    plt.xscale('log')
    plt.show()
    ```
    ![Grafico de Barras Horizontais](/Sprint3/Evidencias/desafio/grafico_barrasH.png)

## 1.4 Graficos e Buscas Extras

1. **Total de Apps Pagos**
    - Foi criado uma busca que retorna o total de apps pagos:

    ```py
    total_apps_pago = dados[dados['Type'] == 'Paid'].shape[0]
    print(f"Total de Apps Pagos: {total_apps_pago}")
    ```

    ![total de apps pagos](/Sprint3/Evidencias/desafio/total_apps_pagos.png)

2. **Total de Renda Estimada**
    - Ainda sobre os apps pagos, foi criado também uma busco que exite o total de renda estimada:

    ```py
    dados['Receita_Estimada'] = dados['Installs'] * dados['Price']
    top10_receita = dados[dados['Type'] == 'Paid'].nlargest(10, 'Receita_Estimada')[['App', 'Receita_Estimada', 'Price', 'Installs']]
    top10_receita
    ```

    ![Top 10 apps com maior receita estimada](/Sprint3/Evidencias/desafio/top10_receita.png)
    - E o grafico de barras e linha (dual-axis chart) utilizando os dados acima:
    ![Grafico de barras e linhas do top 10 apps com maior receita estimada](/Sprint3/Evidencias/desafio/dual_axis_chart.png)

3. **Top Apps com mais Reviews por Categoria**
    - E por fim, a última busca extra feita, exibe os apps com o maior numero de reviews por categoria:

    ``` py
    app_top_reviews_categoria = dados.loc[dados.groupby('Category')['Reviews'].idxmax()][['Category', 'App', 'Reviews']]
    app_top_reviews_categoria
    ```

    ![Top apps com mais reviews separados por categoria](/Sprint3/Evidencias/desafio/mais_reviews_por_categoria.png)

    - E o gráfico de linhas gerado apartir desta busca:

    ```py
    plt.figure(figsize=(12, 6))
    plt.plot(top_reviews_categoria['Category'], top_reviews_categoria['Reviews'], marker='o', linestyle='-', color='green')
    plt.xlabel('Categoria')
    plt.ylabel('Número de Reviews')
    plt.title('App com Mais Reviews em Cada Categoria')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.yscale('log')
    plt.show()
    ```

    ![Grafico dos Apps com maior numero de reviews por categoria](/Sprint3/Evidencias/desafio/grafico_apps_reviews_por_categoria.png)