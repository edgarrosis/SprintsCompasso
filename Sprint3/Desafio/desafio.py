# Importação das bibliotecas
import pandas as pd
import matplotlib.pyplot as plt

# Leitura do arquivo CSV
dados = pd.read_csv('googleplaystore.csv')
dados.head()

# Remoção de linhas duplicadas
dados = dados.sort_values('Reviews', ascending=False).drop_duplicates(subset='App', keep='first')

# Tratamento dos dados
dados['Installs'] = dados['Installs'].str.replace('+', '').str.replace(',', '')
dados = dados[dados['Installs'].str.isdigit()]
dados['Installs'] = dados['Installs'].astype(int)

dados['Reviews'] = dados['Reviews'].str.replace(',', '')
dados['Reviews'] = pd.to_numeric(dados['Reviews'], errors='coerce')

dados['Price'] = dados['Price'].str.replace('$', '').astype(float)

# Grafico de Barras: Seleção do Top 5 Apps por número de Installs
top5_apps = dados.nlargest(5, 'Installs')

plt.figure(figsize=(17, 6))
plt.bar(top5_apps['App'], top5_apps['Installs'], color='skyblue')
plt.title('Top 5 Apps por Número de Instalação')
plt.xlabel('App')
plt.ylabel('Número de Instalações')
plt.yscale('log')
plt.show()

# Grafico de Pizza: Distribuição das categorias de apps
category_count = dados['Category'].value_counts()
plt.figure(figsize=(18, 13))
plt.pie(category_count, labels=category_count.index, autopct='%1.1f%%', startangle=0)
plt.title('Distribuição das Categorias de Apps')
plt.axis('equal')
plt.show()

# Identificação do app mais caro e seus dados
app_mais_caro = dados.loc[dados['Price'].idxmax()]
app_mais_caro

# Contagem dos apps classificados como Mature 17+
mature_apps = dados[dados['Content Rating'] == 'Mature 17+'].shape[0]
print(f"Quantidade de apps classificados como 'Mature 17+': {mature_apps}")

# Seleção do Top 10 apps por numero de reviews
top10_reviews = dados.nlargest(10, 'Reviews')[['App', 'Reviews']]
top10_reviews

# Grafico de Barras Horizontal: utilizando os dados anteriores
plt.figure(figsize=(15, 6))
plt.barh(top10_reviews['App'], top10_reviews['Reviews'], color='blue')
plt.xlabel('Número de Reviews')
plt.ylabel('Aplicativos')
plt.title('Top 10 Apps por Número de Reviews')
plt.gca().invert_yaxis()
plt.xscale('log')
plt.show()

# Buscas e Graficos extras
# Total de apps pagos
total_apps_pago = dados[dados['Type'] == 'Paid'].shape[0]
print(f"Total de Apps Pagos: {total_apps_pago}")

# Top 10 apps com maior receita estimada
dados['Receita_Estimada'] = dados['Installs'] * dados['Price']
top10_receita = dados[dados['Type'] == 'Paid'].nlargest(10, 'Receita_Estimada')[['App', 'Receita_Estimada', 'Price', 'Installs']]
top10_receita

# Grafico de Barras e Linha: utilizando os dados de receita estimada
fig, ax1 = plt.subplots(figsize=(12, 6))

# Gráfico de barras para a Receita Estimada
ax1.bar(top10_receita['App'], top10_receita['Receita_Estimada'], color='teal')
ax1.set_xlabel('Aplicativo')
ax1.set_ylabel('Receita Estimada (USD)', color='teal')
ax1.tick_params(axis='y', labelcolor='teal')

# Configurar o eixo X com os nomes dos aplicativos
ax1.set_xticklabels(top10_receita['App'], rotation=45, ha='right')

# Criar um segundo eixo Y para o número de instalações
ax2 = ax1.twinx()
ax2.plot(top10_receita['App'], top10_receita['Installs'], color='brown', marker='o', linestyle='-', linewidth=2)
ax2.set_ylabel('Número de Instalações', color='brown')
ax2.tick_params(axis='y', labelcolor='brown')

plt.title('Receita Estimada e Número de Instalações dos Top 10 Aplicativos Pagos')
plt.show()

# App com maior numero de reviews por categoria
top_reviews_categoria = dados.loc[dados.groupby('Category')['Reviews'].idxmax()][['Category', 'App', 'Reviews']]
top_reviews_categoria

# Grafico de Linha: seleção dos apps com mais reviews por categoria
plt.figure(figsize=(12, 6))
plt.plot(top_reviews_categoria['Category'], top_reviews_categoria['Reviews'], marker='o', linestyle='-', color='green')
plt.xlabel('Categoria')
plt.ylabel('Número de Reviews')
plt.title('App com Mais Reviews em Cada Categoria')
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle='--', alpha=0.6)
plt.yscale('log')
plt.show()