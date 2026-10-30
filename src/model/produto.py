class Produto:
    def __init__(self,
                 id_produto: int = None,
                 nome: str = None,
                 descricao: str = None,
                 preco_venda: float = None,
                 estoque_atual: int = None,
                 estoque_minimo: int = None):
        self.set_id_produto(id_produto)
        self.set_nome(nome)
        self.set_descricao(descricao)
        self.set_preco_venda(preco_venda)
        self.set_estoque_atual(estoque_atual)
        self.set_estoque_minimo(estoque_minimo)

    def get_id_produto(self) -> int:
        return self.id_produto

    def set_id_produto(self, id_produto: int):
        self.id_produto = id_produto

    def get_nome(self) -> str:
        return self.nome

    def set_nome(self, nome: str):
        self.nome = nome

    def get_descricao(self) -> str:
        return self.descricao

    def set_descricao(self, descricao: str):
        self.descricao = descricao

    def get_preco_venda(self) -> float:
        return self.preco_venda

    def set_preco_venda(self, preco_venda: float):
        self.preco_venda = preco_venda

    def get_estoque_atual(self) -> int:
        return self.estoque_atual

    def set_estoque_atual(self, estoque_atual: int):
        self.estoque_atual = estoque_atual

    def get_estoque_minimo(self) -> int:
        return self.estoque_minimo

    def set_estoque_minimo(self, estoque_minimo: int):
        self.estoque_minimo = estoque_minimo

    def to_string(self) -> str:
        preco_fmt = f"{float(self.get_preco_venda()):.2f}" if self.get_preco_venda() is not None else "0.00"
        desc_fmt = self.get_descricao() if self.get_descricao() else "-"
        return (
            f"ID: {self.get_id_produto()} | "
            f"Nome: {self.get_nome()} | "
            f"Descrição: {desc_fmt} | "
            f"Preço Venda: R$ {preco_fmt} | "
            f"Estoque Atual: {self.get_estoque_atual()} | "
            f"Estoque Mínimo: {self.get_estoque_minimo()}"
        )
