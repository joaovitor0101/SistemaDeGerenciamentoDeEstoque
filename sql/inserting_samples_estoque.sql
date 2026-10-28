-- Registros iniciais da tabela FORNECEDOR
INSERT INTO FORNECEDOR (id_fornecedor, nome, cnpj, telefone, email)
VALUES (SEQ_FORNECEDOR.NEXTVAL, 'Distribuidora Alfa Ltda', '11222333000101', '2733331001', 'contato@alfa.com.br');

INSERT INTO FORNECEDOR (id_fornecedor, nome, cnpj, telefone, email)
VALUES (SEQ_FORNECEDOR.NEXTVAL, 'Suprimentos Beta S.A.', '44555666000102', '1140028922', 'vendas@beta.com.br');

INSERT INTO FORNECEDOR (id_fornecedor, nome, cnpj, telefone, email)
VALUES (SEQ_FORNECEDOR.NEXTVAL, 'Atacado Gama Comercio', '77888999000103', '2132225050', 'comercial@gama.com.br');

-- Registros iniciais da tabela PRODUTO
INSERT INTO PRODUTO (id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo)
VALUES (SEQ_PRODUTO.NEXTVAL, 'Teclado USB Padrao', 'Teclado ABNT2 com fio', 59.90, 20, 10);

INSERT INTO PRODUTO (id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo)
VALUES (SEQ_PRODUTO.NEXTVAL, 'Mouse Optico', 'Mouse USB 1200 DPI', 35.00, 5, 10);

INSERT INTO PRODUTO (id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo)
VALUES (SEQ_PRODUTO.NEXTVAL, 'Monitor LED 24', 'Monitor Full HD HDMI', 750.00, 8, 5);

INSERT INTO PRODUTO (id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo)
VALUES (SEQ_PRODUTO.NEXTVAL, 'Cabo HDMI 2m', 'Cabo de video alta velocidade', 25.00, 3, 8);

-- Registros iniciais da tabela COMPRA
INSERT INTO COMPRA (id_compra, id_fornecedor, data_compra, status)
VALUES (SEQ_COMPRA.NEXTVAL, 1, TO_DATE('2026-10-10', 'YYYY-MM-DD'), 'CONCLUIDA');

INSERT INTO COMPRA (id_compra, id_fornecedor, data_compra, status)
VALUES (SEQ_COMPRA.NEXTVAL, 2, TO_DATE('2026-10-15', 'YYYY-MM-DD'), 'CONCLUIDA');

INSERT INTO COMPRA (id_compra, id_fornecedor, data_compra, status)
VALUES (SEQ_COMPRA.NEXTVAL, 3, TO_DATE('2026-10-20', 'YYYY-MM-DD'), 'PENDENTE');

-- Registros iniciais da tabela ITEM_COMPRA
INSERT INTO ITEM_COMPRA (id_item, id_compra, id_produto, quantidade, preco_unitario)
VALUES (SEQ_ITEM_COMPRA.NEXTVAL, 1, 1, 20, 35.00);

INSERT INTO ITEM_COMPRA (id_item, id_compra, id_produto, quantidade, preco_unitario)
VALUES (SEQ_ITEM_COMPRA.NEXTVAL, 1, 2, 10, 18.00);

INSERT INTO ITEM_COMPRA (id_item, id_compra, id_produto, quantidade, preco_unitario)
VALUES (SEQ_ITEM_COMPRA.NEXTVAL, 2, 3, 8, 520.00);

INSERT INTO ITEM_COMPRA (id_item, id_compra, id_produto, quantidade, preco_unitario)
VALUES (SEQ_ITEM_COMPRA.NEXTVAL, 3, 4, 15, 12.00);

