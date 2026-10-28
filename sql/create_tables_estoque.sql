-- Remove relacionamentos e tabelas caso ja existam
DROP TABLE ITEM_COMPRA CASCADE CONSTRAINTS;
DROP TABLE COMPRA CASCADE CONSTRAINTS;
DROP TABLE PRODUTO CASCADE CONSTRAINTS;
DROP TABLE FORNECEDOR CASCADE CONSTRAINTS;

-- Remove sequences caso ja existam
DROP SEQUENCE SEQ_FORNECEDOR;
DROP SEQUENCE SEQ_PRODUTO;
DROP SEQUENCE SEQ_COMPRA;
DROP SEQUENCE SEQ_ITEM_COMPRA;

-- Criacao das sequences para controle das chaves primarias (PK)
CREATE SEQUENCE SEQ_FORNECEDOR START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_PRODUTO START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_COMPRA START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_ITEM_COMPRA START WITH 1 INCREMENT BY 1 NOCACHE;

-- 1. Tabela FORNECEDOR
CREATE TABLE FORNECEDOR (
    id_fornecedor NUMBER        NOT NULL,
    nome          VARCHAR2(120) NOT NULL,
    cnpj          CHAR(14)      NOT NULL,
    telefone      VARCHAR2(20),
    email         VARCHAR2(120),
    CONSTRAINT pk_fornecedor PRIMARY KEY (id_fornecedor),
    CONSTRAINT uq_fornecedor_cnpj UNIQUE (cnpj)
);

-- 2. Tabela PRODUTO
CREATE TABLE PRODUTO (
    id_produto     NUMBER        NOT NULL,
    nome           VARCHAR2(120) NOT NULL,
    descricao      VARCHAR2(255),
    preco_venda    NUMBER(10,2)  NOT NULL,
    estoque_atual  NUMBER        NOT NULL,
    estoque_minimo NUMBER        NOT NULL,
    CONSTRAINT pk_produto PRIMARY KEY (id_produto)
);

-- 3. Tabela COMPRA
CREATE TABLE COMPRA (
    id_compra     NUMBER       NOT NULL,
    id_fornecedor NUMBER       NOT NULL,
    data_compra   DATE         NOT NULL,
    status        VARCHAR2(12) NOT NULL,
    CONSTRAINT pk_compra PRIMARY KEY (id_compra),
    CONSTRAINT fk_compra_fornecedor FOREIGN KEY (id_fornecedor)
        REFERENCES FORNECEDOR (id_fornecedor)
);

-- 4. Tabela ITEM_COMPRA
CREATE TABLE ITEM_COMPRA (
    id_item        NUMBER       NOT NULL,
    id_compra      NUMBER       NOT NULL,
    id_produto     NUMBER       NOT NULL,
    quantidade     NUMBER       NOT NULL,
    preco_unitario NUMBER(10,2) NOT NULL,
    CONSTRAINT pk_item_compra PRIMARY KEY (id_item),
    CONSTRAINT fk_item_compra FOREIGN KEY (id_compra)
        REFERENCES COMPRA (id_compra),
    CONSTRAINT fk_item_produto FOREIGN KEY (id_produto)
        REFERENCES PRODUTO (id_produto)
);

