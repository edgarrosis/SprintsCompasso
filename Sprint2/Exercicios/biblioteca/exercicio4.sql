SELECT aut.nome, aut.codautor, aut.nascimento, COUNT(liv.cod) as quantidade
FROM autor as aut
LEFT JOIN livro as liv on aut.codautor = liv.autor
GROUP BY aut.codautor
ORDER BY aut.nome