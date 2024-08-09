CREATE VIEW EditorasMaisLivros as
SELECT e.codeditora as CodEditora,
	e.nome as NomeEditora,
	COUNT(l.cod) as QuantidadeLivros
FROM editora as e
LEFT JOIN livro as l on l.editora = e.codeditora
GROUP BY codeditora
ORDER BY QuantidadeLivros DESC
limit 5