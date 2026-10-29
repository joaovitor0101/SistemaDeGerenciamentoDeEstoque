import os
import pandas as pd

# Tenta carregar o driver moderno (oracledb) ou o driver legado da VM (cx_Oracle)
try:
    import oracledb as oracle_driver
except ImportError:
    import cx_Oracle as oracle_driver


class ConexaoOracle:
    """
    Gerencia a conexão direta com o banco de dados Oracle (sem uso de ORM),
    permitindo executar comandos DDL, DML (INSERT/UPDATE/DELETE) e consultas SELECT.
    """

    def __init__(self, permite_escrita: bool = False):
        self.permite_escrita = permite_escrita
        self.host = os.getenv("ORACLE_HOST", "localhost")
        self.porta = int(os.getenv("ORACLE_PORT", "1521"))
        self.servico = os.getenv("ORACLE_SERVICE", "XEPDB1")
        self.usuario = os.getenv("ORACLE_USER", "labdatabase")
        self.senha = os.getenv("ORACLE_PASSWORD", "labDatabase2022")

        self.conexao = None
        self.cursor = None

    def conectar(self):
        """Abre a conexão com o Oracle e retorna o cursor ativo."""
        dsn = f"{self.host}:{self.porta}/{self.servico}"
        self.conexao = oracle_driver.connect(
            user=self.usuario,
            password=self.senha,
            dsn=dsn
        )
        self.cursor = self.conexao.cursor()
        return self.cursor

    def desconectar(self):
        """Fecha o cursor e a conexão ativa com segurança."""
        if self.cursor is not None:
            try:
                self.cursor.close()
            except Exception:
                pass
            self.cursor = None

        if self.conexao is not None:
            try:
                self.conexao.close()
            except Exception:
                pass
            self.conexao = None

    def consultar(self, sql: str) -> pd.DataFrame:
        """Executa uma consulta SELECT e retorna os registros em um DataFrame do Pandas."""
        try:
            self.conectar()
            self.cursor.execute(sql)
            linhas = self.cursor.fetchall()
            colunas = [col[0].lower() for col in self.cursor.description]
            return pd.DataFrame(linhas, columns=colunas)
        finally:
            self.desconectar()

    def executar_dml(self, sql: str) -> int:
        """
        Executa comandos de manipulação de dados (INSERT, UPDATE, DELETE)
        e confirma a gravação no banco com commit().
        """
        if not self.permite_escrita:
            raise PermissionError("Esta instância de conexão não tem permissão de escrita (permite_escrita=False).")

        try:
            self.conectar()
            self.cursor.execute(sql)
            linhas_afetadas = self.cursor.rowcount
            self.conexao.commit()
            return linhas_afetadas
        finally:
            self.desconectar()

    def executar_ddl(self, sql: str):
        """Executa comandos estruturais no banco (CREATE, DROP, ALTER)."""
        if not self.permite_escrita:
            raise PermissionError("Esta instância de conexão não tem permissão de escrita (permite_escrita=False).")

        try:
            self.conectar()
            self.cursor.execute(sql)
        finally:
            self.desconectar()

    def obter_proximo_id(self, nome_sequence: str) -> int:
        """Busca o próximo número de uma SEQUENCE do Oracle para usar como PK."""
        try:
            self.conectar()
            self.cursor.execute(f"SELECT {nome_sequence}.NEXTVAL FROM DUAL")
            proximo_valor = self.cursor.fetchone()[0]
            return int(proximo_valor)
        finally:
            self.desconectar()

