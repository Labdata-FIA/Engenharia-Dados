USE DATABASE ecommerce_lab;

CREATE TABLE produtos_log (
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


CREATE OR REPLACE STREAM stream_produtos
ON TABLE produtos;

select * from stream_produtos;


INSERT INTO produtos (produto_id, nome_produto, fornecedor_id, categoria_id, quantidade_por_unidade, preco_unitario, unidades_em_estoque, unidades_encomendadas, nivel_reordenacao, descontinuado) VALUES 
(101, 'Suco de Cupuaçu 500ml', 1, 1, '12 garrafas', 15.50, 40, 0, 10, FALSE);


select * from produtos where produto_id = 100;

select * from stream_produtos;

insert into produtos_log
select produto_id, nome_produto ,fornecedor_id,categoria_id ,quantidade_por_unidade , preco_unitario,unidades_em_estoque , unidades_encomendadas , nivel_reordenacao,
    descontinuado from stream_produtos
where metadata$action = 'INSERT' and metadata$isupdate = false;

select * from produtos_log;

delete from produtos_log;
