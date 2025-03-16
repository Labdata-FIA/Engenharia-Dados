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

### Criar a tabela produto

```sql
CREATE TABLE produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL CHECK (preco >= 0)
);
```

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
CREATE TABLE pedido (
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

