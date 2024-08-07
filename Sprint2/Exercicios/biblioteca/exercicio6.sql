SELECT aut.codautor, aut.nome, COUNT(liv.cod) as quantidade_publicacoes
FROM autor as aut
JOIN livro as liv on aut.codautor = liv.autor
GROUP BY aut.codautor
ORDER BY quantidade_publicacoes DESC
LIMIT 1