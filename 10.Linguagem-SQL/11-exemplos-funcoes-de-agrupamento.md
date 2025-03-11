
# Utilização das Funções de Agrupamento em SQL com Contexto de Negócios

## 1. COUNT()
**Contexto de Negócio:** Determinar quantos pedidos foram feitos por cada cliente para identificar os mais ativos.
```sql
SELECT Cliente.nome, COUNT(Pedido.id) AS NumeroDePedidos
FROM Cliente
JOIN Pedido ON Cliente.id = Pedido.cliente_id
GROUP BY Cliente.nome;
```

## 2. SUM()
**Contexto de Negócio:** Calcular o total de vendas geradas por cada produto.
```sql
SELECT Produto.nome, SUM(item_pedido.quantidade * item_pedido.preco_unitario) AS TotalVendas
FROM Produto
JOIN item_pedido ON Produto.id = item_pedido.produto_id
GROUP BY Produto.nome;
```

## 3. AVG()
**Contexto de Negócio:** Calcular o preço médio dos produtos vendidos para auxiliar na definição de preços e promoções.
```sql
SELECT Categoria.nome, AVG(Produto.preco) AS PrecoMedio
FROM Produto
JOIN produto_categoria ON Produto.id = produto_categoria.produto_id
JOIN Categoria ON produto_categoria.categoria_id = Categoria.id
GROUP BY Categoria.nome;
```

## 4. MAX()
**Contexto de Negócio:** Identificar o produto mais caro em cada categoria para campanhas de marketing de produtos premium.
```sql
SELECT Categoria.nome AS Categoria, MAX(Produto.preco) AS PrecoMaximo
FROM Produto
JOIN produto_categoria ON Produto.id = produto_categoria.produto_id
JOIN Categoria ON produto_categoria.categoria_id = Categoria.id
GROUP BY Categoria.nome;
```

## 5. MIN()
**Contexto de Negócio:** Determinar o produto mais barato em cada categoria para promoções especiais.
```sql
SELECT Categoria.nome AS Categoria, MIN(Produto.preco) AS PrecoMinimo
FROM Produto
JOIN produto_categoria ON Produto.id = produto_categoria.produto_id
JOIN Categoria ON produto_categoria.categoria_id = Categoria.id
GROUP BY Categoria.nome;
```

## 6. STDDEV()
**Contexto de Negócio:** Analisar a variação nos preços dos produtos dentro de cada categoria para entender a diversidade da oferta.
```sql
SELECT Categoria.nome, STDDEV(Produto.preco) AS DesvioPadraoPreco
FROM Produto
JOIN produto_categoria ON Produto.id = produto_categoria.produto_id
JOIN Categoria ON produto_categoria.categoria_id = Categoria.id
GROUP BY Categoria.nome;
```

## 7. VAR() ou VARIANCE()
**Contexto de Negócio:** Calcular a variância nos preços dos produtos para identificar categorias com grande dispersão de preços.
```sql
SELECT Categoria.nome, VARIANCE(Produto.preco) AS VariacaoPreco
FROM Produto
JOIN produto_categoria ON Produto.id = produto_categoria.produto_id
JOIN Categoria ON produto_categoria.categoria_id = Categoria.id
GROUP BY Categoria.nome;
```

## Navegação
- [Anterior](10-funcoes-de-agrupamento.md)
- [Próximo](12-exemplo-having.md)

