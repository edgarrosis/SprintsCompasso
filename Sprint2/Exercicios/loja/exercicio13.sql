with total_vendas as (
	select SUM(qtd) as quantidade_vendas, cdpro, nmpro, nmcanalvendas
	from tbvendas
	where status = 'Concluído'
	group by cdpro, nmcanalvendas
	order by quantidade_vendas ASC
	LIMIT 10)

select cdpro, nmcanalvendas, nmpro, quantidade_vendas
from total_vendas
