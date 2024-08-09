select cdcli, nmcli, SUM(qtd * vrunt) as gasto
from tbvendas
where status = 'Concluído'
group by cdcli
order by gasto DESC
limit 1