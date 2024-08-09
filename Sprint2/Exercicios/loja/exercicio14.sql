with total_vendas as (
	select avg(qtd * vrunt) as gastomedio, estado
	from tbvendas
	where status = 'Concluído'
	group by estado
	order by gastomedio DESC)

select estado, ROUND(gastomedio, 2) as gastomedio
from total_vendas
