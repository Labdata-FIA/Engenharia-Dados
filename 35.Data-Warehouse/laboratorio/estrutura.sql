CREATE DATABASE ecommerce_lab;

USE DATABASE ecommerce_lab;

CREATE TABLE categorias (
    categoria_id SMALLINT NOT NULL,
    nome_categoria STRING NOT NULL,
    descricao STRING
);

CREATE TABLE clientes (
    cliente_id STRING NOT NULL,
    nome_empresa STRING NOT NULL,
    nome_contato STRING,
    titulo_contato STRING,
    endereco STRING,
    cidade STRING,
    regiao STRING,
    codigo_postal STRING,
    pais STRING,
    telefone STRING
);

CREATE TABLE funcionarios (
    funcionario_id SMALLINT NOT NULL,
    sobrenome STRING NOT NULL,
    nome STRING NOT NULL,
    titulo STRING,
    titulo_cortesia STRING,
    data_nascimento DATE,
    data_contratacao DATE,
    endereco STRING,
    cidade STRING,
    regiao STRING,
    codigo_postal STRING,
    pais STRING,
    telefone_residencial STRING,
    extensao STRING,
    notas STRING,
    reporta_a SMALLINT,
    caminho_foto STRING,
    salario FLOAT
);

CREATE TABLE detalhes_pedido (
    pedido_id SMALLINT NOT NULL,
    produto_id SMALLINT NOT NULL,
    preco_unitario FLOAT NOT NULL,
    quantidade SMALLINT NOT NULL,
    desconto FLOAT NOT NULL
);

CREATE TABLE pedidos (
    pedido_id SMALLINT NOT NULL,
    cliente_id STRING,
    funcionario_id SMALLINT,
    data_pedido DATE,
    data_requerida DATE,
    data_envio DATE,
    enviar_via SMALLINT,
    frete FLOAT,
    nome_envio STRING,
    endereco_envio STRING,
    cidade_envio STRING,
    regiao_envio STRING,
    codigo_postal_envio STRING,
    pais_envio STRING
)
CLUSTER BY (data_pedido);

CREATE TABLE produtos (
    produto_id SMALLINT NOT NULL,
    nome_produto STRING NOT NULL,
    fornecedor_id SMALLINT,
    categoria_id SMALLINT,
    quantidade_por_unidade STRING,
    preco_unitario FLOAT,
    unidades_em_estoque SMALLINT,
    unidades_encomendadas SMALLINT,
    nivel_reordenacao SMALLINT,
    descontinuado BOOLEAN NOT NULL
);

CREATE TABLE transportadoras (
    transportadora_id SMALLINT NOT NULL,
    nome_empresa STRING NOT NULL,
    telefone STRING
);

CREATE TABLE fornecedores (
    fornecedor_id SMALLINT NOT NULL,
    nome_empresa STRING NOT NULL,
    nome_contato STRING,
    titulo_contato STRING,
    endereco STRING,
    cidade STRING,
    regiao STRING,
    codigo_postal STRING,
    pais STRING,
    telefone STRING,
    fax STRING,
    pagina_inicial STRING
);


