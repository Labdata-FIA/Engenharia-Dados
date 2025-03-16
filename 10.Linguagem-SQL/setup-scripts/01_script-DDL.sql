use `database-dev-mysql`;

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

CREATE TABLE produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL CHECK (preco >= 0)
);

CREATE TABLE categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

CREATE TABLE produto_categoria (
    produto_id INT NOT NULL,
    categoria_id INT NOT NULL,
    PRIMARY KEY (produto_id, categoria_id),
    FOREIGN KEY (produto_id) REFERENCES produto(id),
    FOREIGN KEY (categoria_id) REFERENCES categoria(id)
);

CREATE TABLE pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    data_pedido DATE NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

CREATE TABLE item_pedido (
    pedido_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (pedido_id, produto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (produto_id) REFERENCES produto(id)
);

CREATE INDEX idx_email ON cliente(email);

CREATE INDEX idx_nome_produto ON produto(nome);

ALTER TABLE pedido ADD COLUMN status VARCHAR(10) NOT NULL DEFAULT 'ativo';

ALTER TABLE item_pedido ADD COLUMN desconto DECIMAL(10, 2) DEFAULT 0;

DROP VIEW IF EXISTS v_detalhe_pedido_cliente;

CREATE VIEW v_detalhe_pedido_cliente AS
SELECT
    c.id AS cliente_id,
    c.nome AS cliente_nome,
    c.email AS cliente_email,
    prd.id AS produto_id,
    prd.nome AS produto_nome,
    prd.preco AS produto_preco,
    p.id AS pedido_id,
    p.data_pedido AS data_pedido,
    ic.quantidade AS quantidade,
    ic.preco_unitario AS preco_unitario,
    (ic.quantidade * ic.preco_unitario) AS total_item
FROM
    pedido p
        INNER JOIN cliente c ON p.cliente_id = c.id
        INNER JOIN item_pedido ic ON p.id = ic.pedido_id
        INNER JOIN produto prd ON ic.produto_id = prd.id;
