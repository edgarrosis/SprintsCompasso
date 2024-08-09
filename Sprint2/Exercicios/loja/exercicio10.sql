with total_vendas as (
	select SUM(qtd * vrunt) as valor_total_vendas, cdvdd
	from tbvendas
	where status = 'Concluído'
	group by cdvdd)

select v1.nmvdd as vendedor, v2.valor_total_vendas, round((v2.valor_total_vendas * v1.perccomissao) / 100, 2) as comissao
from tbvendedor as v1
join total_vendas as v2 on v1.cdvdd = v2.cdvdd
order by comissao desc