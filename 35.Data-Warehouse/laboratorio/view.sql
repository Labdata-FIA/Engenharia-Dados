USE DATABASE ecommerce_lab;

CREATE OR REPLACE VIEW vw_resumo_pedidos AS
SELECT 
    p.pedido_id,
    p.data_pedido,
    c.nome_empresa AS cliente,
    pr.nome_produto,
    dp.quantidade,
    dp.preco_unitario,
    dp.desconto,
    ROUND((dp.quantidade * dp.preco_unitario) * (1 - dp.desconto), 2) AS valor_item_liquido
FROM pedidos p
JOIN detalhes_pedido dp ON p.pedido_id = dp.pedido_id
JOIN produtos pr ON dp.produto_id = pr.produto_id
JOIN clientes c ON p.cliente_id = c.cliente_id;


CREATE OR REPLACE VIEW vw_catalogo_produtos AS
SELECT 
    p.produto_id,
    p.nome_produto,
    c.nome_categoria AS categoria,
    f.nome_empresa AS fornecedor,
    p.preco_unitario,
    p.unidades_em_estoque,
    CASE 
        WHEN p.unidades_em_estoque <= p.nivel_reordenacao THEN 'ESTOQUE BAIXO'
        ELSE 'OK'
    END AS status_estoque
FROM produtos p
JOIN categorias c ON p.categoria_id = c.categoria_id
JOIN fornecedores f ON p.fornecedor_id = f.fornecedor_id
WHERE p.descontinuado = FALSE;


CREATE OR REPLACE VIEW vw_vendas_por_categoria AS
SELECT 
    cat.nome_categoria,
    SUM(dp.quantidade) AS total_itens_vendidos,
    SUM(ROUND((dp.quantidade * dp.preco_unitario) * (1 - dp.desconto), 2)) AS receita_total
FROM detalhes_pedido dp
JOIN produtos pr ON dp.produto_id = pr.produto_id
JOIN categorias cat ON pr.categoria_id = cat.categoria_id
GROUP BY cat.nome_categoria;


SELECT * FROM vw_catalogo_produtos;

select  * from  vw_vendas_por_categoria;


SELECT * FROM vw_resumo_pedidos WHERE cliente = 'Mercado Central Ltda';