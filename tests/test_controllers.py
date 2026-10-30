"""Testes locais com SQL real no SQLite; nao substituem teste no Oracle da VM."""
import sqlite3
import sys
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from controller.controller_compra import ControllerCompra, executar
from controller.controller_item_compra import ControllerItemCompra
from model.compra import Compra
from model.fornecedor import Fornecedor
from model.item_compra import ItemCompra
from model.produto import Produto

sqlite3.register_adapter(Decimal, str)
sqlite3.register_adapter(date, lambda valor: valor.isoformat())
sqlite3.register_converter('DATE', lambda valor: date.fromisoformat(valor.decode()))


class BancoTeste:
    def __init__(self):
        self.permite_escrita = True
        self.conexao = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
        self.conexao.execute('PRAGMA foreign_keys=ON')
        self.conexao.executescript('''
            CREATE TABLE FORNECEDOR (id_fornecedor INTEGER PRIMARY KEY, nome TEXT,
                cnpj TEXT, telefone TEXT, email TEXT);
            CREATE TABLE PRODUTO (id_produto INTEGER PRIMARY KEY, nome TEXT,
                descricao TEXT, preco_venda NUMERIC, estoque_atual INTEGER, estoque_minimo INTEGER);
            CREATE TABLE COMPRA (id_compra INTEGER PRIMARY KEY,
                id_fornecedor INTEGER REFERENCES FORNECEDOR, data_compra DATE, status TEXT);
            CREATE TABLE ITEM_COMPRA (id_item INTEGER PRIMARY KEY,
                id_compra INTEGER REFERENCES COMPRA, id_produto INTEGER REFERENCES PRODUTO,
                quantidade INTEGER, preco_unitario NUMERIC);
            INSERT INTO FORNECEDOR VALUES (1, 'Fornecedor teste', '123', NULL, NULL);
            INSERT INTO PRODUTO VALUES (1, 'Produto teste', NULL, 10, 20, 5);
        ''')
        self.sequences = {}
        self.fechamentos = 0

    def conectar(self):
        return self.conexao.cursor()

    def desconectar(self):
        # Mantem o banco em memoria vivo entre as operacoes do teste.
        self.fechamentos += 1

    def obter_proximo_id(self, nome):
        self.sequences[nome] = self.sequences.get(nome, 0) + 1
        return self.sequences[nome]


class ControllersTest(unittest.TestCase):
    def setUp(self):
        self.banco = BancoTeste()
        self.compras = ControllerCompra(self.banco)
        self.itens = ControllerItemCompra(self.banco)

    def tearDown(self):
        self.banco.conexao.close()

    def compra(self):
        return self.compras.inserir(Compra(None, Fornecedor(1), date(2026, 10, 29), 'PENDENTE'))

    def test_ciclo_compra_e_texto_com_aspas(self):
        compra = self.compra()
        compra.set_status("EM 'TESTE'")
        salvo = self.compras.atualizar(compra)
        self.assertEqual(salvo.get_status(), "EM 'TESTE'")
        self.assertEqual(salvo.get_fornecedor().get_nome(), 'Fornecedor teste')
        self.assertEqual(len(self.compras.listar()), 1)
        self.assertTrue(self.compras.existe(compra.get_id_compra()))
        self.assertTrue(self.compras.excluir(compra.get_id_compra()))
        self.assertIsNone(self.compras.buscar(compra.get_id_compra()))

    def test_ciclo_item_e_bloqueio_de_exclusao_da_compra(self):
        compra = self.compra()
        item = self.itens.inserir(ItemCompra(None, compra, Produto(1), 3, Decimal('12.50')))
        with self.assertRaisesRegex(ValueError, 'possui itens'):
            self.compras.excluir(compra.get_id_compra())
        self.assertEqual(len(self.itens.listar(compra.get_id_compra())), 1)
        self.assertEqual(self.itens.listar(999), [])
        item.set_quantidade(4)
        atualizado = self.itens.atualizar(item)
        self.assertEqual(atualizado.get_quantidade(), 4)
        self.assertEqual(atualizado.get_produto().get_nome(), 'Produto teste')
        self.assertEqual(atualizado.get_compra().get_fornecedor().get_nome(), 'Fornecedor teste')
        self.assertEqual(self.banco.conexao.execute('SELECT estoque_atual FROM PRODUTO').fetchone()[0], 20)
        self.itens.excluir(item.get_id_item())
        self.assertIsNone(self.itens.buscar(item.get_id_item()))
        self.compras.excluir(compra.get_id_compra())

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
