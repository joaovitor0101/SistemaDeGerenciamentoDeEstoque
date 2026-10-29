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

## 2. Alinhamento Arquitetural ao Modelo Entidade-Relacionamento

- **Fonte / Ferramenta:** Google Antigravity (Modelo Gemini)
- **Data da Consulta:** 28/10/2026
- **Prompt Utilizado:**
  > *"Com base no Diagrama Entidade-Relacionamento (DER) elaborado pelo grupo para o Sistema de Gerenciamento de Estoque — composto pelas entidades FORNECEDOR, PRODUTO, COMPRA e ITEM_COMPRA, seus respectivos atributos, domínios de dados, restrições de nulidade (NOT NULL), chaves únicas (UNIQUE), chaves primárias (PK) e chaves estrangeiras (FK) —, adapte a estrutura de módulos do projeto e gere a especificação correspondente em sintaxe Mermaid (diagrama como código) em conformidade com o Item 3 e o Roteiro de Execução do edital."*

## 3. Implementação do Script DDL/DML e Mapeamento Objeto-Relacional Manual

- **Fonte / Ferramenta:** Google Antigravity (Modelo Gemini)
- **Data da Consulta:** 28/10/2026
- **Prompt Utilizado:**
  > *"Elabore os scripts SQL compatíveis com o SGBD Oracle para a Etapa 1 do projeto (sql/create_tables_estoque.sql e sql/inserting_samples_estoque.sql), contemplando comandos de limpeza (DROP com CASCADE CONSTRAINTS), objetos SEQUENCE para geração incremental das chaves primárias e definição explícita das CONSTRAINTS (PRIMARY KEY, FOREIGN KEY e UNIQUE) para as tabelas FORNECEDOR, PRODUTO, COMPRA e ITEM_COMPRA. Em seguida, estruture as classes de domínio da Etapa 2 no pacote src/model/, aplicando encapsulamento (getters e setters), método descritivo to_string() e associação entre objetos por referência de instância."*
-

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

## 4. Implementação do Módulo de Conexão Oracle e Script de Carga Automatizada

- **Fonte / Ferramenta:** Google Antigravity (Modelo Gemini)
- **Data da Consulta:** 29/10/2026
- **Prompt Utilizado:**
  > *"Desenvolva de forma autoral o módulo de conexão direta com o banco de dados Oracle (src/conexion/oracle_queries.py) e o script de inicialização estrutural e carga de registros (src/create_tables_and_records.py), assegurando compatibilidade tanto com o driver moderno python-oracledb quanto com o driver cx_Oracle presente na Máquina Virtual Linux da disciplina, sem qualquer utilização de frameworks ORM."*
- **Análise Crítica e Aplicação pelo Grupo:**
  - O grupo estruturou a classe `ConexaoOracle` com gerenciamento explícito de abertura/fechamento de conexões e cursores (`try/finally`), controle de permissão de escrita (`permite_escrita`), confirmação transacional via `commit()` para comandos DML, consulta tabular retornando `DataFrame` do Pandas e obtenção sequencial de chaves primárias (`NEXTVAL`).
  - No script `create_tables_and_records.py`, implementamos o parser `extrair_comandos_sql()` para higienizar comentários dos scripts `.sql` e tratar de forma resiliente a primeira execução dos comandos `DROP` na VM do laboratório.
