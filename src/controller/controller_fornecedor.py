"""Operações CRUD da entidade Fornecedor com validação e integridade referencial."""
from controller.controller_compra import executar, existe, inteiro_positivo
from model.fornecedor import Fornecedor


class ControllerFornecedor:
    def __init__(self, banco=None, conexao=None):
        banco_efetivo = banco if banco is not None else conexao
        if banco_efetivo is None:
            from conexion.oracle_queries import ConexaoOracle
            banco_efetivo = ConexaoOracle(permite_escrita=True)
        self.banco = banco_efetivo

    def existe(self, id_fornecedor: int) -> bool:
        return existe(self.banco, "FORNECEDOR", "id_fornecedor", id_fornecedor)

    @staticmethod
    def _validar(fornecedor: Fornecedor) -> dict:
        if not isinstance(fornecedor, Fornecedor):
            raise ValueError("Informe um objeto Fornecedor.")
        nome = (fornecedor.get_nome() or "").strip()
        if not nome or len(nome) > 120:
            raise ValueError("O nome do fornecedor deve ter entre 1 e 120 caracteres.")
        cnpj = (fornecedor.get_cnpj() or "").strip()
        if not cnpj or len(cnpj) > 14:
            raise ValueError("O CNPJ deve ser informado com até 14 caracteres.")
        telefone = (fornecedor.get_telefone() or "").strip() or None
        if telefone and len(telefone) > 20:
            raise ValueError("O telefone deve ter no máximo 20 caracteres.")
        email = (fornecedor.get_email() or "").strip() or None
        if email and len(email) > 120:
            raise ValueError("O email deve ter no máximo 120 caracteres.")
        return {
            "nome": nome,
            "cnpj": cnpj,
            "telefone": telefone,
            "email": email,
        }

    @staticmethod
    def _objeto(linha) -> Fornecedor:
        id_f, nome, cnpj, telefone, email = linha
        return Fornecedor(id_f, nome, cnpj.strip() if cnpj else cnpj, telefone, email)

    def inserir(self, fornecedor: Fornecedor) -> Fornecedor:
        parametros = self._validar(fornecedor)
        if fornecedor.get_id_fornecedor() is not None:
            raise ValueError("Um novo fornecedor deve ter id_fornecedor=None.")
        codigo = self.banco.obter_proximo_id("SEQ_FORNECEDOR")
        parametros["id"] = codigo
        executar(
            self.banco,
            """INSERT INTO FORNECEDOR (id_fornecedor, nome, cnpj, telefone, email)
               VALUES (:id, :nome, :cnpj, :telefone, :email)""",
            parametros,
            escrita=True,
        )
        fornecedor.set_id_fornecedor(codigo)
        return self.buscar(codigo)

    def listar(self) -> list:
        linhas = executar(
            self.banco,
            "SELECT id_fornecedor, nome, cnpj, telefone, email FROM FORNECEDOR ORDER BY id_fornecedor",
        )
        return [self._objeto(linha) for linha in linhas]

    def buscar(self, id_fornecedor: int):
        inteiro_positivo(id_fornecedor, "Fornecedor")
        linha = executar(
            self.banco,
            "SELECT id_fornecedor, nome, cnpj, telefone, email FROM FORNECEDOR WHERE id_fornecedor = :id",
            {"id": id_fornecedor},
            unico=True,
        )
        return self._objeto(linha) if linha else None

    def atualizar(self, fornecedor: Fornecedor) -> Fornecedor:
        parametros = self._validar(fornecedor)
        codigo = inteiro_positivo(fornecedor.get_id_fornecedor(), "Fornecedor")
        parametros["id"] = codigo
        quantidade = executar(
            self.banco,
            """UPDATE FORNECEDOR
               SET nome = :nome, cnpj = :cnpj, telefone = :telefone, email = :email
               WHERE id_fornecedor = :id""",
            parametros,
            escrita=True,
        )
        if quantidade == 0:
            raise ValueError("Fornecedor nao encontrado.")
        return self.buscar(codigo)

    def excluir(self, id_fornecedor: int) -> bool:
        inteiro_positivo(id_fornecedor, "Fornecedor")
        if not self.existe(id_fornecedor):
            raise ValueError("Fornecedor nao encontrado.")
        compra_filha = executar(
            self.banco,
            "SELECT id_compra FROM COMPRA WHERE id_fornecedor = :id",
            {"id": id_fornecedor},
            unico=True,
        )
        if compra_filha:
            raise ValueError("Fornecedor possui compras vinculadas. Exclua as compras antes de remover o fornecedor.")
        quantidade = executar(
            self.banco,
            "DELETE FROM FORNECEDOR WHERE id_fornecedor = :id",
            {"id": id_fornecedor},
            escrita=True,
        )
        if quantidade == 0:
            raise ValueError("Fornecedor nao encontrado.")
        return True
