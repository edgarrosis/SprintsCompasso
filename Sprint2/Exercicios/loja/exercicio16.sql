with total_vendas as (
	select avg(qtd) as gastomedio, estado, nmpro
	from tbvendas
	where status = 'Concluído'
	group by estado, nmpro)

select estado, nmpro, ROUND(gastomedio, 4) as quantidade_media
from total_vendas
order by estado, nmpro