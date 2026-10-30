"""Execução e apresentação dos relatórios do sistema de estoque."""

from pathlib import Path
import sys


class Relatorio:
    """Executa relatórios pela classe compartilhada ConexaoOracle."""

    def __init__(self, conexao=None, saida=None):
        self.conexao = conexao
        self.saida = saida if saida is not None else sys.stdout

    def _executar_relatorio(self, arquivo, titulo):
        print("\n=== {} ===".format(titulo), file=self.saida)
        caminho_sql = Path(__file__).resolve().parents[1] / "sql" / arquivo

        try:
            sql = caminho_sql.read_text(encoding="utf-8")
            if not sql.strip():
                raise ValueError("o arquivo SQL está vazio")
            sql = sql.rstrip()
            if sql.endswith(";"):
                sql = sql[:-1].rstrip()
        except (OSError, ValueError) as erro:
            print("Não foi possível carregar o SQL: {}".format(erro), file=self.saida)
            return

        if self.conexao is None:
            print("Conexão Oracle compartilhada não fornecida.", file=self.saida)
            return

        try:
            resultado = self.conexao.consultar(sql)
            if resultado.empty:
                print("A consulta não retornou registros.", file=self.saida)
            else:
                print(resultado.to_string(index=False), file=self.saida)
        except Exception as erro:
            print("Falha ao executar o relatório: {}".format(erro), file=self.saida)

    def get_relatorio_compras_por_fornecedor(self):
        """Exibe as compras agrupadas por fornecedor (GROUP BY)."""
        self._executar_relatorio(
            "relatorio_compras_por_fornecedor.sql",
            "Relatório de Compras por Fornecedor (Sumarização)",
        )

    def get_relatorio_itens_compra(self):
        """Exibe os itens detalhados das compras (JOIN)."""
        self._executar_relatorio(
            "relatorio_itens_compra.sql",
            "Relatório Detalhado de Itens de Compra (Junção de Tabelas)",
        )

    def get_relatorio_estoque_baixo(self):
        """Exibe os produtos com estoque atual abaixo ou igual ao estoque mínimo."""
        self._executar_relatorio(
            "relatorio_estoque_baixo.sql",
            "Relatório de Produtos com Estoque Baixo",
        )

    def get_relatorio_fornecedores(self):
        """Exibe isoladamente todos os fornecedores cadastrados."""
        self._executar_relatorio(
            "relatorio_fornecedores.sql",
            "Relatório de Fornecedores Cadastrados",
        )

    def get_relatorio_produtos(self):
        """Exibe isoladamente todos os produtos cadastrados."""
        self._executar_relatorio(
            "relatorio_produtos.sql",
            "Relatório de Produtos Cadastrados",
        )

    def get_relatorio_compras(self):
        """Exibe isoladamente todas as compras registradas."""
        self._executar_relatorio(
            "relatorio_compras.sql",
            "Relatório de Compras Registradas",
        )
