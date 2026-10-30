# Parte 4 - Controllers de compra e item de compra

Implementacao local com cenarios de CRUD testados no Oracle da VM em 29/10/2026.
Ainda falta integrar e testar o fluxo completo com o menu principal.
Os demais arquivos do grupo foram preservados. A integracao ao menu deve considerar
as interfaces descritas abaixo.

## Interface para combinar com a pessoa 5

As classes sao `ControllerCompra` e `ControllerItemCompra`, nos arquivos
`src/controller/controller_compra.py` e `src/controller/controller_item_compra.py`.
Ambas oferecem:

- `inserir(objeto)`: recebe Compra ou ItemCompra com ID None; devolve o objeto com ID da sequence.
- `buscar(id)`: devolve um objeto com suas associacoes ou None.
- `listar()`: devolve uma lista de objetos.
- `existe(id)`: devolve True ou False.
- `atualizar(objeto)`: recebe o objeto com ID existente e devolve o registro relido do banco.
- `excluir(id)`: devolve True; levanta ValueError se nao existir ou houver bloqueio.
- `ControllerItemCompra.listar(id_compra)`: filtra os itens por compra.

O menu deve listar os objetos com `to_string()`, solicitar os dados, pedir
confirmacao ANTES de chamar excluir, tratar ValueError/erros do banco e perguntar
se o usuario deseja repetir. Essa parte de interface pertence a pessoa 5.
Na atualizacao, o menu deve preservar o ID original do registro.

## Exemplo de integracao (executar a partir da raiz)

```python
# Em src/principal.py, futuramente:
from datetime import date
from controller.controller_compra import ControllerCompra
from model.compra import Compra
from model.fornecedor import Fornecedor

controller = ControllerCompra()
# O fornecedor 1 deve existir. O metodo valida sua existencia.
compra = Compra(None, Fornecedor(id_fornecedor=1), date.today(), 'PENDENTE')
# Este comando GRAVA no banco quando for executado:
# compra = controller.inserir(compra)
```

## Regras adotadas

- SQL manual com bind parameters para preservar textos com aspas e evitar injecao.
  A conexao existente e reutilizada sem alterar seu arquivo.
- IDs automaticos: SEQ_COMPRA e SEQ_ITEM_COMPRA.
- Quantidade inteira positiva; preco positivo de ate 99999999.99, com no maximo duas casas.
- Data e um objeto datetime.date; status nao vazio de ate 12 caracteres.
- Fornecedor, compra e produto referenciados precisam existir.
- Compra com itens nao pode ser excluida. Excluir os itens primeiro, com confirmacao no menu.
- Nao altera estoque automaticamente. Essa regra depende de decisao do grupo
  sobre compras pendentes/concluidas e alteracoes/cancelamentos.
- Cada escrita tem commit no banco, rollback em erro e fechamento da conexao.
  Commit do banco confirma registros; nao e um commit Git/GitHub.

## Testes locais

```sh
python -m unittest discover -s tests -v
```

Os testes usam SQLite em memoria com chaves estrangeiras ativas, sem instalar
Oracle. Exercitam CRUD, associacoes, validacoes, exclusao bloqueada e rollback.
Nao comprovam configuracao ou funcionamento do driver Oracle na VM.

## Validacao realizada na VM

O integrante executou os comandos na VM e compartilhou as saidas no chat:

- 7 testes automatizados passaram na VM, usando SQLite em memoria.
- A consulta SELECT 1 AS teste FROM DUAL confirmou a conexao com o Oracle.
- As compras e os itens iniciais foram listados com fornecedor e produto.
- Compra 4 e item 5 foram cadastrados e consultados no Oracle.
- O status da compra mudou para PENDENTE e a quantidade do item para 3.
- A tentativa de excluir a compra com item foi bloqueada como esperado.
- O item 5 e a compra 4 foram removidos; as buscas retornaram None None.

Nao se trata de validacao exaustiva. O fluxo completo pelo menu ainda precisa
ser integrado e testado com a pessoa 5.

## Como repetir a validacao em um banco de teste

1. Configurar Oracle e as variaveis ORACLE_HOST, ORACLE_PORT, ORACLE_SERVICE,
   ORACLE_USER e ORACLE_PASSWORD conforme o ambiente do grupo.
2. Instalar requirements.txt em um ambiente Python adequado.
3. Usar um banco de teste com as tabelas e sequences do projeto. O script
   create_tables_and_records.py REMOVE e recria tabelas; nao executar sobre dados a preservar.
4. Testar insercao, busca, listagem, atualizacao e exclusao das duas entidades;
   conferir as datas, os IDs e a preservacao das FKs.
5. Integrar ao menu e mostrar confirmacoes, repeticoes e registro atualizado.

## Transparencia de IA

Apendice no PROMPTS.md registra os pedidos reais de desenvolvimento e o alcance
da validacao. O integrante deve revisar e entender o codigo antes de entregar.
