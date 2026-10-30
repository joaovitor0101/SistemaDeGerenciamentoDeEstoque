"""Testes automatizados cobrindo CRUD nas 4 tabelas, FKs, SplashScreen e Relatórios."""
import io
import sqlite3
import sys
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from controller.controller_fornecedor import ControllerFornecedor
from controller.controller_produto import ControllerProduto
from controller.controller_compra import ControllerCompra, executar
from controller.controller_item_compra import ControllerItemCompra
from model.compra import Compra
from model.fornecedor import Fornecedor
from model.item_compra import ItemCompra
from model.produto import Produto
from reports.relatorios import Relatorio
from utils.splash_screen import SplashScreen

sqlite3.register_adapter(Decimal, str)
sqlite3.register_adapter(date, lambda valor: valor.isoformat())
sqlite3.register_converter('DATE', lambda valor: date.fromisoformat(valor.decode()))


class BancoTeste:
    def __init__(self):
        self.permite_escrita = True
        self.conexao = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
        self.conexao.execute('PRAGMA foreign_keys=ON')
        # Registra NVL no SQLite para validar tambem os SQLs nativos de relatorio do Oracle
        self.conexao.create_function('NVL', 2, lambda a, b: b if a is None else a)
        self.conexao.executescript('''
            CREATE TABLE FORNECEDOR (id_fornecedor INTEGER PRIMARY KEY, nome TEXT NOT NULL,
                cnpj TEXT UNIQUE NOT NULL, telefone TEXT, email TEXT);
            CREATE TABLE PRODUTO (id_produto INTEGER PRIMARY KEY, nome TEXT NOT NULL,
                descricao TEXT, preco_venda NUMERIC NOT NULL, estoque_atual INTEGER NOT NULL,
                estoque_minimo INTEGER NOT NULL);
            CREATE TABLE COMPRA (id_compra INTEGER PRIMARY KEY,
                id_fornecedor INTEGER NOT NULL REFERENCES FORNECEDOR, data_compra DATE NOT NULL,
                status TEXT NOT NULL);
            CREATE TABLE ITEM_COMPRA (id_item INTEGER PRIMARY KEY,
                id_compra INTEGER NOT NULL REFERENCES COMPRA,
                id_produto INTEGER NOT NULL REFERENCES PRODUTO,
                quantidade INTEGER NOT NULL, preco_unitario NUMERIC NOT NULL);
            INSERT INTO FORNECEDOR VALUES (1, 'Fornecedor teste', '12345678000199', '2733330000', 'teste@forn.com');
            INSERT INTO PRODUTO VALUES (1, 'Produto teste', 'Descricao inicial', 10.50, 4, 5);
        ''')
        self.sequences = {'SEQ_FORNECEDOR': 1, 'SEQ_PRODUTO': 1}
        self.fechamentos = 0

    def conectar(self):
        return self.conexao.cursor()

    def desconectar(self):
        self.fechamentos += 1

    def obter_proximo_id(self, nome):
        self.sequences[nome] = self.sequences.get(nome, 0) + 1
        return self.sequences[nome]

    def consultar(self, sql, parametros=None):
        cursor = self.conectar()
        try:
            cursor.execute(sql, parametros or {})
            linhas = cursor.fetchall()
            colunas = [col[0].lower() for col in cursor.description]
            return pd.DataFrame(linhas, columns=colunas)
        finally:
            cursor.close()
            self.desconectar()


class ControllersTest(unittest.TestCase):
    def setUp(self):
        self.banco = BancoTeste()
        self.fornecedores = ControllerFornecedor(self.banco)
        self.produtos = ControllerProduto(self.banco)
        self.compras = ControllerCompra(self.banco)
        self.itens = ControllerItemCompra(self.banco)

    def tearDown(self):
        self.banco.conexao.close()

    def compra(self):
        return self.compras.inserir(Compra(None, Fornecedor(1), date(2026, 10, 29), 'PENDENTE'))

    def test_crud_completo_fornecedor_e_bloqueio_fk(self):
        novo = self.fornecedores.inserir(
            Fornecedor(None, 'Fornecedor Dois', '98765432000188', '11999990000', 'dois@forn.com')
        )
        self.assertEqual(novo.get_id_fornecedor(), 2)
        self.assertIn('Fornecedor Dois', novo.to_string())
        self.assertEqual(len(self.fornecedores.listar()), 2)

        novo.set_nome('Fornecedor Dois Atualizado')
        atualizado = self.fornecedores.atualizar(novo)
        self.assertEqual(atualizado.get_nome(), 'Fornecedor Dois Atualizado')

        # Vincula uma compra e verifica bloqueio de exclusao por FK
        compra_vinculada = self.compras.inserir(Compra(None, atualizado, date(2026, 10, 29), 'CONCLUIDA'))
        with self.assertRaisesRegex(ValueError, 'possui compras'):
            self.fornecedores.excluir(novo.get_id_fornecedor())

        # Remove a compra filha e entao remove o fornecedor
        self.compras.excluir(compra_vinculada.get_id_compra())
        self.assertTrue(self.fornecedores.excluir(novo.get_id_fornecedor()))
        self.assertIsNone(self.fornecedores.buscar(novo.get_id_fornecedor()))

    def test_crud_completo_produto_e_bloqueio_fk(self):
        novo = self.produtos.inserir(
            Produto(None, 'Teclado Gamer', 'Switch Red', 199.90, 15, 5)
        )
        self.assertEqual(novo.get_id_produto(), 2)
        self.assertIn('199.90', novo.to_string())
        self.assertEqual(len(self.produtos.listar()), 2)

        novo.set_estoque_atual(22)
        novo.set_preco_venda(210.00)
        atualizado = self.produtos.atualizar(novo)
        self.assertEqual(atualizado.get_estoque_atual(), 22)
        self.assertEqual(atualizado.get_preco_venda(), 210.00)

        # Vincula um item de compra e verifica bloqueio de exclusao por FK
        compra = self.compra()
        item = self.itens.inserir(ItemCompra(None, compra, atualizado, 2, 120.00))
        with self.assertRaisesRegex(ValueError, 'possui itens'):
            self.produtos.excluir(atualizado.get_id_produto())

        # Remove o item filho e entao remove o produto
        self.itens.excluir(item.get_id_item())
        self.assertTrue(self.produtos.excluir(atualizado.get_id_produto()))
        self.assertIsNone(self.produtos.buscar(atualizado.get_id_produto()))

    def test_ciclo_compra_e_texto_com_aspas(self):
        compra = self.compra()
        compra.set_status("EM 'TESTE'")
        salvo = self.compras.atualizar(compra)
        self.assertEqual(salvo.get_status(), "EM 'TESTE'")
        self.assertEqual(salvo.get_fornecedor().get_nome(), 'Fornecedor teste')
        self.assertIn('29/10/2026', salvo.to_string())
        self.assertEqual(len(self.compras.listar()), 1)
        self.assertTrue(self.compras.existe(compra.get_id_compra()))
        self.assertTrue(self.compras.excluir(compra.get_id_compra()))
        self.assertIsNone(self.compras.buscar(compra.get_id_compra()))

    def test_ciclo_item_e_bloqueio_de_exclusao_da_compra(self):
        compra = self.compra()
        item = self.itens.inserir(ItemCompra(None, compra, Produto(1), 3, Decimal('12.50')))
        self.assertIn('12.50', item.to_string())
        with self.assertRaisesRegex(ValueError, 'possui itens'):
            self.compras.excluir(compra.get_id_compra())
        self.assertEqual(len(self.itens.listar(id_compra=compra.get_id_compra())), 1)
        self.assertEqual(self.itens.listar(id_compra=999), [])
        item.set_quantidade(4)
        atualizado = self.itens.atualizar(item)
        self.assertEqual(atualizado.get_quantidade(), 4)
        self.assertEqual(atualizado.get_produto().get_nome(), 'Produto teste')
        self.assertEqual(atualizado.get_compra().get_fornecedor().get_nome(), 'Fornecedor teste')
        self.itens.excluir(item.get_id_item())
        self.assertIsNone(self.itens.buscar(item.get_id_item()))
        self.compras.excluir(compra.get_id_compra())

    def test_splash_screen_e_tres_relatorios(self):
        compra = self.compra()
        self.itens.inserir(ItemCompra(None, compra, Produto(1), 5, 8.00))

        tela = SplashScreen(conexao=self.banco).get_updated_screen()
        self.assertIn('COM REGISTROS', tela)
        self.assertIn('FORNECEDOR', tela)
        self.assertIn('ITEM_COMPRA', tela)

        saida = io.StringIO()
        relatorio = Relatorio(conexao=self.banco, saida=saida)
        relatorio.get_relatorio_compras_por_fornecedor()
        relatorio.get_relatorio_itens_compra()
        relatorio.get_relatorio_estoque_baixo()
        texto_relatorios = saida.getvalue()
        self.assertIn('Fornecedor teste', texto_relatorios)
        self.assertIn('Produto teste', texto_relatorios)
        self.assertIn('40', texto_relatorios)

    def test_rejeita_referencias_inexistentes(self):
        with self.assertRaisesRegex(ValueError, 'Fornecedor nao encontrado'):
            self.compras.inserir(Compra(None, Fornecedor(999), date.today(), 'PENDENTE'))
        compra = self.compra()
        with self.assertRaisesRegex(ValueError, 'Produto nao encontrado'):
            self.itens.inserir(ItemCompra(None, compra, Produto(999), 1, 10))
        with self.assertRaisesRegex(ValueError, 'Compra nao encontrada'):
            self.itens.inserir(ItemCompra(None, Compra(999), Produto(1), 1, 10))

    def test_validacoes_de_quantidade_preco_e_id(self):
        compra = self.compra()
        for quantidade in (0, -1, True, 1.5, '2'):
            with self.subTest(quantidade=quantidade), self.assertRaises(ValueError):
                self.itens.inserir(ItemCompra(None, compra, Produto(1), quantidade, 10))
        for preco in (0, -1, True, 'NaN', 'Infinity', '1.234', '100000000', None):
            with self.subTest(preco=preco), self.assertRaises(ValueError):
                self.itens.inserir(ItemCompra(None, compra, Produto(1), 1, preco))
        with self.assertRaises(ValueError):
            self.compras.buscar('1 OR 1=1')

    def test_ausencia_e_protecao_de_pk(self):
        compra = self.compra()
        with self.assertRaises(ValueError):
            self.compras.inserir(compra)
        compra.set_id_compra(999)
        with self.assertRaisesRegex(ValueError, 'nao encontrada'):
            self.compras.atualizar(compra)
        with self.assertRaises(ValueError):
            self.itens.excluir(999)

    def test_rollback_e_fechamento_apos_erro_sql(self):
        antes = self.banco.fechamentos
        with self.assertRaises(sqlite3.IntegrityError):
            executar(self.banco, "INSERT INTO COMPRA VALUES (1,999,:data,'PENDENTE')",
                     {'data': date.today()}, escrita=True)
        self.assertEqual(self.banco.conexao.execute('SELECT COUNT(*) FROM COMPRA').fetchone()[0], 0)
        self.assertEqual(self.banco.fechamentos, antes + 1)

    def test_permissao_de_escrita(self):
        self.banco.permite_escrita = False
        with self.assertRaises(PermissionError):
            self.compra()
        self.assertEqual(self.compras.listar(), [])


if __name__ == '__main__':
    unittest.main()
