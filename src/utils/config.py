import os
import time

# Menus do Sistema
MENU_PRINCIPAL = """|                      MENU PRINCIPAL                      |
============================================================
1 - Relatórios
2 - Inserir Registros
3 - Remover Registros
4 - Atualizar Registros
5 - Sair
============================================================
Escolha uma opção: """

MENU_ENTIDADES = """
============================================================
|                    MENU DE ENTIDADES                     |
============================================================
1 - FORNECEDOR
2 - PRODUTO
3 - COMPRA
4 - ITEM COMPRA
5 - Voltar
============================================================
Escolha uma opção: """

MENU_RELATORIOS = """
============================================================
|                    MENU DE RELATÓRIOS                    |
============================================================
1 - Relatório de Compras Agrupado por Fornecedor (GROUP BY)
2 - Relatório Detalhado de Itens de Compra (JOIN)
3 - Relatório de Produtos com Estoque Baixo
4 - Relatório de Fornecedores
5 - Relatório de Produtos
6 - Relatório de Compras
7 - Voltar
============================================================
Escolha uma opção: """


def clear_console(wait_time: int = 1):
    """
    Limpa a tela do console após aguardar um tempo.
    Compatível com Linux ('posix' -> clear) e Windows ('cls').
    """
    if wait_time > 0:
        time.sleep(wait_time)
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
