import os
import time

# Menus do Sistema
MENU_PRINCIPAL = """
================================================
|                MENU PRINCIPAL                |
================================================
1 - Relatórios
2 - Inserir Registros
3 - Remover Registros
4 - Atualizar Registros
5 - Sair
================================================
Escolha uma opção: """

MENU_ENTIDADES = """
================================================
|              MENU DE ENTIDADES               |
================================================
1 - FORNECEDOR
2 - PRODUTO
3 - COMPRA
4 - ITEM COMPRA
5 - Voltar
================================================
Escolha uma opção: """

MENU_RELATORIOS = """
================================================
|              MENU DE RELATÓRIOS              |
================================================
1 - Relatório de Compras Agrupado por Fornecedor
2 - Relatório Detalhado de Compras
3 - Voltar
================================================
Escolha uma opção: """

def clear_console(wait_time: int = 3):
    '''
    Limpa a tela do console após aguardar um tempo.
    '''
    time.sleep(wait_time)
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
