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
        # A conexão compartilhada é recebida do programa principal.
        self.conexao = conexao

    def get_updated_screen(self):
        """Retorna a tela atualizada; sem conexão, informa dados indisponíveis."""
        contagens = {}
        erros = {}
        cursor = None

        if self.conexao is None:
            erros["CONEXAO"] = "conexão Oracle compartilhada não fornecida"
        else:
            try:
                cursor = self.conexao.cursor()
                for tabela in self.TABELAS:
                    try:
                        cursor.execute("SELECT COUNT(1) FROM " + tabela)
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
