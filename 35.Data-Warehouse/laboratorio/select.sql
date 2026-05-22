USE DATABASE ecommerce_lab;

SELECT nome_empresa, nome_contato, cidade
FROM fornecedores
WHERE pais = 'Brasil';

SELECT nome_categoria, descricao  FROM categorias;

//2. Consultas com Filtros e Ordenação


SELECT * 
FROM transportadoras 
ORDER BY nome_empresa ASC;



SELECT nome_empresa, pagina_inicial 
FROM fornecedores 
WHERE pagina_inicial != '';




// 3. Consultas Relacionais (Joins)


SELECT p.nome_produto, c.nome_categoria
FROM produtos p
JOIN categorias c ON p.categoria_id = c.categoria_id;


SELECT pe.pedido_id, pe.data_pedido, tr.nome_empresa AS transportadora
FROM pedidos pe
JOIN transportadoras tr ON pe.enviar_via = tr.transportadora_id;




SELECT pais, COUNT(*) AS total_fornecedores
FROM fornecedores
GROUP BY pais
ORDER BY total_fornecedores DESC;



