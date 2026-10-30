from model.fornecedor import Fornecedor


class ControllerFornecedor:
    # Controla o fornecedor no banco

    def __init__(self, conexao):
        self.conexao = conexao

    def inserir(self, fornecedor: Fornecedor):
        # Salva o fornecedor no banco
        cursor = self.conexao.cursor()
        id_novo = cursor.var(int)
        cursor.execute(
            """
            INSERT INTO FORNECEDOR (id_fornecedor, nome, cnpj, telefone, email)
            VALUES (SEQ_FORNECEDOR.NEXTVAL, :nome, :cnpj, :telefone, :email)
            RETURNING id_fornecedor INTO :id_novo
            """,
            {
                "nome": fornecedor.get_nome(),
                "cnpj": fornecedor.get_cnpj(),
                "telefone": fornecedor.get_telefone(),
                "email": fornecedor.get_email(),
                "id_novo": id_novo,
            },
        )
        self.conexao.commit()
        fornecedor.set_id_fornecedor(id_novo.getvalue()[0])
        cursor.close()

    def listar(self):
        # Traz todos os fornecedores
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT id_fornecedor, nome, cnpj, telefone, email FROM FORNECEDOR ORDER BY nome"
        )
        lista = []
        for id_f, nome, cnpj, telefone, email in cursor.fetchall():
            lista.append(Fornecedor(id_f, nome, cnpj.strip(), telefone, email))
        cursor.close()
        return lista

    def buscar(self, id_fornecedor: int):
        # Busca um fornecedor pelo id
        cursor = self.conexao.cursor()
        cursor.execute(
            "SELECT id_fornecedor, nome, cnpj, telefone, email FROM FORNECEDOR WHERE id_fornecedor = :id",
            {"id": id_fornecedor},
        )
        linha = cursor.fetchone()
        cursor.close()
        if linha is None:
            return None
        id_f, nome, cnpj, telefone, email = linha
        return Fornecedor(id_f, nome, cnpj.strip(), telefone, email)

    def atualizar(self, fornecedor: Fornecedor):
        # Altera os dados do fornecedor
        cursor = self.conexao.cursor()
        cursor.execute(
            """
            UPDATE FORNECEDOR
            SET nome = :nome, cnpj = :cnpj, telefone = :telefone, email = :email
            WHERE id_fornecedor = :id
            """,
            {
                "nome": fornecedor.get_nome(),
                "cnpj": fornecedor.get_cnpj(),
                "telefone": fornecedor.get_telefone(),
                "email": fornecedor.get_email(),
                "id": fornecedor.get_id_fornecedor(),
            },
        )
        self.conexao.commit()
        cursor.close()

    def excluir(self, id_fornecedor: int):
        # Apaga o fornecedor pelo id
        cursor = self.conexao.cursor()
        cursor.execute(
            "DELETE FROM FORNECEDOR WHERE id_fornecedor = :id",
            {"id": id_fornecedor},
        )
        self.conexao.commit()
        cursor.close()
