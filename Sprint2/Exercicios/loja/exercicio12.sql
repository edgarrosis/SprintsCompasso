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
