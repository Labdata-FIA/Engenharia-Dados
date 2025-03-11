# Introdução a linguagem SQL

## Categorias de Linguagem SQL: DDL, DML, DQL, DTL e DCL

Nos sistemas de gerenciamento de banco de dados (SGBDs), diferentes categorias de linguagem SQL permitem interações específicas com o banco de dados. Essas categorias incluem DDL (Linguagem de Definição de Dados), DML (Linguagem de Manipulação de Dados), DQL (Linguagem de Consulta de Dados), DCL (Linguagem de Controle de Dados) e DTL (Linguagem de Transação de Dados). Aqui está uma explicação de cada uma:

### 1. DDL (Data Definition Language - Linguagem de Definição de Dados)
A DDL envolve comandos que definem a estrutura do banco de dados. Esses comandos permitem ao usuário criar, alterar e deletar bancos de dados, tabelas, índices e outros objetos dentro do banco de dados. Os comandos mais comuns incluem:
- **CREATE**: Usado para criar novos objetos, como tabelas, índices, funções e bancos de dados.
- **ALTER**: Usado para modificar a estrutura de um objeto existente, como adicionar uma nova coluna a uma tabela.
- **DROP**: Usado para deletar objetos existentes, como uma tabela ou índice.
- **TRUNCATE**: Remove todos os registros de uma tabela, sem deletar a tabela em si.

### 2. DML (Data Manipulation Language - Linguagem de Manipulação de Dados)
A DML é utilizada para manipular os dados dentro das tabelas. Esta categoria de comandos permite inserir, modificar ou remover dados de um banco de dados já existente. Os comandos mais comuns incluem:
- **INSERT**: Insere novos dados em uma tabela.
- **UPDATE**: Modifica dados existentes em uma tabela.
- **DELETE**: Remove dados de uma tabela.

### 3. DQL (Data Query Language - Linguagem de Consulta de Dados)
A DQL é usada principalmente para consultar dados de um banco de dados. É fundamentalmente composta pelo comando:
- **SELECT**: Usado para buscar dados de uma ou mais tabelas. Geralmente é o comando mais usado em SQL e pode ser altamente complexo e poderoso, com cláusulas para filtragem, ordenação e agregação de dados.

### 4. DTL (Data Transaction Language - Linguagem de Transação de Dados)
Embora menos comumente referenciada como uma categoria separada (geralmente considerada parte do DML), a DTL lida com transações dentro de um banco de dados. As transações são importantes para manter a integridade dos dados e garantir que operações múltiplas sejam tratadas de forma atômica. Comandos incluem:
- **BEGIN TRANSACTION** (ou **START TRANSACTION**): Inicia uma transação.
- **COMMIT**: Salva todas as mudanças feitas na transação atual.
- **ROLLBACK**: Reverte todas as mudanças feitas na transação atual.

### 5. DCL (Data Control Language - Linguagem de Controle de Dados)
A DCL inclui comandos que lidam com direitos, permissões e outros controles de acesso ao banco de dados. Estes comandos ajudam a administrar quem tem que tipo de acesso aos dados dentro do banco de dados. Comandos comuns são:
- **GRANT**: Concede acesso ou privilégios a um usuário.
- **REVOKE**: Remove acessos ou privilégios existentes de um usuário.

Essas categorias cobrem a vasta gama de operações que podem ser realizadas em bancos de dados SQL e são essenciais para o gerenciamento e manipulação eficazes de dados.

## Navegação
- [Anterior](01-intruducao.md)
- [Próximo](03-exercicios-criar-tabela.md)

