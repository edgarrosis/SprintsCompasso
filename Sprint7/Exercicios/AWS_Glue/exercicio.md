# Exercicio Glue
Na primeira etapa, iniciei a configuração do usuário IAM com as permissões necessárias para utilizar o **AWS Glue**. Em seguida, criei uma *role* específica para o AWS Glue, garantindo todas as permissões exigidas. Após essas configurações, criei o banco de dados chamado **"glue-lab"** no Lake Formation e o configurei adequadamente para as próximas operações.

### Configuração do Glue Job

Na segunda etapa, criei um job no AWS Glue usando **Spark**, nomeando-o como **job_aws_glue_lab_4**. Realizei todas as configurações iniciais do job para preparar o ambiente, e então desenvolvi o script conforme os requisitos do exercício:

1. **Leitura do arquivo CSV**  
   O primeiro passo do script foi ler o arquivo `nomes.csv`, previamente carregado no S3. Em seguida, imprimi o schema do DataFrame gerado para garantir que os dados foram carregados corretamente.

2. **Manipulação de Dados**  
   Alterei todos os valores da coluna "nome" para letras maiúsculas, e então imprimi a contagem total de linhas do DataFrame.

3. **Agrupamento e Contagem**  
   O script também agrupou os dados por ano e sexo, contando a quantidade de ocorrências para cada grupo, e organizou o DataFrame de modo que o ano mais recente aparecesse no topo.

4. **Análise de Nomes Mais Frequentes**  
   - Identifiquei o nome feminino com mais registros e o ano correspondente.
   - Fiz o mesmo para o nome masculino mais frequente, com seu respectivo ano.

5. **Resumo Anual de Registros**  
   Calculei o total de registros (femininos e masculinos) para cada ano presente no DataFrame, considerando apenas as primeiras 10 linhas ordenadas de forma crescente pelo ano.

### Gravação dos Dados Processados no S3

Por fim, o script salva o conteúdo do DataFrame, com os nomes em letras maiúsculas, no S3. O destino do arquivo é o caminho **`s3://exercicio.glue/lab-glue/frequencia_nomes`**. Os dados são gravados no formato **JSON** e particionados pelas colunas "sexo" e "ano", como especificado.

O script completo, que inclui as operações mencionadas e exibe as saídas no console do CloudWatch, pode ser acessado [aqui](/Sprint7/Exercicios/AWS_Glue/glue.py).