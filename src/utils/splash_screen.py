"""Tela inicial do Sistema de Gerenciamento de Estoque."""


class SplashScreen:
    """Exibe os dados do projeto e as contagens fornecidas pelo Oracle."""

    TABELAS = ("FORNECEDOR", "PRODUTO", "COMPRA", "ITEM_COMPRA")
    INTEGRANTES = (
        "Arthur Gava Calil",
        "André Luiz Alves Bofonha",
        "Miguel Gomes",
        "Kawan Wendler Goldner",
        "João Vitor Gnocchi da Cunha",
        "João Vitor Gera Bof",
    )

    def __init__(self, conexao=None):
        self.conexao = conexao

    def _contar_registros(self):
        contagens = {}
        erros = {}

        if self.conexao is None:
            erros["CONEXAO"] = "conexão Oracle compartilhada não fornecida"
            return contagens, erros

        # Suporta tanto ConexaoOracle (método consultar) quanto conexão DB-API direta (.cursor)
        if hasattr(self.conexao, "consultar"):
            for tabela in self.TABELAS:
                alias = f"total_{tabela.lower()}"
                sql = f"SELECT COUNT(1) {alias} FROM {tabela}"
                try:
                    df = self.conexao.consultar(sql)
                    contagens[tabela] = int(df[alias].iloc[0])
                except Exception as erro:
                    erros[tabela] = str(erro)
            return contagens, erros

        cursor = None
        try:
            cursor = self.conexao.cursor()
            for tabela in self.TABELAS:
                alias = f"total_{tabela.lower()}"
                try:
                    cursor.execute(f"SELECT COUNT(1) {alias} FROM {tabela}")
                    resultado = cursor.fetchone()
                    if resultado is None:
                        raise RuntimeError("consulta sem resultado")
                    contagens[tabela] = int(resultado[0])
                except Exception as erro:
                    erros[tabela] = str(erro)
        except Exception as erro:
            erros["CONEXAO"] = str(erro)
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

        return contagens, erros

    def get_updated_screen(self):
        """Retorna a tela atualizada; sem conexão, informa dados indisponíveis."""
        contagens, erros = self._contar_registros()

        linhas = [
            "=" * 52,
            "Sistema de Gerenciamento de Estoque",
            "Professor: Howard Roatti",
            "Disciplina: Banco de Dados",
            "Semestre: 2026/2",
            "=" * 52,
            "Integrantes:",
        ]
        linhas.extend("- " + nome for nome in self.INTEGRANTES)
        linhas.append("")
        linhas.append("Registros no Oracle:")
        if "CONEXAO" in erros:
            linhas.append("Oracle indisponível: " + erros["CONEXAO"])

        for tabela in self.TABELAS:
            if tabela in contagens:
                quantidade = contagens[tabela]
                situacao = "COM REGISTROS" if quantidade else "VAZIA"
                linhas.append(f"{tabela:<18} {quantidade:>6}  {situacao}")
            elif tabela in erros:
                linhas.append(f"{tabela:<18} indisponível: {erros[tabela]}")
            else:
                linhas.append(f"{tabela:<18} indisponível")

        return "\n".join(linhas)


if __name__ == "__main__":
    print(SplashScreen().get_updated_screen())
