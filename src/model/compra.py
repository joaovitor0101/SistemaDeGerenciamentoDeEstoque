from datetime import date, datetime
from model.fornecedor import Fornecedor


class Compra:
    def __init__(self,
                 id_compra: int = None,
                 fornecedor: Fornecedor = None,
                 data_compra: date = None,
                 status: str = None):
        self.set_id_compra(id_compra)
        self.set_fornecedor(fornecedor)
        self.set_data_compra(data_compra)
        self.set_status(status)

    def get_id_compra(self) -> int:
        return self.id_compra

    def set_id_compra(self, id_compra: int):
        self.id_compra = id_compra

    def get_fornecedor(self) -> Fornecedor:
        return self.fornecedor

    def set_fornecedor(self, fornecedor: Fornecedor):
        self.fornecedor = fornecedor

    def get_data_compra(self) -> date:
        return self.data_compra

    def set_data_compra(self, data_compra: date):
        self.data_compra = data_compra

    def get_status(self) -> str:
        return self.status

    def set_status(self, status: str):
        self.status = status

    def to_string(self) -> str:
        nome_fornecedor = self.get_fornecedor().get_nome() if self.get_fornecedor() else "N/A"
        data_val = self.get_data_compra()
        data_fmt = data_val.strftime("%d/%m/%Y") if isinstance(data_val, (date, datetime)) else str(data_val)
        return (
            f"ID Compra: {self.get_id_compra()} | "
            f"Fornecedor: {nome_fornecedor} | "
            f"Data: {data_fmt} | "
            f"Status: {self.get_status()}"
        )
