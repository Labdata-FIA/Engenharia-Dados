
# Utilização das Funções de Agrupamento em SQL com Contexto de Negócios

## 1. COUNT()
**Contexto de Negócio:** Determinar quantos pedidos foram feitos por cada cliente para identificar os mais ativos.
```sql
SELECT cliente.nome, COUNT(pedido.id) AS NumeroDepedidos
FROM cliente
JOIN pedido ON cliente.id = pedido.cliente_id
GROUP BY cliente.nome;
```

## 2. SUM()
**Contexto de Negócio:** Calcular o total de vendas geradas por cada produto.
```sql
SELECT produto.nome, SUM(item_pedido.quantidade * item_pedido.preco_unitario) AS TotalVendas
FROM produto
JOIN item_pedido ON produto.id = item_pedido.produto_id
GROUP BY produto.nome;
```

## 3. AVG()
**Contexto de Negócio:** Calcular o preço médio dos produtos vendidos para auxiliar na definição de preços e promoções.
```sql
SELECT categoria.nome, AVG(produto.preco) AS PrecoMedio
FROM produto
JOIN produto_categoria ON produto.id = produto_categoria.produto_id
JOIN categoria ON produto_categoria.categoria_id = categoria.id
GROUP BY categoria.nome;
```

## 4. MAX()
**Contexto de Negócio:** Identificar o produto mais caro em cada categoria para campanhas de marketing de produtos premium.
```sql
SELECT categoria.nome AS categoria, MAX(produto.preco) AS PrecoMaximo
FROM produto
JOIN produto_categoria ON produto.id = produto_categoria.produto_id
JOIN categoria ON produto_categoria.categoria_id = categoria.id
GROUP BY categoria.nome;
```

## 5. MIN()
**Contexto de Negócio:** Determinar o produto mais barato em cada categoria para promoções especiais.
```sql
SELECT categoria.nome AS categoria, MIN(produto.preco) AS PrecoMinimo
FROM produto
JOIN produto_categoria ON produto.id = produto_categoria.produto_id
JOIN categoria ON produto_categoria.categoria_id = categoria.id
GROUP BY categoria.nome;
```

## 6. STDDEV()
**Contexto de Negócio:** Analisar a variação nos preços dos produtos dentro de cada categoria para entender a diversidade da oferta.
```sql
SELECT categoria.nome, STDDEV(produto.preco) AS DesvioPadraoPreco
FROM produto
JOIN produto_categoria ON produto.id = produto_categoria.produto_id
JOIN categoria ON produto_categoria.categoria_id = categoria.id
GROUP BY categoria.nome;
```

## 7. VAR() ou VARIANCE()
**Contexto de Negócio:** Calcular a variância nos preços dos produtos para identificar categorias com grande dispersão de preços.
```sql
SELECT categoria.nome, VARIANCE(produto.preco) AS VariacaoPreco
FROM produto
JOIN produto_categoria ON produto.id = produto_categoria.produto_id
JOIN categoria ON produto_categoria.categoria_id = categoria.id
GROUP BY categoria.nome;
```

## Navegação
- [Anterior](10-funcoes-de-agrupamento.md)
- [Próximo](12-exemplo-having.md)

