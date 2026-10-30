from datetime import datetime

from src.utils import config
from src.utils.splash_screen import SplashScreen
from src.reports.relatorios import Relatorio

from src.controller.controller_fornecedor import ControllerFornecedor
from src.controller.controller_produto import ControllerProduto
from src.controller.controller_compra import ControllerCompra
from src.controller.controller_item_compra import ControllerItemCompra

from src.model.fornecedor import Fornecedor
from src.model.produto import Produto
from src.model.compra import Compra
from src.model.item_compra import ItemCompra


def run():
    from src.conexion.oracle_queries import ConexaoOracle
    
    # 1 - banco Automático (Abre e fecha sozinho para compras e relatórios)
    oracle_automatico = ConexaoOracle(permite_escrita=True)
    
    # 2 - banco Persistente (Fica aberto para a splash screen e cadastros base)
    oracle_fixo = ConexaoOracle(permite_escrita=True)
    oracle_fixo.conectar()
    conexao_bruta = oracle_fixo.conexao

    #exibe a tela inicial
    tela_inicial = SplashScreen(conexao=conexao_bruta)
    print(tela_inicial.get_updated_screen())

    #configura a instância dos relatórios
    relatorio = Relatorio(conexao=oracle_automatico)

    #instancia os controllers
    ctrl_fornecedor = ControllerFornecedor(conexao=conexao_bruta)
    ctrl_produto = ControllerProduto(conexao=conexao_bruta)
    ctrl_compra = ControllerCompra(banco=oracle_automatico)
    ctrl_item_compra = ControllerItemCompra(banco=oracle_automatico)

    while True:
        opcao = input(config.MENU_PRINCIPAL)

        if opcao == '1':
            #submenu de relatórios
            while True:
                opcao_relatorio = input(config.MENU_RELATORIOS)
                
                if opcao_relatorio == '1':
                    relatorio.get_relatorio_compras_por_fornecedor()
                elif opcao_relatorio == '2':
                    relatorio.get_relatorio_itens_compra()
                elif opcao_relatorio == '3':
                    break
                else:
                    print("Opção inválida")
                    
        elif opcao == '2':
            #inserir registros
            opcao_inserir = input(config.MENU_ENTIDADES)
            
            if opcao_inserir == '1':
                print("\n--- Inserir Novo Fornecedor ---")
                nome = input("Nome: ")
                cnpj = input("CNPJ: ")
                telefone = input("Telefone: ")
                email = input("Email: ")
                
                novo_fornecedor = Fornecedor(
                    id_fornecedor=None, 
                    nome=nome, 
                    cnpj=cnpj, 
                    telefone=telefone, 
                    email=email
                )
                ctrl_fornecedor.inserir(novo_fornecedor)
                print("Fornecedor inserido com sucesso")

            elif opcao_inserir == '2':
                print("\n--- Inserir Novo Produto ---")
                nome = input("Nome: ")
                descricao = input("Descrição: ")
                preco_venda = float(input("Preço de Venda: "))
                estoque_atual = int(input("Estoque Atual: "))
                estoque_minimo = int(input("Estoque Mínimo: "))
                
                novo_produto = Produto(
                    id_produto=None, 
                    nome=nome, 
                    descricao=descricao, 
                    preco_venda=preco_venda, 
                    estoque_atual=estoque_atual, 
                    estoque_minimo=estoque_minimo
                )
                ctrl_produto.inserir(novo_produto)
                print("Produto inserido com sucesso")

            elif opcao_inserir == '3':
                print("\n--- Inserir Nova Compra ---")
                try:
                    id_fornecedor = int(input("ID do Fornecedor: "))
                    data_str = input("Data da compra (DD/MM/AAAA): ")
                    status = input("Status (até 12 caracteres): ")
                    
                    data_compra = datetime.strptime(data_str, "%d/%m/%Y").date()
                    
                    fornecedor = ctrl_fornecedor.buscar(id_fornecedor)
                    if not fornecedor:
                        print("Fornecedor não encontrado")
                        continue
                        
                    nova_compra = Compra(
                        id_compra=None, 
                        fornecedor=fornecedor, 
                        data_compra=data_compra, 
                        status=status
                    )
                    ctrl_compra.inserir(nova_compra)
                    print("Compra inserida com sucesso")
                    
                except ValueError as e:
                    print(f"Erro de validação: {e}")
                except Exception as e:
                    print(f"Erro: {e}")

            elif opcao_inserir == '4':
                print("\n--- Inserir Novo Item Compra ---")
                try:
                    id_compra = int(input("ID da Compra: "))
                    id_produto = int(input("ID do Produto: "))
                    quantidade = int(input("Quantidade: "))
                    preco_unitario = float(input("Preço Unitário: "))

                    compra = ctrl_compra.buscar(id_compra)
                    if not compra:
                        print("Compra não encontrada")
                        continue
                        
                    produto = ctrl_produto.buscar(id_produto)
                    if not produto:
                        print("Produto não encontrado")
                        continue

                    novo_item = ItemCompra(
                        id_item=None, 
                        compra=compra, 
                        produto=produto, 
                        quantidade=quantidade, 
                        preco_unitario=preco_unitario
                    )
                    ctrl_item_compra.inserir(novo_item)
                    print("Item inserido com sucesso")

                except ValueError as e:
                    print(f"Erro de validação: {e}")
                except Exception as e:
                    print(f"Erro: {e}")

            elif opcao_inserir == '5':
                continue
            else:
                print("Opção inválida.")
            
        elif opcao == '3':
            #remover registros
            opcao_remover = input(config.MENU_ENTIDADES)
            
            if opcao_remover == '1':
                id_f = int(input("ID do Fornecedor a remover: "))
                ctrl_fornecedor.excluir(id_f)
                print("Excluído com sucesso")
            elif opcao_remover == '2':
                id_p = int(input("ID do Produto a remover: "))
                ctrl_produto.excluir(id_p)
                print("Excluído com sucesso")
            elif opcao_remover == '3':
                id_c = int(input("ID da Compra a remover: "))
                ctrl_compra.excluir(id_c)
                print("Excluído com sucesso")
            elif opcao_remover == '4':
                id_i = int(input("ID do Item a remover: "))
                ctrl_item_compra.excluir(id_i)
                print("Excluído com sucesso")
            elif opcao_remover == '5':
                continue
            else:
                print("Opção inválida.")
            
        elif opcao == '4':
            #atualizar registros
            opcao_atualizar = input(config.MENU_ENTIDADES)
            
            if opcao_atualizar == '1':
                id_f = int(input("ID do Fornecedor a atualizar: "))
                f_atual = ctrl_fornecedor.buscar(id_f)
                if f_atual:
                    nome = input(f"Nome atual ({f_atual.get_nome()}): ") or f_atual.get_nome()
                    cnpj = input(f"CNPJ atual ({f_atual.get_cnpj()}): ") or f_atual.get_cnpj()
                    telefone = input(f"Telefone atual ({f_atual.get_telefone()}): ") or f_atual.get_telefone()
                    email = input(f"Email atual ({f_atual.get_email()}): ") or f_atual.get_email()
                    
                    f_atual.set_nome(nome)
                    f_atual.set_cnpj(cnpj)
                    f_atual.set_telefone(telefone)
                    f_atual.set_email(email)
                    ctrl_fornecedor.atualizar(f_atual)
                    print("Atualizado com sucesso")
                else:
                    print("Não encontrado")
                    
            elif opcao_atualizar == '2':
                id_p = int(input("ID do Produto a atualizar: "))
                p_atual = ctrl_produto.buscar(id_p)
                if p_atual:
                    nome = input(f"Nome atual ({p_atual.get_nome()}): ") or p_atual.get_nome()
                    descricao = input(f"Descrição atual ({p_atual.get_descricao()}): ") or p_atual.get_descricao()
                    preco_str = input(f"Preço atual ({p_atual.get_preco_venda()}): ")
                    preco = float(preco_str) if preco_str else p_atual.get_preco_venda()
                    est_str = input(f"Estoque atual ({p_atual.get_estoque_atual()}): ")
                    estoque = int(est_str) if est_str else p_atual.get_estoque_atual()
                    min_str = input(f"Estoque minimo ({p_atual.get_estoque_minimo()}): ")
                    minimo = int(min_str) if min_str else p_atual.get_estoque_minimo()
                    
                    p_atual.set_nome(nome)
                    p_atual.set_descricao(descricao)
                    p_atual.set_preco_venda(preco)
                    p_atual.set_estoque_atual(estoque)
                    p_atual.set_estoque_minimo(minimo)
                    
                    ctrl_produto.atualizar(p_atual)
                    print("Atualizado com sucesso")
                else:
                    print("Não encontrado")
                    
            elif opcao_atualizar == '3':
                id_c = int(input("ID da Compra a atualizar: "))
                c_atual = ctrl_compra.buscar(id_c)
                if c_atual:
                    id_fornecedor = int(input(f"ID Fornecedor atual ({c_atual.get_fornecedor().get_id_fornecedor()}): ") or c_atual.get_fornecedor().get_id_fornecedor())
                    data_str = input(f"Data atual ({c_atual.get_data_compra().strftime('%d/%m/%Y')}): ")
                    status = input(f"Status atual ({c_atual.get_status()}): ") or c_atual.get_status()
                    
                    data_compra = datetime.strptime(data_str, "%d/%m/%Y").date() if data_str else c_atual.get_data_compra()
                    fornecedor = ctrl_fornecedor.buscar(id_fornecedor)
                    
                    c_atual.set_fornecedor(fornecedor)
                    c_atual.set_data_compra(data_compra)
                    c_atual.set_status(status)
                    
                    ctrl_compra.atualizar(c_atual)
                    print("Atualizado com sucesso")
                else:
                    print("Não encontrado")
                    
            elif opcao_atualizar == '4':
                id_i = int(input("ID do Item a atualizar: "))
                i_atual = ctrl_item_compra.buscar(id_i)
                if i_atual:
                    id_compra = int(input(f"ID Compra atual ({i_atual.get_compra().get_id_compra()}): ") or i_atual.get_compra().get_id_compra())
                    id_produto = int(input(f"ID Produto atual ({i_atual.get_produto().get_id_produto()}): ") or i_atual.get_produto().get_id_produto())
                    qtd_str = input(f"Quantidade atual ({i_atual.get_quantidade()}): ")
                    qtd = int(qtd_str) if qtd_str else i_atual.get_quantidade()
                    preco_str = input(f"Preço Unitário atual ({i_atual.get_preco_unitario()}): ")
                    preco = float(preco_str) if preco_str else i_atual.get_preco_unitario()
                    
                    compra = ctrl_compra.buscar(id_compra)
                    produto = ctrl_produto.buscar(id_produto)
                    
                    i_atual.set_compra(compra)
                    i_atual.set_produto(produto)
                    i_atual.set_quantidade(qtd)
                    i_atual.set_preco_unitario(preco)
                    
                    ctrl_item_compra.atualizar(i_atual)
                    print("Atualizado com sucesso")
                else:
                    print("Não encontrado")
            elif opcao_atualizar == '5':
                continue
            else:
                print("Opção inválida")
            
        elif opcao == '5':
            #sair
            print("Encerrando o programa")
            oracle_fixo.desconectar()
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    run()
