from model.produto import Produto


class ControllerProduto:
    # Controla o produto no banco

    def __init__(self, conexao):
        # Recebe a conexão com o banco
        self.conexao = conexao

    def inserir(self, produto: Produto):
        # Salva o produto no banco
        cursor = self.conexao.cursor()
        id_novo = cursor.var(int)
        cursor.execute(
            """
            INSERT INTO PRODUTO (id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo)
            VALUES (SEQ_PRODUTO.NEXTVAL, :nome, :descricao, :preco, :atual, :minimo)
            RETURNING id_produto INTO :id_novo
            """,
            {
                "nome": produto.get_nome(),
                "descricao": produto.get_descricao(),
                "preco": produto.get_preco_venda(),
                "atual": produto.get_estoque_atual(),
                "minimo": produto.get_estoque_minimo(),
                "id_novo": id_novo,
            },
        )
        self.conexao.commit()
        produto.set_id_produto(id_novo.getvalue()[0])
        cursor.close()

    def listar(self):
        # Traz todos os produtos
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo "
            "FROM PRODUTO ORDER BY nome"
        )
        lista = []
        for id_p, nome, descricao, preco, atual, minimo in cursor.fetchall():
            lista.append(Produto(id_p, nome, descricao, float(preco), atual, minimo))
        cursor.close()
        return lista

    def buscar(self, id_produto: int):
        # Busca um produto pelo id
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo "
            "FROM PRODUTO WHERE id_produto = :id",
            {"id": id_produto},
        )
        linha = cursor.fetchone()
        cursor.close()
        if linha is None:
            return None
        id_p, nome, descricao, preco, atual, minimo = linha
        return Produto(id_p, nome, descricao, float(preco), atual, minimo)

    def atualizar(self, produto: Produto):
        # Altera os dados do produto
        cursor = self.conexao.cursor()
        cursor.execute(
            """
            UPDATE PRODUTO
            SET nome = :nome, descricao = :descricao, preco_venda = :preco,
                estoque_atual = :atual, estoque_minimo = :minimo
            WHERE id_produto = :id
            """,
            {
                "nome": produto.get_nome(),
                "descricao": produto.get_descricao(),
                "preco": produto.get_preco_venda(),
                "atual": produto.get_estoque_atual(),
                "minimo": produto.get_estoque_minimo(),
                "id": produto.get_id_produto(),
            },
        )
        self.conexao.commit()
        cursor.close()

    def excluir(self, id_produto: int):
        # Apaga o produto pelo id
       
        cursor = self.conexao.cursor()
        cursor.execute(
            "DELETE FROM PRODUTO WHERE id_produto = :id",
            {"id": id_produto},
        )
        self.conexao.commit()
        cursor.close()