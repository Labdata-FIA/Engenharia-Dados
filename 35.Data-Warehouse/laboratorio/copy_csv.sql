USE DATABASE ecommerce_lab;

-- Criar um estágio para armazenar o arquivo CSV
CREATE OR REPLACE STAGE meu_estagio_csv;

CREATE OR REPLACE FILE FORMAT formato_csv_simples
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 0
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';



list @MEU_ESTAGIO_CSV

//Subir o arquivo csv

SHOW STAGES;


CREATE TABLE produtos_csv (
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

COPY INTO produtos_csv (
    produto_id, 
    nome_produto, 
    fornecedor_id, 
    categoria_id, 
    quantidade_por_unidade, 
    preco_unitario,
    unidades_em_estoque, 
    unidades_encomendadas, 
    nivel_reordenacao, 
    descontinuado
)
FROM (
  SELECT 
    t.$1,
    t.$2,
    t.$3,
    t.$4,
    t.$5,
    t.$6 AS FLOAT, -- CORREÇÃO: Cast explícito antes da operação
    t.$7,
    t.$8,
    t.$9,
    t.$10
  FROM @meu_estagio_csv/produto.csv t
)
FILE_FORMAT = (FORMAT_NAME = formato_csv_simples);

select * from produtos_csv

delete from produtos_csv



SELECT 
    t.$1,  -- produto_id
    t.$2,  -- nome_produto
    t.$3,  -- fornecedor_id
    t.$4,  -- categoria_id
    t.$5,  -- quantidade_por_unidade
    t.$6 * 1.1, -- TRANSFORMAÇÃO: Preço + 10% de acréscimo,
    t.$6,
    t.$7,  -- unidades_em_estoque
    t.$8,  -- unidades_encomendadas
    t.$9,  -- nivel_reordenacao
    t.$10  -- descontinuado
  FROM @meu_estagio_csv/produto.csv t
  