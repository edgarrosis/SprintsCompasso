# 1. Instruções
Para a reprodução do que foi feito no Desafio Final, é necessario: ter instalado um banco de dados postgres, por exemplo com o pgAdmin4 ou um banco sqlite, como o DB Browser que foi utlizado em alguns momentos durante a resolução do desafio. 

Entao deve-se carregar o banco de dados com o arquivo `desafio_dump_MR.sql` e executa-lo como uma query em algum banco sqlite ou postgres. 

Ambos modelos entidade-relacionamento foram feitos utilizando o aplicativo `Br Modelo`.

## 1.1 Normalização do Banco de Dados

1. **Primeira Forma Normal (1FN)**:
    - A primeira forma normal exige que cada coluna de uma tabela seja atômica, ou seja, não deve conter múltiplos valores em uma única célula. Além disso, cada registro na tabela deve ser único, e cada campo deve ser único e indivisível.

    - Os dados do banco do desafio, apesar do agrupamento de diversas colunas em uma mesma tabela, inicialmente ja se encontrava na sua primeira forma normal.


2. **Segunda Forma Normal (2FN)**:
    - A segunda forma normal (2NF) exige que a tabela esteja na 1NF e que todas as colunas não-chave dependam inteiramente da chave primária. Isso significa que cada coluna deve ser totalmente dependente da chave primária e não parcialmente dependente. Em outras palavras, uma tabela atinge a 2NF quando não existem dependências parciais entre colunas e chaves primárias compostas.

    - Nesse ponto surgiram a maioria das tabelas, seguindo a segunda forma normal, sendo elas CLIENTE, LOCACAO, CARRO, VENDEDOR e COMBUSTIVEL. Destas tabelas apenas a CARRO ainda sofreria mudanças na terceira forma normal.

3. **Terceira Forma Normal (3FN)**:
    - A terceira forma normal (3NF) exige que a tabela esteja na 2NF e que não existam dependências transitivas de atributos não-chave. Isso significa que nenhuma coluna não-chave pode depender de outra coluna não-chave, além da chave primária.

    - Nesse ponto surgiu apenas mais uma tabela, sendo ela QUILOMETRAGEM.

### Modelo Relacional Final Obitido
Após a normalização obtive a seguinte organização do banco, nos modelos relacional e entidade-relacionamento.

- [Modelo Relacional](/Sprint2/Evidencias/desafio/modelo_relacional.txt)
- Modelo Entidade-Relacional ![MER](/Sprint2/Evidencias/desafio/MER.png)
- Arquivo `.sql` com os comandos para a criação do banco: [desafio_dump.sql](/Sprint2/Desafio/desafio_dump_MR.sql)

## 2.2 Modelo Dimensional

O modelo dimensional foi realizado através de views no banco de dados normalizado, utlizando o star schema, organizado da seguinte forma:
- [Dimensão Cliente](/Sprint2/Evidencias/desafio/VIEWS/dimensao_cliente.csv)
- [Dimensão Tempo](/Sprint2/Evidencias/desafio/VIEWS/dimensao_tempo.csv)
- [Dimensão Vendedor](/Sprint2/Evidencias/desafio/VIEWS/dimensao_vendedor.csv)
- [Dimensão Carro](/Sprint2/Evidencias/desafio/VIEWS/dimensao_carro.csv)
- [Fato Locação](/Sprint2/Evidencias/desafio/VIEWS/fato_locacao.csv)
- [Dump das Views](/Sprint2/Desafio/modelo_dimensional.sql), a view referente a `dimensao_tempo`foi organizada para ser criada em um banco sqlite ou postgres.

O modelo dimensonal final ficou da seguinte forma:
![Modelo Dimensional](/Sprint2/Evidencias/desafio/MER_DIMENSIONAL.png)