"""CRUD de itens; nao movimenta estoque automaticamente por status de compra."""
from decimal import Decimal, InvalidOperation

from controller.controller_compra import ControllerCompra, executar, existe, inteiro_positivo
from model.item_compra import ItemCompra
from model.compra import Compra
from model.produto import Produto


class ControllerItemCompra:
    def __init__(self, banco=None):
        if banco is None:
            from conexion.oracle_queries import ConexaoOracle
            banco = ConexaoOracle(permite_escrita=True)
        self.banco = banco

    def existe(self, id_item):
        return existe(self.banco, "ITEM_COMPRA", "id_item", id_item)

    def _validar(self, item):
        if not isinstance(item, ItemCompra):
            raise ValueError("Informe um objeto ItemCompra.")
        if not isinstance(item.get_compra(), Compra):
            raise ValueError("O item precisa de um objeto Compra.")
        if not isinstance(item.get_produto(), Produto):
            raise ValueError("O item precisa de um objeto Produto.")
        compra = inteiro_positivo(item.get_compra().get_id_compra(), "Compra")
        produto = inteiro_positivo(item.get_produto().get_id_produto(), "Produto")
        if not existe(self.banco, "COMPRA", "id_compra", compra):
            raise ValueError("Compra nao encontrada.")
        if not existe(self.banco, "PRODUTO", "id_produto", produto):
            raise ValueError("Produto nao encontrado.")
        quantidade = inteiro_positivo(item.get_quantidade(), "Quantidade")
        try:
            if isinstance(item.get_preco_unitario(), bool):
                raise ValueError("Preco invalido.")
            preco = Decimal(str(item.get_preco_unitario()))
            if (not preco.is_finite() or preco <= 0 or preco > Decimal('99999999.99')
                    or preco != preco.quantize(Decimal('0.01'))):
                raise ValueError("Preco deve ser positivo e ter no maximo duas casas decimais.")
        except (InvalidOperation, TypeError, ValueError) as erro:
            raise ValueError("Preco invalido para NUMBER(10,2).") from erro
        return {"compra": compra, "produto": produto,
                "quantidade": quantidade, "preco": preco}

    def inserir(self, item):
        parametros = self._validar(item)
        if item.get_id_item() is not None:
            raise ValueError("Um novo item deve ter id_item=None.")
        codigo = self.banco.obter_proximo_id("SEQ_ITEM_COMPRA")
        parametros["id"] = codigo
        executar(self.banco, """INSERT INTO ITEM_COMPRA
            (id_item, id_compra, id_produto, quantidade, preco_unitario)
            VALUES (:id, :compra, :produto, :quantidade, :preco)""", parametros, escrita=True)
        item.set_id_item(codigo)
        return item

    _SELECT = """SELECT i.id_item, i.id_compra, i.id_produto, i.quantidade,
        i.preco_unitario, p.id_produto, p.nome, p.descricao, p.preco_venda,
        p.estoque_atual, p.estoque_minimo
        FROM ITEM_COMPRA i JOIN PRODUTO p ON p.id_produto = i.id_produto"""

    def _objeto(self, linha):
        compra = ControllerCompra(self.banco).buscar(int(linha[1]))
        produto = Produto(*linha[5:11])
        return ItemCompra(linha[0], compra, produto, linha[3], linha[4])

    def listar(self, id_compra=None):
        sql = self._SELECT
        parametros = {}
        if id_compra is not None:
            inteiro_positivo(id_compra, "Compra")
            sql += " WHERE i.id_compra = :compra"
            parametros["compra"] = id_compra
        linhas = executar(self.banco, sql + " ORDER BY i.id_item", parametros)
        return [self._objeto(linha) for linha in linhas]

    def buscar(self, id_item):
        inteiro_positivo(id_item, "Item")
        linha = executar(self.banco, self._SELECT + " WHERE i.id_item = :id",
                         {"id": id_item}, unico=True)
        return self._objeto(linha) if linha else None

    def atualizar(self, item):
        parametros = self._validar(item)
        codigo = inteiro_positivo(item.get_id_item(), "Item")
        parametros["id"] = codigo
        quantidade = executar(self.banco, """UPDATE ITEM_COMPRA SET
            id_compra = :compra, id_produto = :produto,
            quantidade = :quantidade, preco_unitario = :preco
            WHERE id_item = :id""", parametros, escrita=True)
        if quantidade == 0:
            raise ValueError("Item de compra nao encontrado.")
        return self.buscar(codigo)

    def excluir(self, id_item):
        inteiro_positivo(id_item, "Item")
        quantidade = executar(self.banco,
            "DELETE FROM ITEM_COMPRA WHERE id_item = :id", {"id": id_item}, escrita=True)
        if quantidade == 0:
            raise ValueError("Item de compra nao encontrado.")
        return True
