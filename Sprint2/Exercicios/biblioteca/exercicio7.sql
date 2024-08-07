SELECT aut.nome
FROM autor as aut
WHERE NOT EXISTS 
	(SELECT liv.cod
	FROM livro as liv
	WHERE aut.codautor = liv.autor)