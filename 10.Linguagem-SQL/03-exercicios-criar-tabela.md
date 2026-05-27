# Exercício 1: Criação de Tabelas

## Modelo de entidade de relacionamento - MER
![mer-v1.0.0.png](imagens%2Fmer-v1.0.0.png)

### Selecionar o banco de dados
```sql
use `database-dev-mysql`;
```

### Removendo as tabelas
```sql
DROP VIEW IF EXISTS v_detalhe_pedido_cliente;
DROP TABLE IF EXISTS item_pedido;
DROP TABLE IF EXISTS entrega;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS produto_categoria;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS forma_pagamento;
DROP TABLE IF EXISTS transportadora;
```

### Criar a tabela cliente
```sql
CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    telefone VARCHAR(15),
    email VARCHAR(100),
    logradouro VARCHAR(100),
    numero VARCHAR(10),
    complemento VARCHAR(50),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    estado VARCHAR(2),
    cep VARCHAR(8)
);
```

> https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Data-Types.html
> https://dev.mysql.com/doc/refman/9.7/en/data-types.html
> https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17

### Inserindo clientes

O comando `INSERT` é usado para cadastrar novos registros na tabela.

#### Inserir um cliente

```sql
INSERT INTO cliente (
    nome, cpf, telefone, email, logradouro, numero, complemento,
    bairro, cidade, estado, cep
)
VALUES (
    'João Silva', '12345678901', '11999990000', 'joao@email.com',
    'Rua das Flores', '100', 'Apto 12', 'Centro', 'São Paulo', 'SP', '01001000'
);
```

### Inserir mais de um cliente

```sql
INSERT INTO cliente (
    nome, cpf, telefone, email, logradouro, numero, complemento,
    bairro, cidade, estado, cep
)
VALUES
(
    'Maria Oliveira', '98765432100', '21988887777', 'maria@email.com',
    'Avenida Brasil', '200', NULL, 'Copacabana', 'Rio de Janeiro', 'RJ', '22040002'
),
(
    'Carlos Souza', '45678912300', '13977776666', 'carlos@email.com',
    'Rua do Porto', '50', 'Casa', 'Boqueirão', 'Praia Grande', 'SP', '11700000'
),
(
    'Ana Pereira', '32165498700', '31966665555', 'ana@email.com',
    'Rua Minas Gerais', '300', NULL, 'Funcionários', 'Belo Horizonte', 'MG', '30140000'
);
```

#### Consultar os dados inseridos

```sql
SELECT * FROM cliente;
```

### Atualizando clientes

O comando `UPDATE` é usado para alterar dados existentes.

> Atenção: sempre use `WHERE` no `UPDATE` para evitar alterar todos os registros da tabela.

#### Atualizar telefone de um cliente

```sql
UPDATE cliente
SET telefone = '11911112222'
WHERE cpf = '12345678901';
```

#### Atualizar e-mail e endereço

```sql
UPDATE cliente
SET 
    email = 'joao.silva@novoemail.com',
    logradouro = 'Rua Nova Esperança',
    numero = '150',
    bairro = 'Vila Mariana',
    cidade = 'São Paulo',
    estado = 'SP',
    cep = '04101000'
WHERE cpf = '12345678901';
```

#### Atualizar cidade de clientes de um estado

```sql
UPDATE cliente
SET cidade = 'Santos'
WHERE estado = 'SP' AND cidade = 'Praia Grande';
```

#### Conferir atualização

```sql
SELECT id, nome, cpf, telefone, email, cidade, estado
FROM cliente;
```

### Excluindo clientes

O comando `DELETE` é usado para remover registros da tabela.

> Atenção: sempre use `WHERE` no `DELETE` para evitar excluir todos os registros.

### Excluir um cliente pelo CPF

```sql
DELETE FROM cliente
WHERE cpf = '32165498700';
```

#### Excluir clientes de uma cidade específica

```sql
DELETE FROM cliente
WHERE cidade = 'Santos';
```

#### Conferir exclusão

```sql
SELECT * FROM cliente;
```



### Criar a tabela produto

```sql
CREATE TABLE produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL CHECK (preco >= 0)
);
```

> [!IMPORTANT]
>Constraint é uma regra aplicada em uma tabela ou coluna para garantir que os dados gravados estejam corretos.

### Criar a tabela categoria

```sql
CREATE TABLE categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);
```

### Criar a tabela de associaçao produto categoria

```sql
CREATE TABLE produto_categoria (
    produto_id INT NOT NULL,
    categoria_id INT NOT NULL,
    PRIMARY KEY (produto_id, categoria_id),
    FOREIGN KEY (produto_id) REFERENCES produto(id),
    FOREIGN KEY (categoria_id) REFERENCES categoria(id)
);
```

### Criar a tabela Pedido

```sql
CREATE TABLE tbpedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    data_pedido DATE NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);
```

### Fiz errado

```sql
drop TABLE tbpedido;
```

### Criado novamente a tabela Pedido correta

```sql
CREATE TABLE tbpedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    data_pedido DATE NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);
```

### Criar a tabela item_pedido (associação entre Pedido e Produto)


```sql
CREATE TABLE item_pedido (
    pedido_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (pedido_id, produto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (produto_id) REFERENCES produto(id)
);
```

## Navegação
- [Anterior](02-introducao-sql.md)
- [Próximo](04-exercicios-criar-indices.md)

