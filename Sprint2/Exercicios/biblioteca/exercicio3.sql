SELECT COUNT(liv.cod) as quantidade, edt.nome, ende.estado, ende.cidade
FROM editora as edt
JOIN livro liv on edt.codeditora = liv.editora
JOIN endereco as ende on edt.endereco = ende.codendereco
GROUP BY edt.nome, ende.estado, ende.cidade
ORDER BY quantidade DESC
LIMIT 5