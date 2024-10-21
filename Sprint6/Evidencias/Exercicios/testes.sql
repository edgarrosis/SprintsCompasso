WITH nomes_por_decada AS (
    SELECT
        nome,
        SUM(total) AS total_por_nome,
        CAST((ano / 10) * 10 AS VARCHAR) AS decada
    FROM meubanco.nomes
    WHERE ano >= 1950
    GROUP BY nome, (ano / 10) * 10
),
ranking_por_decada AS (
    SELECT
        decada,
        nome,
        total_por_nome,
        ROW_NUMBER() OVER (PARTITION BY decada ORDER BY total_por_nome DESC) AS rank
    FROM nomes_por_decada
)
SELECT decada, nome, total_por_nome
FROM ranking_por_decada
WHERE rank <= 3
ORDER BY decada ASC, rank ASC;