class Fornecedor:
    def __init__(self,
                 id_fornecedor: int = None,
                 nome: str = None,
                 cnpj: str = None,
                 telefone: str = None,
                 email: str = None):
        self.set_id_fornecedor(id_fornecedor)
        self.set_nome(nome)
        self.set_cnpj(cnpj)
        self.set_telefone(telefone)
        self.set_email(email)

    def get_id_fornecedor(self) -> int:
        return self.id_fornecedor

    def set_id_fornecedor(self, id_fornecedor: int):
        self.id_fornecedor = id_fornecedor

    def get_nome(self) -> str:
        return self.nome

    def set_nome(self, nome: str):
        self.nome = nome

    def get_cnpj(self) -> str:
        return self.cnpj

    def set_cnpj(self, cnpj: str):
        self.cnpj = cnpj

    def get_telefone(self) -> str:
        return self.telefone

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def get_email(self) -> str:
        return self.email

    def set_email(self, email: str):
        self.email = email

    def to_string(self) -> str:
        return (
            f"ID: {self.get_id_fornecedor()} | "
            f"Nome: {self.get_nome()} | "
            f"CNPJ: {self.get_cnpj()} | "
            f"Telefone: {self.get_telefone()} | "
            f"Email: {self.get_email()}"
        )
