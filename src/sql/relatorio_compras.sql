-- Lista isoladamente todas as compras registradas no sistema.
SELECT
    c.id_compra AS id_compra,
    c.id_fornecedor AS id_fornecedor,
    f.nome AS nome_fornecedor,
    c.data_compra AS data_compra,
    c.status AS status
FROM COMPRA c
JOIN FORNECEDOR f
    ON f.id_fornecedor = c.id_fornecedor
ORDER BY
    c.id_compra;

