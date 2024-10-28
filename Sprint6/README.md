# Sprint 06

# 1. Introdução

Esta sprint incluiu práticas na plataforma AWS por meio de diversos cursos voltados para serviços essenciais de análise de dados e computação na nuvem. Foram explorados conceitos fundamentais de análise com [AWS Analytics Parte 1](https://explore.skillbuilder.aws/learn/course/external/view/elearning/19345/nocoes-basicas-de-analytics-na-aws-parte-1-portugues-fundamentals-of-analytics-on-aws-part-1-portuguese) e [AWS Analytics Parte 2](https://explore.skillbuilder.aws/learn/course/external/view/elearning/19359/fundamentos-de-analytics-na-aws-parte-2-portugues-fundamentals-of-analytics-on-aws-part-2-portuguese), e o uso do [Amazon Athena](https://explore.skillbuilder.aws/learn/course/5838/Introduction%2520to%2520Amazon%2520Athena%2520%28Portuguese%29) para consultas SQL diretamente em dados armazenados no S3. 

Além disso, os cursos abrangeram a criação e gerenciamento de [Data Warehouse](https://explore.skillbuilder.aws/learn/course/6339/Best%2520Practices%2520for%2520Data%2520Warehousing%2520with%2520Amazon%2520Redshift%2520%28Portuguese%29) com [AWS Redshift](https://explore.skillbuilder.aws/learn/course/13655/Amazon%2520Redshift%2520Getting%2520Started), processamento de grandes volumes de dados com [AWS EMR](https://explore.skillbuilder.aws/learn/course/8827/Amazon%2520EMR%2520Getting%2520Started) e [AWS Glue](https://explore.skillbuilder.aws/learn/course/8171/AWS%2520Glue%2520Getting%2520Started), e desenvolvimento de soluções de análises com manipulação dos dados com [AWS Serverless Analytics](https://explore.skillbuilder.aws/learn/course/6256/Serverless%2520Analytics%2520%28Portuguese%29). A sprint foi concluída com a utilização do [Amazon Quicksight](https://explore.skillbuilder.aws/learn/course/14908/Amazon%2520QuickSight%2520-%2520Getting%2520Started) para criação de dashboards interativos e relatórios dinâmicos. 

# 2. Resolução do Desafio
O tema escolhido, utilizando dos gêneros de filmes/série de `Crime e Guerra`, para a criação do DataLake ao final do programa de bolsas foi: `Países e Regiões mais Ativos na Produção de Filmes do Gênero Crime e Guerra`.

O tema faz um comparativo entre a nacionalidade e o número de obras do gênero crime e guerra entre os países e a recepção do público utilizando a nota e a critica com base nos dados obtidos.

A resolução da Etapa 1 do desafio esta documentada em: [README.md](/Sprint6/Desafio/README.md).

# 3. Exercicios
Essa sprint contou com 2 exercicios abordando funcionalidades/serviços da plataforma da AWS:

### 1. **AWS Athena**
- A resolução do exercício contou com a criação de um bucket para armazenar o arquivo .csv [nomes.csv](/Sprint6/Exercicios/AWS_Athena/nomes.csv) e um diretório para armazenar as buscas da query.

- ![Bucket Athena](/Sprint6/Evidencias/Exercicios/exercicio_athena_bucket.png)

- Em seguida foi solicitada uma busca, `3 nomes mais usados em cada década desde o 1950 até hoje`, para testar a a criação do banco de dados e da tabela com o conteudo do arquivo .csv utilizando o Athena. A busca utilizada foi a seguinte: [buscas.sql](/Sprint6/Exercicios/AWS_Athena/busca.sql) e teve como resulado o arquivo [resultado_busca.csv](/Sprint6/Exercicios/AWS_Athena/resultado_busca.csv).

- ![Resultado da Busca](/Sprint6/Evidencias/Exercicios/evidencia_exercicio_athena.png)

### 2. **AWS Lambda**
- A resolução do exercicio contou com a utilização do bucket criado no exercicio anterior, utilizando uma função lambda da aws para fazer a contagem do numero de linhas do arquivo `nomes.csv`, utlizando um  [Dockerfile](/Sprint6/Exercicios/AWS_Lambda/Dockerfile) e um arquivo .zip com as bibliotecas necessarias do python, [minha-camada-pandas.zip](/Sprint6/Exercicios/AWS_Lambda/minha-camada-pandas.zip) 

- ![Resultado script python](/Sprint6/Evidencias/Exercicios/exercicio_aws_lambda.png)

# 4. Resultado Final Desafio
O script para injestão dos dados no bucket do desafio final do programa de bolsa apartir de uma imagem docker correu sem problemas e foi executada com sucesso.

# 5. Certificados
- [Noções Básicas de Analytics na AWS - Parte 1](/Sprint6/Certificados/AWS_analytics_part1.pdf)
- [Noções Básicas de Analytics na AWS - Parte 2](/Sprint6/Certificados/AWS_analytics_part2.pdf)
- [Introduction to Amazon Athena](/Sprint6/Certificados/AWS_Athena_introduction.pdf)
- [Best Practices for Data Warehousing with Amazon Redshift](/Sprint6/Certificados/AWS_data_warehouse.pdf)
- [Amazon ERM Getting Started](/Sprint6/Certificados/AWS_EMR.pdf)
- [Amazon Glue Getting Started](/Sprint6/Certificados/AWS_Glue.pdf)
- [Amazon Redshift Getting Started](/Sprint6/Certificados/AWS_redshift.pdf)
- [Serverless Analytics](/Sprint6/Certificados/AWS_serverless_analytics.pdf)
- [Amazon QuickSight - Getting Started](/Sprint6/Certificados/AWS-quicksight.pdf)
- [Data & Analytics - PB - AWS - Novo - 6/10](/Sprint6/Certificados/sprint6-certificado.jpg)