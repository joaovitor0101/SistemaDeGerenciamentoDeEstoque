"""Operacoes de compra. O menu chama estes metodos e trata ValueError.

As consultas usam SQL explicito com parametros, sem ORM. Nao ha input/print
nesta camada: a interface e a confirmacao de exclusao pertencem ao menu.
"""
from datetime import date, datetime

from model.compra import Compra
from model.fornecedor import Fornecedor


def inteiro_positivo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise ValueError(f"{campo} deve ser um inteiro positivo.")
    return valor


def inteiro_nao_negativo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
        raise ValueError(f"{campo} deve ser um inteiro maior ou igual a zero.")
    return valor


def executar(banco, sql, parametros=None, escrita=False, unico=False):
    """Uma operacao por conexao, com commit/rollback e fechamento garantido."""
    if escrita and not banco.permite_escrita:
        raise PermissionError("A conexao precisa de permite_escrita=True.")
    try:
        cursor = banco.conectar()
        cursor.execute(sql, parametros or {})
        if escrita:
            quantidade = cursor.rowcount
            banco.conexao.commit()
            return quantidade
        return cursor.fetchone() if unico else cursor.fetchall()
    except Exception:
        if escrita and banco.conexao is not None:
            banco.conexao.rollback()
        raise
    finally:
        banco.desconectar()


def existe(banco, tabela, coluna, codigo):
    # Tabela e coluna sao constantes internas, nunca entradas do usuario.
    inteiro_positivo(codigo, coluna)
    return executar(banco, f"SELECT {coluna} FROM {tabela} WHERE {coluna} = :id",
                    {"id": codigo}, unico=True) is not None


class ControllerCompra:
    def __init__(self, banco=None):
        if banco is None:
            from conexion.oracle_queries import ConexaoOracle
            banco = ConexaoOracle(permite_escrita=True)
        self.banco = banco

    def existe(self, id_compra):
        return existe(self.banco, "COMPRA", "id_compra", id_compra)

    def _validar(self, compra):
        if not isinstance(compra, Compra):
            raise ValueError("Informe um objeto Compra.")
        fornecedor = compra.get_fornecedor()
        if not isinstance(fornecedor, Fornecedor):
            raise ValueError("A compra precisa de um objeto Fornecedor.")
        codigo = inteiro_positivo(fornecedor.get_id_fornecedor(), "Fornecedor")
        if not existe(self.banco, "FORNECEDOR", "id_fornecedor", codigo):
            raise ValueError("Fornecedor nao encontrado.")
        data = compra.get_data_compra()
        if isinstance(data, datetime):
            data = data.date()
        if not isinstance(data, date):
            raise ValueError("Data da compra deve ser datetime.date.")
        status = compra.get_status()
        if not isinstance(status, str) or not status.strip() or len(status.strip()) > 12:
            raise ValueError("Status deve ter entre 1 e 12 caracteres.")
        return {"fornecedor": codigo, "data_compra": data,
                "status": status.strip().upper()}

    def inserir(self, compra):
        parametros = self._validar(compra)
        if compra.get_id_compra() is not None:
            raise ValueError("Uma nova compra deve ter id_compra=None.")
        codigo = self.banco.obter_proximo_id("SEQ_COMPRA")
        parametros["id"] = codigo
        executar(self.banco, """INSERT INTO COMPRA
            (id_compra, id_fornecedor, data_compra, status)
            VALUES (:id, :fornecedor, :data_compra, :status)""", parametros, escrita=True)
        compra.set_id_compra(codigo)
        return self.buscar(codigo)

    @staticmethod
    def _objeto(linha):
        cnpj_limpo = linha[6].strip() if linha[6] else linha[6]
        fornecedor = Fornecedor(linha[4], linha[5], cnpj_limpo, linha[7], linha[8])
        return Compra(linha[0], fornecedor, linha[2], linha[3])

    _SELECT = """SELECT c.id_compra, c.id_fornecedor, c.data_compra, c.status,
        f.id_fornecedor, f.nome, f.cnpj, f.telefone, f.email
        FROM COMPRA c JOIN FORNECEDOR f ON f.id_fornecedor = c.id_fornecedor"""

    def listar(self, id_fornecedor=None):
        sql = self._SELECT
        parametros = {}
        if id_fornecedor is not None:
            inteiro_positivo(id_fornecedor, "Fornecedor")
            sql += " WHERE c.id_fornecedor = :fornecedor"
            parametros["fornecedor"] = id_fornecedor
        return [self._objeto(linha) for linha in executar(
            self.banco, sql + " ORDER BY c.id_compra", parametros)]

    def buscar(self, id_compra):
        inteiro_positivo(id_compra, "Compra")
        linha = executar(self.banco, self._SELECT + " WHERE c.id_compra = :id",
                         {"id": id_compra}, unico=True)
        return self._objeto(linha) if linha else None

    def atualizar(self, compra):
        parametros = self._validar(compra)
        codigo = inteiro_positivo(compra.get_id_compra(), "Compra")
        parametros["id"] = codigo
        quantidade = executar(self.banco, """UPDATE COMPRA SET
            id_fornecedor = :fornecedor, data_compra = :data_compra, status = :status
            WHERE id_compra = :id""", parametros, escrita=True)
        if quantidade == 0:
            raise ValueError("Compra nao encontrada.")
        return self.buscar(codigo)

    def excluir(self, id_compra):
        inteiro_positivo(id_compra, "Compra")
        if not self.existe(id_compra):
            raise ValueError("Compra nao encontrada.")
        filho = executar(self.banco,
            "SELECT id_item FROM ITEM_COMPRA WHERE id_compra = :id",
            {"id": id_compra}, unico=True)
        if filho:
            raise ValueError("Compra possui itens. Exclua os itens antes de excluir a compra.")
        quantidade = executar(self.banco, "DELETE FROM COMPRA WHERE id_compra = :id",
                              {"id": id_compra}, escrita=True)
        if quantidade == 0:
            raise ValueError("Compra nao encontrada.")
        return True
