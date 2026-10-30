-- Lista isoladamente todos os fornecedores cadastrados no sistema.
SELECT
    f.id_fornecedor AS id_fornecedor,
    f.nome AS nome_fornecedor,
    TRIM(f.cnpj) AS cnpj,
    NVL(f.telefone, '-') AS telefone,
    NVL(f.email, '-') AS email
FROM FORNECEDOR f
ORDER BY
    f.id_fornecedor;

