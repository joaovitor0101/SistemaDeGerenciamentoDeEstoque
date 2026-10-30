# Sistema de Gerenciamento de Estoque (Python + Oracle 21c XE)

Aplicação em linha de comando desenvolvida para a disciplina de **Banco de Dados (Semestre 2026/2)**, lecionada pelo **Prof. M.Sc. Howard Roatti**, simulando um sistema real de gerenciamento de estoque e compras com integração direta entre **Python** e o SGBD relacional **Oracle** (sem utilização de frameworks ORM).

---

## 👥 Integrantes do Grupo

- Arthur Gava Calil
- André Luiz Alves Bofonha
- Miguel Gomes
- Kawan Wendler Goldner
- João Vitor Gnocchi da Cunha
- João Vitor Gera Bof

---

## 🎥 Vídeo Demonstrativo (YouTube)

> **Link do vídeo demonstrando todas as funcionalidades e menus:**  
> 🔗 *[Inserir aqui o link do vídeo no YouTube antes do envio final]*

---

## 🏗️ Arquitetura e Organização de Pastas

O projeto está organizado em camadas de responsabilidade bem definidas:

```text
SistemaDeGerenciamentoDeEstoque/
├── diagrams/
│   ├── diagrama_relacional.png                  # Diagrama Entidade-Relacionamento (DER)
│   └── diagrama_relacional.mmd                  # Modelo relacional em código Mermaid
├── sql/
│   ├── create_tables_estoque.sql                # Script DDL (SEQUENCES, TABELAS, PK, FK e UNIQUE)
│   └── inserting_samples_estoque.sql            # Script DML com carga inicial de dados para testes
├── src/
│   ├── conexion/
│   │   └── oracle_queries.py                    # Classe ConexaoOracle (conexão direta via SQL puro)
│   ├── model/
│   │   ├── fornecedor.py                        # Entidade Fornecedor
│   │   ├── produto.py                           # Entidade Produto
│   │   ├── compra.py                            # Entidade Compra (associada a instância de Fornecedor)
│   │   └── item_compra.py                       # Entidade ItemCompra (associada a Compra e Produto)
│   ├── controller/
│   │   ├── controller_fornecedor.py             # Operações CRUD da tabela FORNECEDOR
│   │   ├── controller_produto.py                # Operações CRUD da tabela PRODUTO
│   │   ├── controller_compra.py                 # Operações CRUD e validações da tabela COMPRA
│   │   └── controller_item_compra.py            # Operações CRUD e validações da tabela ITEM_COMPRA
│   ├── sql/
│   │   ├── relatorio_compras_por_fornecedor.sql # Consulta de sumarização (GROUP BY + COUNT + SUM)
│   │   ├── relatorio_itens_compra.sql           # Consulta com junção de 4 tabelas (INNER JOIN)
│   │   ├── relatorio_estoque_baixo.sql          # Consulta de produtos com saldo <= estoque mínimo
│   │   ├── relatorio_fornecedores.sql           # Listagem isolada de todos os fornecedores
│   │   ├── relatorio_produtos.sql               # Listagem isolada de todos os produtos
│   │   └── relatorio_compras.sql                # Listagem isolada de todas as compras
│   ├── reports/
│   │   └── relatorios.py                        # Leitura dos arquivos .sql e exibição tabular com Pandas
│   ├── utils/
│   │   ├── config.py                            # Definição dos menus e limpeza de tela multiplataforma
│   │   └── splash_screen.py                     # Tela inicial com contagem dinâmica (SELECT COUNT(1))
│   ├── create_tables_and_records.py             # Script automatizado de criação e carga inicial do banco
│   └── principal.py                             # Ponto de entrada e controle dos fluxos de menu
├── tests/
│   └── test_controllers.py                      # Testes automatizados de validação dos controllers
├── requirements.txt                             # Dependências Python do projeto
├── PROMPTS.md                                   # Registro transparente do uso de IA Generativa
└── README.md                                    # Documentação de instalação e utilização no Linux
```

---

## 🗄️ Modelo Relacional do Banco de Dados

O sistema gerencia **4 tabelas relacionais** interligadas por chaves primárias (`PK` controladas por `SEQUENCE`) e chaves estrangeiras (`FK`):

1. **`FORNECEDOR`**: Armazena os dados cadastrais dos fornecedores (`id_fornecedor` PK, `nome`, `cnpj` UNIQUE, `telefone`, `email`).
2. **`PRODUTO`**: Armazena o catálogo de produtos e seus níveis de estoque (`id_produto` PK, `nome`, `descricao`, `preco_venda`, `estoque_atual`, `estoque_minimo`).
3. **`COMPRA`**: Registra os pedidos de compra realizados junto a um fornecedor (`id_compra` PK, `id_fornecedor` FK → `FORNECEDOR`, `data_compra`, `status`).
4. **`ITEM_COMPRA`**: Tabela associativa que registra os produtos adquiridos em cada compra, suas quantidades e preços praticados (`id_item` PK, `id_compra` FK → `COMPRA`, `id_produto` FK → `PRODUTO`, `quantidade`, `preco_unitario`).

Visualização completa disponível em [diagrams/diagrama_relacional.png](diagrams/diagrama_relacional.png) e [diagrams/diagrama_relacional.mmd](diagrams/diagrama_relacional.mmd).

---

## 🐧 Passo a Passo para Executar no Linux (VM da Disciplina)

### 1. Iniciar o Banco de Dados Oracle 21c XE na VM
Abra o terminal no Linux da Máquina Virtual da disciplina e verifique se o serviço/container do Oracle está em execução na porta `1521`:

```bash
# Caso o Oracle esteja em container Docker na VM:
docker ps -a
# Se o container estiver parado (Exited), inicie-o e aguarde ~30 segundos:
docker start $(docker ps -aq)

# Ou, caso utilize o serviço nativo do Oracle XE no Linux:
sudo systemctl start oracle-xe-21c
```

### 2. Clonar o Repositório e Configurar o Ambiente Python
No terminal do Linux, execute:

```bash
git clone https://github.com/joaovitor0101/SistemaDeGerenciamentoDeEstoque.git
cd SistemaDeGerenciamentoDeEstoque

# Criar e ativar o ambiente virtual (opcional caso já exista na VM):
python3 -m venv .venv
source .venv/bin/activate

# Instalar as dependências:
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Conexão (Opcional)
O módulo `src/conexion/oracle_queries.py` já vem pré-configurado por padrão para o ambiente da VM da disciplina:
- **Host:** `localhost`
- **Porta:** `1521`
- **Service Name:** `XEPDB1`
- **Usuário:** `labdatabase`
- **Senha:** `lab@Database2025`

*(Caso seja necessário alterar algum parâmetro sem editar o código, basta exportar as variáveis `ORACLE_HOST`, `ORACLE_PORT`, `ORACLE_SERVICE`, `ORACLE_USER` ou `ORACLE_PASSWORD` no terminal).*

### 4. Criar as Tabelas e Inserir os Registros Iniciais
Execute o script abaixo para criar automaticamente as `SEQUENCES`, as 4 tabelas com seus relacionamentos e inserir os dados iniciais de exemplo:

```bash
cd src
python3 create_tables_and_records.py
```
> **Atenção:** Este script recria as tabelas do zero (`DROP` + `CREATE` + `INSERT`). Execute-o na primeira vez que for testar o projeto ou quando quiser restaurar a massa de dados original.

### 5. Iniciar o Sistema Principal
Ainda dentro da pasta `src/` (ou a partir da raiz do projeto com `python3 src/principal.py`), execute:

```bash
python3 principal.py
```

---

## ⚙️ Como Funciona o Sistema (Fluxo dos Menus)

1. **Splash Screen (Tela de Inicialização):**
   Ao abrir o programa (e após ciclos de alterações), o sistema executa `SELECT COUNT(1)` em cada uma das 4 tabelas no Oracle e exibe a contagem atualizada de registros, identificando se cada tabela possui registros ou está vazia, além das informações da disciplina, professor e integrantes.

2. **Opção `1` — Relatórios:**
   - **1 - Relatório de Compras Agrupado por Fornecedor (`GROUP BY`):** Sumariza a quantidade de compras e o valor financeiro total comprado de cada fornecedor.
   - **2 - Relatório Detalhado de Itens de Compra (`JOIN`):** Realiza a junção entre `COMPRA`, `FORNECEDOR`, `ITEM_COMPRA` e `PRODUTO`, exibindo cada item adquirido e seu subtotal.
   - **3 - Relatório de Produtos com Estoque Baixo:** Lista os produtos cujo `estoque_atual` está menor ou igual ao `estoque_minimo`, destacando o déficit de reposição.
   - **4 - Relatório de Fornecedores:** Lista isoladamente todos os fornecedores cadastrados.
   - **5 - Relatório de Produtos:** Lista isoladamente todos os produtos e saldos em estoque.
   - **6 - Relatório de Compras:** Lista isoladamente todas as compras registradas e seus status.

3. **Opção `2` — Inserir Registros:**
   Permite cadastrar novos registros em `FORNECEDOR`, `PRODUTO`, `COMPRA` ou `ITEM_COMPRA` utilizando as `SEQUENCES` do Oracle, validando os campos obrigatórios e chaves estrangeiras, exibindo o registro inserido e perguntando ao final se o usuário deseja inserir mais registros (`[S/N]`).

4. **Opção `3` — Remover Registros (com Tratamento de Chave Estrangeira - FK):**
   Lista os registros existentes da entidade escolhida, solicita o ID e pede confirmação (`[S/N]`). Caso o registro possua dependências em tabelas filhas (`COMPRA` ou `ITEM_COMPRA`), o sistema alerta sobre o vínculo de chave estrangeira, exibe os registros dependentes e pergunta se o usuário deseja removê-los em cascata antes de concluir a exclusão. Ao final, pergunta se deseja excluir mais algum registro (`[S/N]`).

5. **Opção `4` — Atualizar Registros:**
   Lista os registros cadastrados, permite selecionar pelo ID e atualizar os atributos desejados (mantendo o valor atual caso o usuário pressione `Enter`), **exibe o registro atualizado** na tela e pergunta se deseja atualizar mais algum registro (`[S/N]`).

6. **Opção `5` — Sair:**
   Exibe a tela atualizada de registros, encerra a conexão com o Oracle de forma segura e finaliza a aplicação.

