-- Lista os produtos cujo estoque atual está menor ou igual ao estoque mínimo de segurança.
SELECT
    p.id_produto AS id_produto,
    p.nome AS nome_produto,
    p.estoque_atual AS estoque_atual,
    p.estoque_minimo AS estoque_minimo,
    (p.estoque_minimo - p.estoque_atual) AS deficit_reposicao,
    p.preco_venda AS preco_venda
FROM PRODUTO p
WHERE p.estoque_atual <= p.estoque_minimo
ORDER BY
    deficit_reposicao DESC,
    p.nome
