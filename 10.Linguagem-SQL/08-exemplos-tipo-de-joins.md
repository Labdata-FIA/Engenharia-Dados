# Exemplos de tipos de Join

## Rodar os scripts de carga
- [02_cliente.sql](setup-scripts%2F02_cliente.sql)
- [03_produto.sql](setup-scripts%2F03_produto.sql)
- [04_categoria.sql](setup-scripts%2F04_categoria.sql)
- [05_pedido.sql](setup-scripts%2F05_pedido.sql)

## 1. INNER JOIN
**Contexto de Negócio:** Listar todos os produtos que foram pedidos, com detalhes dos produtos e dos pedidos correspondentes.

```sql
SELECT p.id AS PedidoID, prd.nome AS ProdutoNome, prd.preco AS Preco, ic.quantidade AS Quantidade
FROM pedido p
INNER JOIN item_pedido ic ON p.id = ic.pedido_id
INNER JOIN produto prd ON ic.produto_id = prd.id
ORDER BY p.id;
```

## 2. LEFT JOIN (LEFT OUTER JOIN)
**Contexto de Negócio:** Identificar clientes que ainda não fizeram nenhum pedido para direcionar campanhas de marketing.

```sql
SELECT c.nome AS ClienteNome, p.id AS PedidoID
FROM cliente c
LEFT JOIN pedido p ON c.id = p.cliente_id
WHERE p.id IS NULL;
```

## 3. RIGHT JOIN (RIGHT OUTER JOIN)
**Contexto de Negócio:** Listar todos os pedidos, incluindo aqueles que não têm produtos associados.

```sql
SELECT p.id AS PedidoID, prd.nome AS ProdutoNome
FROM produto prd
RIGHT JOIN item_pedido ic ON prd.id = ic.produto_id
RIGHT JOIN pedido p ON ic.pedido_id = p.id
WHERE prd.id IS NULL;
```

## 4. FULL OUTER JOIN
**Contexto de Negócio:** Obter uma lista completa de todos os clientes e todos os pedidos, para uma visão completa do engajamento do cliente.

**O FULL OUTER JOIN NÃO É SUPORTADO NO MYSQL**
```sql
SELECT c.nome AS ClienteNome, p.id AS PedidoID
FROM cliente c
FULL OUTER JOIN pedido p ON c.id = p.cliente_id;
```

## 5. CROSS JOIN
**Contexto de Negócio:** Precisamos de um relatório que mostre todas as possíveis combinações de produtos e categorias para análise de potenciais novas linhas de produtos.

```sql
SELECT prd.nome AS ProdutoNome, cat.nome AS CategoriaNome
FROM produto prd
CROSS JOIN categoria cat;
```

## 6. SELF JOIN
**Contexto de Negócio:** Identificar produtos dentro da mesma categoria que poderiam ser promovidos juntos em pacotes ou ofertas especiais.

```sql
SELECT prd1.nome AS Produto1, prd2.nome AS Produto2, cat.nome AS CategoriaNome
FROM produto_categoria pc1
JOIN produto_categoria pc2 ON pc1.categoria_id = pc2.categoria_id AND pc1.produto_id != pc2.produto_id
JOIN produto prd1 ON pc1.produto_id = prd1.id
JOIN produto prd2 ON pc2.produto_id = prd2.id
JOIN categoria cat ON pc1.categoria_id = cat.id;
```


## Navegação
- [Anterior](07-select-tipos-de-joins.md)
- [Próximo](09-exemplo-subselect.md)
