with total_vendas as (
	select count(*) as vendas, cdpro, nmpro
	from tbvendas
	where (dtven > '2014-02-03 00:00:00' AND dtven < '2018-02-02 00:00:00') AND status = 'Concluído'
	group by cdpro
	order by vendas DESC)

select cdpro, nmpro
from total_vendas
LIMIT 1