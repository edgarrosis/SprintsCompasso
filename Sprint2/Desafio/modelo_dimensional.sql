-- DIMENSIONAL
-- dimensao de tempo (utilizando o banco postgres)
create view dimensao_tempo as
select distinct
	dataLocacao as data,
	EXTRACT(year from dataLocacao) as ano,
	EXTRACT(month from dataLocacao) as mes,
	EXTRACT(day from dataLocacao) as dia,
	EXTRACT(week from dataLocacao) as semana,
	horaLocacao as hora
from locacao
union
select distinct
	dataEntrega as data,
	EXTRACT(year from dataEntrega) as ano,
	EXTRACT(month from dataEntrega) as mes,
	EXTRACT(day from dataEntrega) as dia,
	EXTRACT(week from dataEntrega) as semana,
	horaEntrega as hora
from locacao
order by data asc

-- dimensao de tempo (utilizando sqlite)
create view dimensao_tempo as
select distinct
	dataLocacao as data,
	STRFTIME('%Y', dataLocacao) AS Ano,
    STRFTIME('%m', dataLocacao) AS Mes,
    STRFTIME('%d', dataLocacao) AS Dia,
    STRFTIME('%W', dataLocacao) AS Semana,
	horaLocacao as hora
from locacao
union
select distinct
	dataEntrega as data,
	STRFTIME('%Y', dataEntrega) AS Ano,
    STRFTIME('%m', dataEntrega) AS Mes,
    STRFTIME('%d', dataEntrega) AS Dia,
    STRFTIME('%W', dataEntrega) AS Semana,
	horaEntrega as hora
from locacao
order by data asc


-- dimensao cliente
create view dimensao_cliente as
select idcliente as codigo,
	nomecliente as nome,
	cidadecliente as cidade,
	estadocliente as estado,
	paiscliente as pais
from cliente

-- dimensao vendedor
create view dimensao_vendedor as
select idvendedor as codigo,
	nomevendedor as nome, 
	sexovendedor as sexo,
	estadovendedor as estado
from vendedor l

-- dimensao carro
create view dimensao_carro as
	WITH ultima_quilometragem AS (
    SELECT 
        id_carrokm_fk,
        MAX(kmcarro) AS kmcarro
    FROM 
        quilometragem
    GROUP BY 
        id_carrokm_fk
)
select c.idcarro as codigo,
	q.kmcarro as quilometragem,
	c.classicarro as classificacao,
	c.marcacarro as marca,
	c.modelocarro as modelo,
	c.anocarro as ano,
	cb.tipocombustivel as tipoCombustivel
from carro c
join combustivel cb on id_combustivelfk = idcombustivel
join ultima_quilometragem q on id_carrokm_fk = idcarro
order by codigo ASC

-- fato locacao
create view fato_locacao as
select idLocacao as codigo,
	dataLocacao,
	horaLocacao,
	qtdDiaria as QuantidadeDiaria,
	vlrDiaria as ValorDiaria,
	dataEntrega,
	horaEntrega,
	id_clientefk as codigoCliente,
	id_carrofk as codigoCarro,
	id_vendedorfk as codigoVendedor
from locacao l