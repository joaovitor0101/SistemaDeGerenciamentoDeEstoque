# Documentação de Transparência e Uso de IA Generativa (`PROMPTS.md`)

**Disciplina:** Banco de Dados (Semestre 2026/2)  
**Professor:** Prof. M.Sc. Howard Roatti  
**Projeto:** Sistema de Gerenciamento e Controle de Estoque  

Em cumprimento ao **Item 8 — Observação Importante (5)** do edital da disciplina, este documento registra de forma transparente e detalhada os prompts submetidos a ferramentas de Inteligência Artificial Generativa como suporte técnico ao desenvolvimento, especificando a ferramenta utilizada, o objetivo técnico da consulta e o trabalho de revisão, adaptação e implementação conduzido pelos integrantes do grupo.

---

## 1. Interpretação de Requisitos do Edital e Arquitetura de Diretórios

- **Fonte / Ferramenta:** Google Antigravity (Modelo Gemini)
- **Data da Consulta:** 28/10/2026
- **Prompt Utilizado:**
  > *"Realize uma análise técnica minuciosa do edital da disciplina de Banco de Dados referente ao desenvolvimento de uma aplicação CRUD integrada ao banco de dados relacional Oracle. Nosso grupo é composto por 5 integrantes e desenvolverá o tema 'Sistema de Gerenciamento de Estoque'. Estruture a organização modular de diretórios seguindo o padrão arquitetural de separação de responsabilidades (conexion, model, controller, reports, sql e utils) apresentado no repositório de referência do professor (https://github.com/howardroatti/example_crud_oracle)."*

---

## 2. Alinhamento Arquitetural ao Modelo Entidade-Relacionamento

- **Fonte / Ferramenta:** Google Antigravity (Modelo Gemini)
- **Data da Consulta:** 28/10/2026
- **Prompt Utilizado:**
  > *"Com base no Diagrama Entidade-Relacionamento (DER) elaborado pelo grupo para o Sistema de Gerenciamento de Estoque — composto pelas entidades FORNECEDOR, PRODUTO, COMPRA e ITEM_COMPRA, seus respectivos atributos, domínios de dados, restrições de nulidade (NOT NULL), chaves únicas (UNIQUE), chaves primárias (PK) e chaves estrangeiras (FK) —, adapte a estrutura de módulos do projeto e gere a especificação correspondente em sintaxe Mermaid (diagrama como código) em conformidade com o Item 3 e o Roteiro de Execução do edital."*

---

## 3. Implementação do Script DDL/DML e Mapeamento Objeto-Relacional Manual

- **Fonte / Ferramenta:** Google Antigravity (Modelo Gemini)
- **Data da Consulta:** 28/10/2026
- **Prompt Utilizado:**
  > *"Elabore os scripts SQL compatíveis com o SGBD Oracle para a Etapa 1 do projeto (sql/create_tables_estoque.sql e sql/inserting_samples_estoque.sql), contemplando comandos de limpeza (DROP com CASCADE CONSTRAINTS), objetos SEQUENCE para geração incremental das chaves primárias e definição explícita das CONSTRAINTS (PRIMARY KEY, FOREIGN KEY e UNIQUE) para as tabelas FORNECEDOR, PRODUTO, COMPRA e ITEM_COMPRA. Em seguida, estruture as classes de domínio da Etapa 2 no pacote src/model/, aplicando encapsulamento (getters e setters), método descritivo to_string() e associação entre objetos por referência de instância."*

---

## 4. Implementação do Módulo de Conexão Oracle e Script de Carga Automatizada

- **Fonte / Ferramenta:** Google Antigravity (Modelo Gemini)
- **Data da Consulta:** 29/10/2026
- **Prompt Utilizado:**
  > *"Desenvolva de forma autoral o módulo de conexão direta com o banco de dados Oracle (src/conexion/oracle_queries.py) e o script de inicialização estrutural e carga de registros (src/create_tables_and_records.py), assegurando compatibilidade tanto com o driver moderno python-oracledb quanto com o driver cx_Oracle presente na Máquina Virtual Linux da disciplina, sem qualquer utilização de frameworks ORM."*
- **Análise Crítica e Aplicação pelo Grupo:**
  - O grupo estruturou a classe `ConexaoOracle` com gerenciamento explícito de abertura/fechamento de conexões e cursores (`try/finally`), controle de permissão de escrita (`permite_escrita`), confirmação transacional via `commit()` para comandos DML, consulta tabular retornando `DataFrame` do Pandas e obtenção sequencial de chaves primárias (`NEXTVAL`).
  - No script `create_tables_and_records.py`, implementamos o parser `extrair_comandos_sql()` para higienizar comentários dos scripts `.sql` e tratar de forma resiliente a primeira execução dos comandos `DROP` na VM do laboratório.

---

## 5. Parte 4 — Controllers de Compra e Item de Compra

- **Fonte / Ferramenta:** ChatGPT/Codex.
- **Data da consulta:** 29/10/2026.
- **Responsável pela parte:** Miguel (`miguelgomessilveira7-cmd`).
- **Registro das solicitações:** síntese técnica dos pedidos da conversa, revisada para documentação; não constitui transcrição literal.

### Solicitações de desenvolvimento

- Analisar os modelos, os scripts SQL e o módulo de conexão existentes para implementar os controllers de compra e item de compra de acordo com a estrutura do grupo.
- Implementar inclusão, consulta, listagem, atualização e exclusão, preservando as associações entre objetos e validando os dados e as referências entre entidades.
- Documentar a interface dos controllers para integração ao menu principal e orientar a validação em ambiente local e no Oracle da VM da disciplina.

### Aplicação do apoio de IA

Foram implementadas as classes `ControllerCompra` e `ControllerItemCompra`, nos arquivos `src/controller/controller_compra.py` e `src/controller/controller_item_compra.py`, reutilizando o módulo `ConexaoOracle` do grupo. O apoio também produziu os testes em `tests/test_controllers.py` e as orientações de integração consolidadas nesta seção.

A implementação utiliza SQL manual com parâmetros vinculados, IDs gerados pelas sequences `SEQ_COMPRA` e `SEQ_ITEM_COMPRA`, confirmação das escritas com `commit()`, `rollback()` em caso de erro e fechamento da conexão após as operações.

Foram adotadas as seguintes validações:

- Existência do fornecedor, da compra e do produto referenciados.
- Quantidade inteira positiva e preço positivo de até `99999999.99`, com no máximo duas casas decimais.
- Data representada por `datetime.date` ou `datetime.datetime` e status não vazio de até 12 caracteres.
- Bloqueio da exclusão de uma compra que ainda possui itens.

A movimentação automática de estoque não foi implementada nesta parte; depende de definição do grupo sobre compras pendentes, concluídas e canceladas.

### Interface documentada para integração

Ambos os controllers disponibilizam `inserir(objeto)`, `buscar(id)`, `listar()`, `existe(id)`, `atualizar(objeto)` e `excluir(id)`. A inclusão recebe um objeto com ID `None` e devolve o objeto com o ID gerado; a busca devolve um objeto com suas associações ou `None`; a listagem devolve uma lista; a verificação de existência devolve um booleano; a atualização devolve o registro relido; e a exclusão devolve `True` ou levanta `ValueError` quando não há registro ou existe bloqueio. `ControllerItemCompra.listar(id_compra)` também permite filtrar os itens de uma compra.

As orientações produzidas para o menu incluem exibir os objetos com `to_string()`, preservar o ID na atualização, solicitar confirmação antes de excluir, tratar erros de validação e do banco e oferecer repetição das operações. Essas orientações descrevem a integração esperada; não comprovam a validação do menu completo.

### Validação realizada

Os testes automatizados com SQLite em memória passaram localmente e na VM, exercitando CRUD, associações, validações, bloqueio de exclusão, permissão de escrita e rollback. Para repetir os testes, executar na raiz do projeto:

```sh
python -m unittest discover -s tests -v
```

Para a validação no Oracle, o integrante executou os comandos orientados na VM e compartilhou as saídas no chat. Foram conferidos os seguintes resultados:

- Conexão confirmada por `SELECT 1 AS teste FROM DUAL` e inicialização das tabelas e dos dados em banco de teste.
- Listagem das compras e dos itens com os dados associados de fornecedor e produto.
- Inclusão e consulta da compra de teste 4 e do item de teste 5.
- Atualização do status da compra para `PENDENTE` e da quantidade do item para 3.
- Bloqueio da exclusão da compra enquanto havia um item associado.
- Exclusão do item e, em seguida, da compra; as buscas finais retornaram `None` para ambos.

Para repetir a validação no Oracle, configurar as variáveis `ORACLE_HOST`, `ORACLE_PORT`, `ORACLE_SERVICE`, `ORACLE_USER` e `ORACLE_PASSWORD`, instalar `requirements.txt` e utilizar as tabelas e sequences do projeto em um banco de teste. O script `create_tables_and_records.py` remove e recria tabelas e não deve ser executado sobre dados a preservar.

Esses resultados validam os cenários exercitados nos controllers. A validação completa pelo menu principal deve ser realizada pelo grupo. A ferramenta não acessou diretamente a VM; a conferência dos resultados no Oracle foi feita a partir das saídas fornecidas pelo integrante.

---

## 6. Revisão de Integração Final, Otimização e Documentação (`README.md`)

- **Fonte / Ferramenta:** Google Antigravity (Modelo Gemini)
- **Data da Consulta:** 29/10/2026 - 30/10/2026
- **Prompt Utilizado:**
  > *"Aplique as correções de integração no menu principal (src/principal.py), realize uma varredura completa em todos os códigos eliminando redundâncias e otimizando consultas, valide a compatibilidade de execução no Linux da VM e elabore o README.md detalhando o funcionamento passo a passo do sistema."*
- **Análise Crítica e Aplicação pelo Grupo:**
  - Unificamos o gerenciamento de conexões para utilizar uma única instância de `ConexaoOracle` em todos os módulos (`SplashScreen`, `Relatorio` e os 4 `Controllers`), eliminando conexões paralelas ociosas e consultas `N+1` na listagem de `ItemCompra`.
  - Completamos todos os requisitos funcionais do edital em `src/principal.py` (listagem prévia de registros, confirmação de exclusão, tratamento de chaves estrangeiras com opção de exclusão em cascata dos filhos, exibição do registro atualizado via `to_string()` e loops de repetição das operações), expandimos a suíte automatizada para 10 testes cobrindo as 4 tabelas e redigimos o guia completo de execução em Linux no `README.md`.
