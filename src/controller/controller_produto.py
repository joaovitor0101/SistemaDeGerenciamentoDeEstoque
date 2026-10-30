"""Operações CRUD da entidade Produto com validação e integridade referencial."""
from controller.controller_compra import executar, existe, inteiro_nao_negativo, inteiro_positivo
from controller.controller_item_compra import validar_decimal_positivo
from model.produto import Produto


class ControllerProduto:
    def __init__(self, banco=None, conexao=None):
        banco_efetivo = banco if banco is not None else conexao
        if banco_efetivo is None:
            from conexion.oracle_queries import ConexaoOracle
            banco_efetivo = ConexaoOracle(permite_escrita=True)
        self.banco = banco_efetivo

    def existe(self, id_produto: int) -> bool:
        return existe(self.banco, "PRODUTO", "id_produto", id_produto)

    @staticmethod
    def _validar(produto: Produto) -> dict:
        if not isinstance(produto, Produto):
            raise ValueError("Informe um objeto Produto.")
        nome = (produto.get_nome() or "").strip()
        if not nome or len(nome) > 120:
            raise ValueError("O nome do produto deve ter entre 1 e 120 caracteres.")
        descricao = (produto.get_descricao() or "").strip() or None
        if descricao and len(descricao) > 255:
            raise ValueError("A descricao do produto deve ter no maximo 255 caracteres.")
        preco = validar_decimal_positivo(produto.get_preco_venda(), "Preco de venda")
        atual = inteiro_nao_negativo(produto.get_estoque_atual(), "Estoque atual")
        minimo = inteiro_nao_negativo(produto.get_estoque_minimo(), "Estoque minimo")
        return {
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "atual": atual,
            "minimo": minimo,
        }

    @staticmethod
    def _objeto(linha) -> Produto:
        id_p, nome, descricao, preco, atual, minimo = linha
        return Produto(id_p, nome, descricao, float(preco), atual, minimo)

    def inserir(self, produto: Produto) -> Produto:
        parametros = self._validar(produto)
        if produto.get_id_produto() is not None:
            raise ValueError("Um novo produto deve ter id_produto=None.")
        codigo = self.banco.obter_proximo_id("SEQ_PRODUTO")
        parametros["id"] = codigo
        executar(
            self.banco,
            """INSERT INTO PRODUTO (id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo)
               VALUES (:id, :nome, :descricao, :preco, :atual, :minimo)""",
            parametros,
            escrita=True,
        )
        produto.set_id_produto(codigo)
        return self.buscar(codigo)

    def listar(self) -> list:
        linhas = executar(
            self.banco,
            "SELECT id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo "
            "FROM PRODUTO ORDER BY id_produto",
        )
        return [self._objeto(linha) for linha in linhas]

    def buscar(self, id_produto: int):
        inteiro_positivo(id_produto, "Produto")
        linha = executar(
            self.banco,
            "SELECT id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo "
            "FROM PRODUTO WHERE id_produto = :id",
            {"id": id_produto},
            unico=True,
        )
        return self._objeto(linha) if linha else None

    def atualizar(self, produto: Produto) -> Produto:
        parametros = self._validar(produto)
        codigo = inteiro_positivo(produto.get_id_produto(), "Produto")
        parametros["id"] = codigo
        quantidade = executar(
            self.banco,
            """UPDATE PRODUTO
               SET nome = :nome, descricao = :descricao, preco_venda = :preco,
                   estoque_atual = :atual, estoque_minimo = :minimo
               WHERE id_produto = :id""",
            parametros,
            escrita=True,
        )
        if quantidade == 0:
            raise ValueError("Produto nao encontrado.")
        return self.buscar(codigo)

    def excluir(self, id_produto: int) -> bool:
        inteiro_positivo(id_produto, "Produto")
        if not self.existe(id_produto):
            raise ValueError("Produto nao encontrado.")
        item_filho = executar(
            self.banco,
            "SELECT id_item FROM ITEM_COMPRA WHERE id_produto = :id",
            {"id": id_produto},
            unico=True,
        )
        if item_filho:
            raise ValueError("Produto possui itens de compra vinculados. Exclua os itens antes de remover o produto.")
        quantidade = executar(
            self.banco,
            "DELETE FROM PRODUTO WHERE id_produto = :id",
            {"id": id_produto},
            escrita=True,
        )
        if quantidade == 0:
            raise ValueError("Produto nao encontrado.")
        return True
