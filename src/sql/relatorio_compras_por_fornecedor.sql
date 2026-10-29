
-- Resume as compras registradas por fornecedor.
-- O LEFT JOIN preserva fornecedores sem compras e compras ainda sem itens.
-- COUNT(DISTINCT) evita contar a mesma compra uma vez por item.
SELECT
    f.nome AS nome_fornecedor,
    COUNT(DISTINCT c.id_compra) AS quantidade_compras,
    NVL(SUM(ic.quantidade * ic.preco_unitario), 0) AS valor_total_compras
FROM FORNECEDOR f
LEFT JOIN COMPRA c
    ON c.id_fornecedor = f.id_fornecedor
LEFT JOIN ITEM_COMPRA ic
    ON ic.id_compra = c.id_compra
GROUP BY
    f.id_fornecedor,
    f.nome
ORDER BY
    f.nome;
