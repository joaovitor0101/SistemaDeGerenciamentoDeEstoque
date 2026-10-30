import sys
from pathlib import Path
from datetime import datetime, date

# Garante que os imports funcionem tanto rodando da raiz ("python3 src/principal.py")
# quanto rodando de dentro da pasta src ("cd src && python3 principal.py")
DIRETORIO_SRC = Path(__file__).resolve().parent
DIRETORIO_RAIZ = DIRETORIO_SRC.parent
if str(DIRETORIO_SRC) not in sys.path:
    sys.path.insert(0, str(DIRETORIO_SRC))
if str(DIRETORIO_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIRETORIO_RAIZ))

from conexion.oracle_queries import ConexaoOracle
from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio

from controller.controller_fornecedor import ControllerFornecedor
from controller.controller_produto import ControllerProduto
from controller.controller_compra import ControllerCompra
from controller.controller_item_compra import ControllerItemCompra

from model.fornecedor import Fornecedor
from model.produto import Produto
from model.compra import Compra
from model.item_compra import ItemCompra


def exibir_registros(lista_objetos, titulo: str) -> bool:
    """Lista os registros existentes da entidade selecionada (PK + campos descritivos)."""
    print(f"\n--- {titulo} ---")
    if not lista_objetos:
        print("Nenhum registro cadastrado nesta tabela.")
        return False
    for obj in lista_objetos:
        print(obj.to_string())
    return True


def formatar_data(valor) -> str:
    if isinstance(valor, (datetime, date)):
        return valor.strftime("%d/%m/%Y")
    return str(valor)


def ler_decimal(texto_input: str) -> float:
    return float(texto_input.strip().replace(",", "."))


def perguntar_continuar(acao: str) -> bool:
    """Pergunta se o usuário deseja realizar a operação novamente (Itens 6.b.5, 6.c.6 e 6.d.8)."""
    resposta = input(f"\nDeseja {acao} mais algum registro? [S/N]: ").strip().upper()
    return resposta in ("S", "SIM")


def menu_relatorios(relatorio: Relatorio):
    while True:
        opcao_relatorio = input(config.MENU_RELATORIOS).strip()

        if opcao_relatorio == '1':
            relatorio.get_relatorio_compras_por_fornecedor()
            input("\nPressione Enter para voltar ao menu de relatórios...")
        elif opcao_relatorio == '2':
            relatorio.get_relatorio_itens_compra()
            input("\nPressione Enter para voltar ao menu de relatórios...")
        elif opcao_relatorio == '3':
            relatorio.get_relatorio_estoque_baixo()
            input("\nPressione Enter para voltar ao menu de relatórios...")
        elif opcao_relatorio == '4':
            break
        else:
            print("Opção inválida. Escolha entre 1 e 4.")


def menu_inserir(ctrl_fornecedor, ctrl_produto, ctrl_compra, ctrl_item_compra):
    while True:
        opcao_inserir = input(config.MENU_ENTIDADES).strip()
        if opcao_inserir == '5':
            break

        try:
            if opcao_inserir == '1':
                print("\n--- Inserir Novo Fornecedor ---")
                nome = input("Nome (obrigatório): ").strip()
                cnpj = input("CNPJ (somente números, até 14 dígitos): ").strip()
                telefone = input("Telefone (opcional): ").strip() or None
                email = input("Email (opcional): ").strip() or None

                novo_fornecedor = Fornecedor(None, nome, cnpj, telefone, email)
                inserido = ctrl_fornecedor.inserir(novo_fornecedor)
                print("\nFornecedor inserido com sucesso:")
                print(inserido.to_string())

            elif opcao_inserir == '2':
                print("\n--- Inserir Novo Produto ---")
                nome = input("Nome do Produto (obrigatório): ").strip()
                descricao = input("Descrição (opcional): ").strip() or None
                preco_venda = ler_decimal(input("Preço de Venda (ex: 59.90): "))
                estoque_atual = int(input("Estoque Atual (inteiro): ").strip())
                estoque_minimo = int(input("Estoque Mínimo (inteiro): ").strip())

                novo_produto = Produto(None, nome, descricao, preco_venda, estoque_atual, estoque_minimo)
                inserido = ctrl_produto.inserir(novo_produto)
                print("\nProduto inserido com sucesso:")
                print(inserido.to_string())

            elif opcao_inserir == '3':
                if not exibir_registros(ctrl_fornecedor.listar(), "Fornecedores Disponíveis"):
                    print("Cadastre ao menos um fornecedor antes de registrar uma compra.")
                else:
                    print("\n--- Inserir Nova Compra ---")
                    id_fornecedor = int(input("ID do Fornecedor: ").strip())
                    fornecedor = ctrl_fornecedor.buscar(id_fornecedor)
                    if not fornecedor:
                        print("Fornecedor não encontrado.")
                    else:
                        data_str = input("Data da compra (DD/MM/AAAA) [Enter para hoje]: ").strip()
                        data_compra = (
                            datetime.strptime(data_str, "%d/%m/%Y").date()
                            if data_str else date.today()
                        )
                        status = input("Status (ex: PENDENTE, CONCLUIDA - até 12 caracteres): ").strip()

                        nova_compra = Compra(None, fornecedor, data_compra, status)
                        inserida = ctrl_compra.inserir(nova_compra)
                        print("\nCompra inserida com sucesso:")
                        print(inserida.to_string())

            elif opcao_inserir == '4':
                tem_compras = exibir_registros(ctrl_compra.listar(), "Compras Disponíveis")
                tem_produtos = exibir_registros(ctrl_produto.listar(), "Produtos Disponíveis")
                if not tem_compras or not tem_produtos:
                    print("É necessário ter ao menos uma Compra e um Produto cadastrados.")
                else:
                    print("\n--- Inserir Novo Item de Compra ---")
                    id_compra = int(input("ID da Compra: ").strip())
                    compra = ctrl_compra.buscar(id_compra)
                    if not compra:
                        print("Compra não encontrada.")
                    else:
                        id_produto = int(input("ID do Produto: ").strip())
                        produto = ctrl_produto.buscar(id_produto)
                        if not produto:
                            print("Produto não encontrado.")
                        else:
                            quantidade = int(input("Quantidade comprada (inteiro positivo): ").strip())
                            preco_unitario = ler_decimal(input("Preço Unitário de compra (ex: 35.00): "))

                            novo_item = ItemCompra(None, compra, produto, quantidade, preco_unitario)
                            inserido = ctrl_item_compra.inserir(novo_item)
                            print("\nItem de compra inserido com sucesso:")
                            print(inserido.to_string())
            else:
                print("Opção inválida. Escolha entre 1 e 5.")
                continue

        except ValueError as erro:
            print(f"\nErro de validação: {erro}")
        except Exception as erro:
            print(f"\nErro ao inserir registro no banco: {erro}")

        if not perguntar_continuar("inserir"):
            break


def menu_remover(ctrl_fornecedor, ctrl_produto, ctrl_compra, ctrl_item_compra):
    while True:
        opcao_remover = input(config.MENU_ENTIDADES).strip()
        if opcao_remover == '5':
            break

        try:
            if opcao_remover == '1':
                if exibir_registros(ctrl_fornecedor.listar(), "Fornecedores Cadastrados"):
                    id_f = int(input("\nInforme o ID do Fornecedor que deseja remover: ").strip())
                    fornecedor = ctrl_fornecedor.buscar(id_f)
                    if not fornecedor:
                        print("Fornecedor não encontrado.")
                    else:
                        confirma = input(
                            f"Tem certeza que deseja remover o fornecedor '{fornecedor.get_nome()}' (ID {id_f})? [S/N]: "
                        ).strip().upper()
                        if confirma not in ("S", "SIM"):
                            print("Remoção cancelada. Retornando ao menu principal.")
                            break

                        # Item 6.c.5.i: Verifica se o fornecedor é FK na tabela COMPRA
                        compras_vinculadas = ctrl_compra.listar(id_fornecedor=id_f)
                        if compras_vinculadas:
                            print(
                                f"\nATENÇÃO: Este fornecedor é referenciado (FK) em {len(compras_vinculadas)} compra(s) na tabela COMPRA:"
                            )
                            for c in compras_vinculadas:
                                print("  ->", c.to_string())
                            remover_filhos = input(
                                "Deseja remover também as compras vinculadas (e seus itens) para concluir a exclusão? [S/N]: "
                            ).strip().upper()
                            if remover_filhos in ("S", "SIM"):
                                for c in compras_vinculadas:
                                    for item in ctrl_item_compra.listar(id_compra=c.get_id_compra()):
                                        ctrl_item_compra.excluir(item.get_id_item())
                                    ctrl_compra.excluir(c.get_id_compra())
                                ctrl_fornecedor.excluir(id_f)
                                print("Registros filhos e fornecedor removidos com sucesso!")
                            else:
                                print("O fornecedor não pôde ser excluído pois possui compras vinculadas.")
                        else:
                            ctrl_fornecedor.excluir(id_f)
                            print("Fornecedor removido com sucesso!")

            elif opcao_remover == '2':
                if exibir_registros(ctrl_produto.listar(), "Produtos Cadastrados"):
                    id_p = int(input("\nInforme o ID do Produto que deseja remover: ").strip())
                    produto = ctrl_produto.buscar(id_p)
                    if not produto:
                        print("Produto não encontrado.")
                    else:
                        confirma = input(
                            f"Tem certeza que deseja remover o produto '{produto.get_nome()}' (ID {id_p})? [S/N]: "
                        ).strip().upper()
                        if confirma not in ("S", "SIM"):
                            print("Remoção cancelada. Retornando ao menu principal.")
                            break

                        # Item 6.c.5.i: Verifica se o produto é FK na tabela ITEM_COMPRA
                        itens_vinculados = ctrl_item_compra.listar(id_produto=id_p)
                        if itens_vinculados:
                            print(
                                f"\nATENÇÃO: Este produto é referenciado (FK) em {len(itens_vinculados)} item(ns) na tabela ITEM_COMPRA:"
                            )
                            for item in itens_vinculados:
                                print("  ->", item.to_string())
                            remover_filhos = input(
                                "Deseja remover também os itens de compra vinculados na tabela filha? [S/N]: "
                            ).strip().upper()
                            if remover_filhos in ("S", "SIM"):
                                for item in itens_vinculados:
                                    ctrl_item_compra.excluir(item.get_id_item())
                                ctrl_produto.excluir(id_p)
                                print("Itens vinculados e produto removidos com sucesso!")
                            else:
                                print("O produto não pôde ser excluído pois possui itens de compra vinculados.")
                        else:
                            ctrl_produto.excluir(id_p)
                            print("Produto removido com sucesso!")

            elif opcao_remover == '3':
                if exibir_registros(ctrl_compra.listar(), "Compras Cadastradas"):
                    id_c = int(input("\nInforme o ID da Compra que deseja remover: ").strip())
                    compra = ctrl_compra.buscar(id_c)
                    if not compra:
                        print("Compra não encontrada.")
                    else:
                        confirma = input(
                            f"Tem certeza que deseja remover a Compra de ID {id_c}? [S/N]: "
                        ).strip().upper()
                        if confirma not in ("S", "SIM"):
                            print("Remoção cancelada. Retornando ao menu principal.")
                            break

                        # Item 6.c.5.i: Verifica se a compra possui itens filhos em ITEM_COMPRA
                        itens_vinculados = ctrl_item_compra.listar(id_compra=id_c)
                        if itens_vinculados:
                            print(
                                f"\nATENÇÃO: Esta compra é referenciada (FK) e possui {len(itens_vinculados)} item(ns) em ITEM_COMPRA:"
                            )
                            for item in itens_vinculados:
                                print("  ->", item.to_string())
                            remover_filhos = input(
                                "Deseja remover também os itens desta compra na tabela filha? [S/N]: "
                            ).strip().upper()
                            if remover_filhos in ("S", "SIM"):
                                for item in itens_vinculados:
                                    ctrl_item_compra.excluir(item.get_id_item())
                                ctrl_compra.excluir(id_c)
                                print("Itens vinculados e compra removidos com sucesso!")
                            else:
                                print("A compra não pôde ser excluída pois possui itens vinculados.")
                        else:
                            ctrl_compra.excluir(id_c)
                            print("Compra removida com sucesso!")

            elif opcao_remover == '4':
                if exibir_registros(ctrl_item_compra.listar(), "Itens de Compra Cadastrados"):
                    id_i = int(input("\nInforme o ID do Item de Compra que deseja remover: ").strip())
                    item = ctrl_item_compra.buscar(id_i)
                    if not item:
                        print("Item de compra não encontrado.")
                    else:
                        confirma = input(
                            f"Tem certeza que deseja remover o Item de ID {id_i}? [S/N]: "
                        ).strip().upper()
                        if confirma not in ("S", "SIM"):
                            print("Remoção cancelada. Retornando ao menu principal.")
                            break
                        ctrl_item_compra.excluir(id_i)
                        print("Item de compra removido com sucesso!")
            else:
                print("Opção inválida. Escolha entre 1 e 5.")
                continue

        except ValueError as erro:
            print(f"\nErro de validação: {erro}")
        except Exception as erro:
            print(f"\nErro ao remover registro: {erro}")

        if not perguntar_continuar("excluir"):
            break


def menu_atualizar(ctrl_fornecedor, ctrl_produto, ctrl_compra, ctrl_item_compra):
    while True:
        opcao_atualizar = input(config.MENU_ENTIDADES).strip()
        if opcao_atualizar == '5':
            break

        try:
            if opcao_atualizar == '1':
                if exibir_registros(ctrl_fornecedor.listar(), "Fornecedores Cadastrados"):
                    id_f = int(input("\nInforme o ID do Fornecedor que deseja atualizar: ").strip())
                    f_atual = ctrl_fornecedor.buscar(id_f)
                    if f_atual:
                        print("(Pressione Enter em um campo caso queira manter o valor atual)")
                        nome = input(f"Nome ({f_atual.get_nome()}): ").strip() or f_atual.get_nome()
                        cnpj = input(f"CNPJ ({f_atual.get_cnpj()}): ").strip() or f_atual.get_cnpj()
                        tel_atual = f_atual.get_telefone() or ""
                        mail_atual = f_atual.get_email() or ""
                        telefone = input(f"Telefone ({tel_atual}): ").strip() or f_atual.get_telefone()
                        email = input(f"Email ({mail_atual}): ").strip() or f_atual.get_email()

                        f_atual.set_nome(nome)
                        f_atual.set_cnpj(cnpj)
                        f_atual.set_telefone(telefone)
                        f_atual.set_email(email)
                        atualizado = ctrl_fornecedor.atualizar(f_atual)
                        print("\nRegistro atualizado com sucesso:")
                        print(atualizado.to_string())
                    else:
                        print("Fornecedor não encontrado.")

            elif opcao_atualizar == '2':
                if exibir_registros(ctrl_produto.listar(), "Produtos Cadastrados"):
                    id_p = int(input("\nInforme o ID do Produto que deseja atualizar: ").strip())
                    p_atual = ctrl_produto.buscar(id_p)
                    if p_atual:
                        print("(Pressione Enter em um campo caso queira manter o valor atual)")
                        nome = input(f"Nome ({p_atual.get_nome()}): ").strip() or p_atual.get_nome()
                        desc_atual = p_atual.get_descricao() or ""
                        descricao = input(f"Descrição ({desc_atual}): ").strip() or p_atual.get_descricao()
                        preco_str = input(f"Preço de Venda ({p_atual.get_preco_venda():.2f}): ").strip()
                        preco = ler_decimal(preco_str) if preco_str else p_atual.get_preco_venda()
                        est_str = input(f"Estoque Atual ({p_atual.get_estoque_atual()}): ").strip()
                        estoque = int(est_str) if est_str else p_atual.get_estoque_atual()
                        min_str = input(f"Estoque Mínimo ({p_atual.get_estoque_minimo()}): ").strip()
                        minimo = int(min_str) if min_str else p_atual.get_estoque_minimo()

                        p_atual.set_nome(nome)
                        p_atual.set_descricao(descricao)
                        p_atual.set_preco_venda(preco)
                        p_atual.set_estoque_atual(estoque)
                        p_atual.set_estoque_minimo(minimo)

                        atualizado = ctrl_produto.atualizar(p_atual)
                        print("\nRegistro atualizado com sucesso:")
                        print(atualizado.to_string())
                    else:
                        print("Produto não encontrado.")

            elif opcao_atualizar == '3':
                if exibir_registros(ctrl_compra.listar(), "Compras Cadastradas"):
                    id_c = int(input("\nInforme o ID da Compra que deseja atualizar: ").strip())
                    c_atual = ctrl_compra.buscar(id_c)
                    if c_atual:
                        exibir_registros(ctrl_fornecedor.listar(), "Fornecedores Disponíveis")
                        print("(Pressione Enter em um campo caso queira manter o valor atual)")
                        id_forn_atual = c_atual.get_fornecedor().get_id_fornecedor()
                        forn_str = input(f"ID do Fornecedor ({id_forn_atual}): ").strip()
                        id_fornecedor = int(forn_str) if forn_str else id_forn_atual
                        fornecedor = ctrl_fornecedor.buscar(id_fornecedor)

                        if not fornecedor:
                            print("Fornecedor informado não existe.")
                        else:
                            data_atual_fmt = formatar_data(c_atual.get_data_compra())
                            data_str = input(f"Data da Compra DD/MM/AAAA ({data_atual_fmt}): ").strip()
                            data_compra = (
                                datetime.strptime(data_str, "%d/%m/%Y").date()
                                if data_str else c_atual.get_data_compra()
                            )
                            status = input(f"Status ({c_atual.get_status()}): ").strip() or c_atual.get_status()

                            c_atual.set_fornecedor(fornecedor)
                            c_atual.set_data_compra(data_compra)
                            c_atual.set_status(status)

                            atualizado = ctrl_compra.atualizar(c_atual)
                            print("\nRegistro atualizado com sucesso:")
                            print(atualizado.to_string())
                    else:
                        print("Compra não encontrada.")

            elif opcao_atualizar == '4':
                if exibir_registros(ctrl_item_compra.listar(), "Itens de Compra Cadastrados"):
                    id_i = int(input("\nInforme o ID do Item que deseja atualizar: ").strip())
                    i_atual = ctrl_item_compra.buscar(id_i)
                    if i_atual:
                        print("(Pressione Enter em um campo caso queira manter o valor atual)")
                        id_c_atual = i_atual.get_compra().get_id_compra()
                        id_p_atual = i_atual.get_produto().get_id_produto()

                        comp_str = input(f"ID da Compra ({id_c_atual}): ").strip()
                        id_compra = int(comp_str) if comp_str else id_c_atual
                        prod_str = input(f"ID do Produto ({id_p_atual}): ").strip()
                        id_produto = int(prod_str) if prod_str else id_p_atual

                        compra = ctrl_compra.buscar(id_compra)
                        produto = ctrl_produto.buscar(id_produto)

                        if not compra:
                            print("Compra informada não existe.")
                        elif not produto:
                            print("Produto informado não existe.")
                        else:
                            qtd_str = input(f"Quantidade ({i_atual.get_quantidade()}): ").strip()
                            qtd = int(qtd_str) if qtd_str else i_atual.get_quantidade()
                            preco_atual = float(i_atual.get_preco_unitario())
                            preco_str = input(f"Preço Unitário ({preco_atual:.2f}): ").strip()
                            preco = ler_decimal(preco_str) if preco_str else i_atual.get_preco_unitario()

                            i_atual.set_compra(compra)
                            i_atual.set_produto(produto)
                            i_atual.set_quantidade(qtd)
                            i_atual.set_preco_unitario(preco)

                            atualizado = ctrl_item_compra.atualizar(i_atual)
                            print("\nRegistro atualizado com sucesso:")
                            print(atualizado.to_string())
                    else:
                        print("Item de compra não encontrado.")
            else:
                print("Opção inválida. Escolha entre 1 e 5.")
                continue

        except ValueError as erro:
            print(f"\nErro de validação: {erro}")
        except Exception as erro:
            print(f"\nErro ao atualizar registro: {erro}")

        if not perguntar_continuar("atualizar"):
            break


def run():
    banco = ConexaoOracle(permite_escrita=True)

    # Valida a conectividade inicial com o Oracle antes de abrir os menus
    try:
        banco.conectar()
        banco.desconectar()
    except Exception as erro:
        print(f"Erro ao conectar ao banco de dados Oracle: {erro}")
        print("Verifique se o serviço/container do Oracle está ativo e tente novamente.")
        sys.exit(1)

    tela_inicial = SplashScreen(conexao=banco)
    relatorio = Relatorio(conexao=banco)

    ctrl_fornecedor = ControllerFornecedor(banco=banco)
    ctrl_produto = ControllerProduto(banco=banco)
    ctrl_compra = ControllerCompra(banco=banco)
    ctrl_item_compra = ControllerItemCompra(banco=banco)

    print(tela_inicial.get_updated_screen())
    config.clear_console(2)

    while True:
        opcao = input(config.MENU_PRINCIPAL).strip()

        if opcao == '1':
            config.clear_console(0)
            menu_relatorios(relatorio)
            config.clear_console(0)

        elif opcao == '2':
            config.clear_console(0)
            menu_inserir(ctrl_fornecedor, ctrl_produto, ctrl_compra, ctrl_item_compra)
            print(tela_inicial.get_updated_screen())
            config.clear_console(2)

        elif opcao == '3':
            config.clear_console(0)
            menu_remover(ctrl_fornecedor, ctrl_produto, ctrl_compra, ctrl_item_compra)
            print(tela_inicial.get_updated_screen())
            config.clear_console(2)

        elif opcao == '4':
            config.clear_console(0)
            menu_atualizar(ctrl_fornecedor, ctrl_produto, ctrl_compra, ctrl_item_compra)
            print(tela_inicial.get_updated_screen())
            config.clear_console(2)

        elif opcao == '5':
            print(tela_inicial.get_updated_screen())
            print("\nEncerrando o Sistema de Gerenciamento de Estoque. Até logo!")
            break

        else:
            print("Opção inválida. Escolha uma opção de 1 a 5.")


if __name__ == "__main__":
    run()
