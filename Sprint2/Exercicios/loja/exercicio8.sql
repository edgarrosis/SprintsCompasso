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