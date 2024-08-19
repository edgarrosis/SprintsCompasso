# Sprint 02

# 1. Introdução
Esta sprint utlizou a prática com comandos básicos e avançados de busca em bancos de dados relacionais Postgres e sqlite, assim como a normalização até a terceira forma normal, através do curso [SQL para Análise de Dados: Do básico ao avançado](https://compassuol.udemy.com/course/sql-para-analise-de-dados/learn/lecture/30132122#overview). Tambem contou com aprendizado sobre conceitos basicos dos serviços de nuvem e sua aplicação no mercado, com o curso [AWS Skill Builder - AWS Partner: Sales Accreditation](https://explore.skillbuilder.aws/learn/course/13660/AWS%2520Partner%253A%2520Sales%2520Accreditation%2520%28Business%29%2520%28Portuguese%29). 

# 2. Resolução do Desafio
A resolução do desafio final da sprint foi iniciada no dia 12/08/2024 até o dia 15/08/2024 com o desenvolvimento dos `modelos relacional e entidade-relacionamento` pós normalização e o `modelo dimensional`.

Seu desenvolvimento e normalização estão detalhados em [README](/Sprint2/Desafio/README.md)

# 3. Exercicios
Os exercicios consistiam basicamente na realização de buscas desde as mais simples à buscas mais complexas, utilizando os bancos de dados [biblioteca](/Sprint2/Exercicios/biblioteca/biblioteca.sqlite) e [loja](/Sprint2/Exercicios/loja/loja.sqlite), ambos DB no formato `sqlite`. 

As queries dos exercicios funcionam conforme o esperado, e foi comprovado nas evidencias dos mesmos.

## 3.1 Database Biblioteca
### Exercicio 1
``` sql
SELECT *
FROM livro
WHERE publicacao > '2014-12-31'
ORDER BY cod ASC
```
- [Evidencia 1](/Sprint2/Evidencias/exercicio/exercicio1.png)

### Exercicio 2
``` sql
SELECT titulo, valor
FROM livro
ORDER BY valor DESC
LIMIT 10
```
- [Evidencia 2](/Sprint2/Evidencias/exercicio/exercicio2.png)

### Exercicio 3
``` sql
SELECT COUNT(liv.cod) as quantidade, edt.nome, ende.estado, ende.cidade
FROM editora as edt
JOIN livro liv on edt.codeditora = liv.editora
JOIN endereco as ende on edt.endereco = ende.codendereco
GROUP BY edt.nome, ende.estado, ende.cidade
ORDER BY quantidade DESC
LIMIT 5
```
- [Evidencia 3](/Sprint2/Evidencias/exercicio/exercicio3.png)

### Exercicio 4
``` sql
SELECT aut.nome, aut.codautor, aut.nascimento, COUNT(liv.cod) as quantidade
FROM autor as aut
LEFT JOIN livro as liv on aut.codautor = liv.autor
GROUP BY aut.codautor
ORDER BY aut.nome
```
- [Evidencia 4](/Sprint2/Evidencias/exercicio/exercicio4.png)

### Exercicio 5
``` sql
SELECT DISTINCT aut.nome
FROM autor as aut
JOIN livro AS liv on aut.codautor = liv.autor
JOIN editora as edt on liv.editora = edt.codeditora
JOIN endereco as ende on edt.endereco = ende.codendereco
WHERE ende.estado != 'PARANÁ' AND ende.estado != 'RIO GRANDE DO SUL'
ORDER BY aut.nome ASC
```
- [Evidencia 5](/Sprint2/Evidencias/exercicio/exercicio5.png)

### Exercicio 6
``` sql
SELECT aut.codautor, aut.nome, COUNT(liv.cod) as quantidade_publicacoes
FROM autor as aut
JOIN livro as liv on aut.codautor = liv.autor
GROUP BY aut.codautor
ORDER BY quantidade_publicacoes DESC
LIMIT 1
```
- [Evidencia 6](/Sprint2/Evidencias/exercicio/exercicio6.png)

### Exercicio Exportação de Dados 1
```sql
CREATE VIEW LivrosCaros as
SELECT l.cod as CodLivro,
	l.titulo as Titulo,
	a.codautor as CodAutor,
	a.nome as NomeAutor,
	l.valor as Valor,
	ed.codeditora as CodEditora,
	ed.nome as NomeEditora
FROM livro as l
JOIN autor as a on a.codautor = l.autor
JOIN editora as ed on ed.codeditora = l.editora
order by valor DESC
limit 10
```
- [Evidencia 1 .csv](/Sprint2/Evidencias/exercicio/LivrosCaros.csv)

### Exercicio Exportação de Dados 2
```sql
CREATE VIEW EditorasMaisLivros as
SELECT e.codeditora as CodEditora,
	e.nome as NomeEditora,
	COUNT(l.cod) as QuantidadeLivros
FROM editora as e
LEFT JOIN livro as l on l.editora = e.codeditora
GROUP BY codeditora
ORDER BY QuantidadeLivros DESC
limit 5
```
- [Evidencia 2 .csv](/Sprint2/Evidencias/exercicio/EditorasMaisLivros.csv)

## 3.2 Database Loja
### Exercicio 8
```sql
with contagem_vendas as (
		select count(cdven) as total_vendas, cdvdd
		from tbvendas
		where status = "Concluído"
		group by cdvdd)

select v1.cdvdd, v1.nmvdd
from tbvendedor as v1
left join contagem_vendas as v2 on v1.cdvdd = v2.cdvdd
order by total_vendas DESC
LIMIT 1
```
- [Evidencia 8](/Sprint2/Evidencias/exercicio/exercicio8.png)

### Exercicio 9
```sql
with total_vendas as (
	select count(*) as vendas, cdpro, nmpro
	from tbvendas
	where (dtven > '2014-02-03 00:00:00' AND dtven < '2018-02-02 00:00:00') AND status = 'Concluído'
	group by cdpro
	order by vendas DESC)

select cdpro, nmpro
from total_vendas
LIMIT 1
```
- [Evidencia 9](/Sprint2/Evidencias/exercicio/exercicio9.png)

### Exercicio 10
```sql
with total_vendas as (
	select SUM(qtd * vrunt) as valor_total_vendas, cdvdd
	from tbvendas
	where status = 'Concluído'
	group by cdvdd)

select v1.nmvdd as vendedor, v2.valor_total_vendas, round((v2.valor_total_vendas * v1.perccomissao) / 100, 2) as comissao
from tbvendedor as v1
join total_vendas as v2 on v1.cdvdd = v2.cdvdd
order by comissao desc
```
- [Evidencia 10](/Sprint2/Evidencias/exercicio/exercicio10.png)

### Exercicio 11
```sql
select cdcli, nmcli, SUM(qtd * vrunt) as gasto
from tbvendas
where status = 'Concluído'
group by cdcli
order by gasto DESC
limit 1
```
- [Evidencia 11](/Sprint2/Evidencias/exercicio/exercicio11.png)

### Exercicio 12
```sql
with total_vendas as (
	select SUM(qtd * vrunt) as valor_total_vendas, cdvdd
	from tbvendas
	where status = 'Concluído'
	group by cdvdd
	order by valor_total_vendas ASC
	LIMIT 1)

select vdep.cddep, vdep.nmdep, vdep.dtnasc, valor_total_vendas
from tbvendedor v1
join tbdependente as vdep on v1.cdvdd = vdep.cdvdd
inner join total_vendas as v2 on v1.cdvdd = v2.cdvdd
```
- [Evidencia 12](/Sprint2/Evidencias/exercicio/exercicio12.png)

### Exercicio 13
```sql
with total_vendas as (
	select SUM(qtd) as quantidade_vendas, cdpro, nmpro, nmcanalvendas
	from tbvendas
	where status = 'Concluído'
	group by cdpro, nmcanalvendas
	order by quantidade_vendas ASC
	LIMIT 10)

select cdpro, nmcanalvendas, nmpro, quantidade_vendas
from total_vendas
```
- [Evidencia 13](/Sprint2/Evidencias/exercicio/exercicio13.png)

### Exercicio 14
```sql
with total_vendas as (
	select avg(qtd * vrunt) as gastomedio, estado
	from tbvendas
	where status = 'Concluído'
	group by estado
	order by gastomedio DESC)

select estado, ROUND(gastomedio, 2) as gastomedio
from total_vendas
```
- [Evidencia 14](/Sprint2/Evidencias/exercicio/exercicio14.png)

### Exercicio 15
```sql
select cdven
from tbvendas
where deletado = true
```
- [Evidencia 15](/Sprint2/Evidencias/exercicio/exercicio15.png)

### Exercicio 16
```sql
with total_vendas as (
	select avg(qtd) as gastomedio, estado, nmpro
	from tbvendas
	where status = 'Concluído'
	group by estado, nmpro)

select estado, nmpro, ROUND(gastomedio, 4) as quantidade_media
from total_vendas
order by estado, nmpro
```
- [Evidencia 16](/Sprint2/Evidencias/exercicio/exercicio16.png)

# 4. Resultado Final Desafio
O banco de que foi remodelado e normalizado foi o `concessionaria.sqlite`, continha os dados [dados_locacao](/Sprint2/Evidencias/desafio/DATA/TABELA_ORIGINAL.csv) e estava organizado da seguinte maneira: 
![banco concessionaria](/Sprint2/Evidencias/desafio/tabela_original.png)

Após a normalização o banco teve como resultado final o seguinte modelo relacional e modelo entidade-relacionamento, respectivamente:
```
CLIENTE(idCliente, nomeCliente, cidadeCliente, estadoCliente, paisCliente);
CARRO(idCarro, classiCarro, marcaCarro, modeloCarro, anoCarro, id_combustivelfk);
QUILOMETRAGEM(id_km, kmCarro, id_carrokm_fk);
COMBUSTIVEL(idcombustivel, tipoCombustivel);
LOCACAO(idLocacao, dataLocacao, horaLocacao, qtdDiaria, vlrDiaria, dataEntrega, horaEntrega, id_clientefk, id_vendedorfk, id_carrofk);
VENDEDOR(idVendedor, nomeVendedor, sexoVendedor, estadoVendedor);

FK id_clientefk(LOCACAO) = PK idCliente(CLIENTE);

FK id_vendedorfk(LOCACAO) = PK idVendedor(VENDEDOR);

FK id_carrofk(LOCACAO) = PK idCarro(CARRO);

FK id_carrokm_fk(QUILOMETRAGEM) = PK idCarro(CARRO);

FK id_combustivelfk(CARRO) = PK idcombustivel(COMBUSTIVEL);
```
![MER](/Sprint2/Evidencias/desafio/MER.png)

Com a organização de cada tabela disposta das seguintes formas: 
- [Cliente](/Sprint2/Evidencias/desafio/tab_cliente.png), [dados clientes](/Sprint2/Evidencias/desafio/DATA/CLIENTE.csv);
- [Vendedor](/Sprint2/Evidencias/desafio/tab_vendedor.png), [dados vendedor](/Sprint2/Evidencias/desafio/DATA/VENDEDOR.csv);
- [Carro](/Sprint2/Evidencias/desafio/tab_carro.png), [dados carro](/Sprint2/Evidencias/desafio/DATA/CARRO.csv);
- [Combustivel](/Sprint2/Evidencias/desafio/tab_combustivel.png), [dados combustivel](/Sprint2/Evidencias/desafio/DATA/COMBUSTIVEL.csv);
- [Quilometragem](/Sprint2/Evidencias/desafio/tab_quilometragem.png), [dados quilometragem](/Sprint2/Evidencias/desafio/DATA/QUILOMETRAGEM.csv);
- [Locacao](/Sprint2/Evidencias/desafio/tab_locacao.png), [dados locacao](/Sprint2/Evidencias/desafio/DATA/LOCACAO.csv).

# 5. Certificados
- [Certificado SQL para Análise de Dados: Do básico ao avançado](/Sprint2/Certificados/Certificado_cursoSQL.jpg)
- [Certificado AWS](/Sprint2/Certificados/Certificado_cursoAWS.pdf)
- [Certificado Sprint 2](/Sprint2/Certificados/Certificado_Sprint2.jpg)