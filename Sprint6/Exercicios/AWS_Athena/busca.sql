WITH total_nomes_por_decada AS (
	SELECT nome,
		SUM(total) AS total_nomes,
		CAST(FLOOR(ano / 10) * 10 AS VARCHAR) AS decada
	FROM meubanco.nome
	WHERE ano >= 1950
	GROUP BY nome,
		FLOOR(ano / 10) * 10
),
classificacao_por_decada AS (
	SELECT decada,
		nome,
		total_nomes,
		ROW_NUMBER() OVER (
			PARTITION BY decada
			ORDER BY total_nomes DESC
		) AS posicao
	FROM total_nomes_por_decada
)
SELECT decada,
	nome,
	total_nomes
FROM classificacao_por_decada
WHERE posicao <= 3
ORDER BY decada ASC,
	posicao ASC;