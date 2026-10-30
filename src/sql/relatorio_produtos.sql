-- Lista isoladamente todos os produtos cadastrados no estoque.
SELECT
    p.id_produto AS id_produto,
    p.nome AS nome_produto,
    NVL(p.descricao, '-') AS descricao,
    p.preco_venda AS preco_venda,
    p.estoque_atual AS estoque_atual,
    p.estoque_minimo AS estoque_minimo
FROM PRODUTO p
ORDER BY
    p.id_produto;

