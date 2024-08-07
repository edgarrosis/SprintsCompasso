SELECT DISTINCT aut.nome
FROM autor as aut
JOIN livro AS liv on aut.codautor = liv.autor
JOIN editora as edt on liv.editora = edt.codeditora
JOIN endereco as ende on edt.endereco = ende.codendereco
WHERE ende.estado != 'PARANÁ' AND ende.estado != 'RIO GRANDE DO SUL'
ORDER BY aut.nome ASC