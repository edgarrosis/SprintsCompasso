CREATE VIEW LivrosCaros as
SELECT l.cod as CodLivro,
	l.titulo as Titulo,
	a.codautor as CodAutor,
	a.nome as NomeAutor,
	l.valor as Valor,
	ed.codeditora as CodEditora,
	ed.nome as NomeEditora
FROM livro as l
JOIN autor as a on a.codautor = l.autor
JOIN editora as ed on ed.codeditora = l.editora
order by valor DESC
limit 10