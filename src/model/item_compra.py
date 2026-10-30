from model.compra import Compra
from model.produto import Produto


class ItemCompra:
    def __init__(self,
                 id_item: int = None,
                 compra: Compra = None,
                 produto: Produto = None,
                 quantidade: int = None,
                 preco_unitario: float = None):
        self.set_id_item(id_item)
        self.set_compra(compra)
        self.set_produto(produto)
        self.set_quantidade(quantidade)
        self.set_preco_unitario(preco_unitario)

    def get_id_item(self) -> int:
        return self.id_item

    def set_id_item(self, id_item: int):
        self.id_item = id_item

    def get_compra(self) -> Compra:
        return self.compra

    def set_compra(self, compra: Compra):
        self.compra = compra

    def get_produto(self) -> Produto:
        return self.produto

    def set_produto(self, produto: Produto):
        self.produto = produto

    def get_quantidade(self) -> int:
        return self.quantidade

    def set_quantidade(self, quantidade: int):
        self.quantidade = quantidade

    def get_preco_unitario(self) -> float:
        return self.preco_unitario

    def set_preco_unitario(self, preco_unitario: float):
        self.preco_unitario = preco_unitario

    def to_string(self) -> str:
        id_compra = self.get_compra().get_id_compra() if self.get_compra() else "N/A"
        nome_produto = self.get_produto().get_nome() if self.get_produto() else "N/A"
        preco_fmt = f"{float(self.get_preco_unitario()):.2f}" if self.get_preco_unitario() is not None else "0.00"
        return (
            f"ID Item: {self.get_id_item()} | "
            f"ID Compra: {id_compra} | "
            f"Produto: {nome_produto} | "
            f"Quantidade: {self.get_quantidade()} | "
            f"Preço Unitário: R$ {preco_fmt}"
        )
