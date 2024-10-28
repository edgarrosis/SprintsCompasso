--Consulta SQL para filtrar dados e adicionar classificação e ordem de meses
SELECT 
    *,
    CASE 
        WHEN numero_consultas < 100 THEN 'BAIXA' 
        WHEN numero_consultas >= 100 AND numero_consultas < 200 THEN 'MEDIA'
        ELSE 'ALTA' 
    END AS classificacao,
    SUBSTR(mês, INSTR(mês, '-') + 2) AS mes_somente,
    CASE 
        WHEN mês LIKE '%May%' THEN 1
        WHEN mês LIKE '%June%' THEN 2
        WHEN mês LIKE '%July%' THEN 3
        WHEN mês LIKE '%August%' THEN 4
        WHEN mês LIKE '%September%' THEN 5
        WHEN mês LIKE '%October%' THEN 6
    END AS mes_ordenado,
    CASE 
        WHEN numero_consultas >= 200 THEN 1  -- Alta primeiro
        WHEN numero_consultas >= 100 THEN 2  -- Média em segundo
        ELSE 3                               -- Baixa por último
    END AS ordem_classificacao
FROM df
WHERE mês LIKE '%May%' OR mês LIKE '%June%' OR mês LIKE '%July%' 
    OR mês LIKE '%August%' OR mês LIKE '%September%' OR mês LIKE '%October%'

-----------------------------------------------------------------------------------------
--Consulta para agrupar e ordenar por mês e classificação
SELECT 
    mes_somente, 
    classificacao, 
    SUM(numero_consultas) AS total_consultas
FROM df_filtrado
GROUP BY mes_somente, classificacao
ORDER BY mes_ordenado, ordem_classificacao

-----------------------------------------------------------------------------------------
--Consulta para totalizar consultas por classificação no período
SELECT 
    classificacao, 
    SUM(numero_consultas) AS total_consultas
FROM df_filtrado
GROUP BY classificacao
ORDER BY ordem_classificacao