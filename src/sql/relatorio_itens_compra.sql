
-- Detalha cada item associado a uma compra, com fornecedor e produto.
SELECT
    c.id_compra AS id_compra,
    c.data_compra AS data_compra,
    f.nome AS nome_fornecedor,
    p.nome AS nome_produto,
    ic.quantidade AS quantidade_comprada,
    ic.preco_unitario AS preco_unitario,
    ic.quantidade * ic.preco_unitario AS valor_total_item
FROM COMPRA c
JOIN FORNECEDOR f
    ON f.id_fornecedor = c.id_fornecedor
JOIN ITEM_COMPRA ic
    ON ic.id_compra = c.id_compra
JOIN PRODUTO p
    ON p.id_produto = ic.id_produto
ORDER BY
    c.id_compra,
    p.id_produto,
    ic.id_item;
