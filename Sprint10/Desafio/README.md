# 1. Introdução

Este projeto implementa a Etapa 5 e ultima do desafio, consistindo na crição do dashboard usando o QuickSight e os dados da camada Refined do bucket S3, exibindo de forma visual o tema abordado para a analise, o tema da analise esta disponivel no [README da Sprint 6](/Sprint6/README.md). O objetivo é realizar a analise final utilizando todos os dados coletados e tratados ao longo das ultimas 5 sprints.

Antes de continuar com a execução desta ultima etapa, foi necessario utilizar o script [budget_revenue.py](/Sprint10/Desafio/Etapa5/budget_revenue.py) e refazer a camada Trusted, complementando o dataframe com dados de custos e arrecadação dos filmes que serão necessarios para a analise da etapa final do desafio.

# 2. Estrutura do Projeto

O projeto final completo está organizado da seguinte forma:

- Scripts AWS Glue e AWS Lambda para coletar, processar e tratar dados de filmes, criando as camadas Raw, Trusted e Refined.
- Crawlers para detectar e catalogar automaticamente os dados no Glue Data Catalog.
- Armazenamento dos dados processados na camada Refined do bucket S3.

![bucket_final](/Sprint10/Evidencias/bucket_final.png)

# 3. Configuração do Projeto

## 3.1 Serviços Utilizados:

1. **AWS IAM**: Configurado com permissões para acessar o bucket S3 e executar os jobs do Glue e Lambda.
2. **AWS Lambda**: Configurado com bibliotecas utilizadas para complementar os dados do `.csv`, utilizando a API de filmes do TMDB
3. **AWS Glue**: Configurado com os scripts e crawlers necessários para processar e tratar os dados.
4. **Bucket S3**: Configurado para armazenar os dados coletados e os scripts utilizados no Glue.

# 4. Dashboard

## 4.1. Total de Filmes para cada Gênero

Este gráfico apresenta a quantidade total de filmes nos gêneros **Crime** e **Guerra**. Ele destaca a proporção entre os dois gêneros, fornecendo um panorama inicial sobre a representação de cada um na base de dados utilizada.

- **Dados**: Quantidade total de filmes em cada gênero.
- **Insight**: Permite identificar qual gênero tem maior produção.

![Gráfico 1](/Sprint10/Evidencias/grafico1.png)

## 4.2. Total de Filmes por País - Top 5

Este gráfico lista os cinco países com maior produção de filmes nos gêneros **Crime** e **Guerra**. Ele demonstra a contribuição dos países líderes em produção cinematográfica para esses gêneros.

- **Dados**: Quantidade de filmes por gênero para os cinco principais países.
- **Insight**: Identifica os países mais ativos na produção cinematográfica desses gêneros.

![Gráfico 2](/Sprint10/Evidencias/grafico2.png)

## 4.3. Percentual dos Filmes por Gênero para cada País

Este gráfico explora a distribuição percentual dos filmes de cada gênero por país. Ele permite visualizar como cada país se especializa ou diversifica na produção dos gêneros analisados.

- **Dados**: Proporção percentual de filmes de Crime e Guerra em relação ao total de filmes por país.
- **Insight**: Ajuda a compreender a preferência ou especialização de cada país nos gêneros analisados.

![Gráfico 3](/Sprint10/Evidencias/grafico3.png)

## 4.4. Relação entre a Popularidade dos Filmes de Cada País e sua Nota Média por Gênero - Top 5

Este gráfico combina a popularidade e as avaliações médias dos filmes por país. Ele analisa como esses dois fatores se relacionam nos gêneros Crime e Guerra.

- **Dados**: Popularidade e média de ratings por gênero e país.
- **Insight**: Destaca quais países têm filmes populares, mas que não são os melhores avaliados.

![Gráfico 4](/Sprint10/Evidencias/grafico4.png)

## 4.5. Relação entre a Popularidade dos Filmes de Cada País e seu Lucro - Top 5

Neste gráfico, a popularidade dos filmes é comparada com o lucro gerado, destacando os cinco países mais lucrativos. Ele avalia o impacto econômico da popularidade sobre os resultados financeiros dos filmes.

- **Dados**: Popularidade e lucro total por país.
- **Insight**: Identifica se a popularidade está diretamente associada ao desempenho financeiro.

![Gráfico 5](/Sprint10/Evidencias/grafico5.png)

## 4.6 Relação entre a Nota Média dos Filmes de Cada País e seu Lucro - Top 5
Neste gráfico, é analisada a relação entre a nota média dos filmes e o lucro total obtido por país, considerando os cinco países com maior nota média. A análise fornece uma perspectiva sobre como a qualidade percebida (refletida nas notas médias) se relaciona com os resultados financeiros nos gêneros Crime e Guerra.

- **Dados**: Nota Média e lucro total por país.
- **Insight**: Contraste do lucro dos países com filmes mais bem avaliados com o lucro dos dados do gráfico anterior.

![Gráfico 6](/Sprint10/Evidencias/grafico6.png)

## Conclusões

Através dos dashboards, é possível identificar padrões de produção e recepção dos filmes nos gêneros Crime e Guerra, fornecendo insights sobre a contribuição de cada país, preferências do público e a relação entre popularidade e impacto econômico. Esses resultados sáo úteis para entender tendências globais e regionais no cinema, assim como fatores influenciam nesses lucros, como a presença de mercado e o número total de filmes produzido.
