import os
import sys
from conexion.oracle_queries import ConexaoOracle


def extrair_comandos_sql(caminho_arquivo: str) -> list:
    """
    Lê um arquivo .sql, ignora linhas de comentário (--) e separa
    cada instrução SQL pelo ponto e vírgula (;).
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        linhas_uteis = [
            linha for linha in arquivo.readlines()
            if not linha.strip().startswith("--")
        ]

    conteudo_limpo = "".join(linhas_uteis)
    comandos = [cmd.strip() for cmd in conteudo_limpo.split(";") if cmd.strip()]
    return comandos


def criar_estrutura_banco(banco: ConexaoOracle, caminho_ddl: str):
    print("\n=== [1/3] CRIANDO TABELAS E SEQUENCES NO ORACLE ===")
    comandos_ddl = extrair_comandos_sql(caminho_ddl)

    for comando in comandos_ddl:
        primeira_linha = comando.splitlines()[0].strip()
        try:
            banco.executar_ddl(comando)
            print(f"[OK] {primeira_linha}")
        except Exception as erro:
            msg_erro = str(erro)
            # ORA-00942 (tabela não existe) / ORA-02289 (sequence não existe) na primeira execução
            if comando.upper().startswith("DROP") and ("ORA-00942" in msg_erro or "ORA-02289" in msg_erro):
                print(f"[INFO] Objeto ainda não existia ({primeira_linha}) - ignorado.")
            else:
                print(f"[ERRO] Falha ao executar '{primeira_linha}': {erro}")


def inserir_dados_iniciais(banco: ConexaoOracle, caminho_dml: str):
    print("\n=== [2/3] INSERINDO REGISTROS INICIAIS NAS TABELAS ===")
    comandos_dml = extrair_comandos_sql(caminho_dml)

    for indice, comando in enumerate(comandos_dml, start=1):
        try:
            banco.executar_dml(comando)
            print(f"[OK] Registro inicial #{indice} inserido com sucesso.")
        except Exception as erro:
            print(f"[ERRO] Falha ao inserir registro #{indice}: {erro}")


def validar_carga_inicial(banco: ConexaoOracle):
    print("\n=== [3/3] VERIFICANDO DADOS GRAVADOS NO ORACLE ===")
    for tabela in ["FORNECEDOR", "PRODUTO", "COMPRA", "ITEM_COMPRA"]:
        try:
            df = banco.consultar(f"SELECT * FROM {tabela}")
            print(f"\n-> Tabela {tabela} ({len(df)} registros):")
            print(df)
        except Exception as erro:
            print(f"[ERRO] Não foi possível consultar a tabela {tabela}: {erro}")


def inicializar_banco():
    diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_ddl = os.path.join(diretorio_raiz, "sql", "create_tables_estoque.sql")
    caminho_dml = os.path.join(diretorio_raiz, "sql", "inserting_samples_estoque.sql")

    banco = ConexaoOracle(permite_escrita=True)

    print(f"Testando conexão com Oracle em {banco.host}:{banco.porta}/{banco.servico}...")
    try:
        banco.conectar()
        banco.desconectar()
        print("[OK] Conexão estabelecida com sucesso!")
    except Exception as erro:
        print(f"[ERRO DE CONEXÃO] Não foi possível conectar ao Oracle ({banco.host}:{banco.porta}/{banco.servico}):\n{erro}")
        sys.exit(1)

    criar_estrutura_banco(banco, caminho_ddl)
    inserir_dados_iniciais(banco, caminho_dml)
    validar_carga_inicial(banco)
    print("\nBanco de dados inicializado e validado com sucesso!\n")


if __name__ == "__main__":
    inicializar_banco()
