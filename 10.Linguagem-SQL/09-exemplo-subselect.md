# Exercício 5

## Análise de Desempenho de Produtos Usando Subselect

### Contexto de Negócio
**Desafio:** Identificar produtos que estão vendendo acima da média de preços dos produtos na mesma categoria. Isso ajuda a empresa a compreender quais produtos têm um desempenho excepcional de vendas, o que pode indicar uma alta percepção de valor por parte dos clientes ou popularidade elevada.

### Solução SQL: Uso de Subselect
Para enfrentar este desafio, usamos um subselect para calcular a média de preços dos produtos em cada categoria e, em seguida, selecionamos produtos que têm um preço acima desta média.

```sql
SELECT p.nome, p.preco, c.nome AS categoria_nome
FROM produto p
JOIN produto_categoria pc ON p.id = pc.produto_id
JOIN categoria c ON pc.categoria_id = c.id
WHERE p.preco > (
    SELECT AVG(p2.preco)
    FROM produto p2
    JOIN produto_categoria pc2 ON p2.id = pc2.produto_id
    WHERE pc2.categoria_id = pc.categoria_id
)
ORDER BY c.nome, p.preco DESC;
```

### Explicação da Query
1. **Junção das Tabelas:** O SQL junta as tabelas `Produto`, `produto_categoria`, e `Categoria` para associar cada produto à sua categoria.
2. **Subselect na Condição WHERE:** A condição `WHERE` utiliza um subselect para calcular a média dos preços dos produtos por categoria. O subselect correlaciona a categoria do produto principal com as categorias no subselect usando `pc.categoria_id = pc2.categoria_id`.
3. **Filtragem de Resultados:** A query principal filtra produtos cujo preço é maior que a média calculada, indicando que estão vendendo por um preço acima da média de sua categoria.
4. **Ordenação:** Os resultados são ordenados por nome da categoria e, dentro de cada categoria, por preço em ordem decrescente.

## Contexto de Negócio: Análise de Vendas de Produtos por Cliente

**Desafio:** Uma empresa deseja analisar o total de vendas por cliente comparando com o total geral de vendas, para entender a participação de cada cliente no faturamento total. Esse tipo de análise ajuda a identificar clientes-chave e também a avaliar a distribuição das vendas entre os clientes.

## Contexto de Negócio
### Solução SQL: Uso de Subselect no SELECT como Coluna
Para resolver este desafio, podemos utilizar um subselect dentro da cláusula SELECT para calcular o total geral de vendas enquanto listamos cada cliente com seu respectivo total de vendas. Isso permite comparar diretamente as vendas de cada cliente com o total geral de vendas na mesma consulta.
```sql
SELECT 
    c.nome AS ClienteNome,
    SUM(ic.preco_unitario * ic.quantidade) AS TotalVendasCliente,
    (SELECT SUM(preco_unitario * quantidade) FROM item_pedido) AS TotalVendasGeral
FROM 
    cliente c
JOIN 
    pedido p ON c.id = p.cliente_id
JOIN 
    item_pedido ic ON p.id = ic.pedido_id
GROUP BY 
    c.nome;
```

### Explicação da Query
1. **Junção das Tabelas:** A consulta junta as tabelas cliente, pedido, e item_pedido para acessar os dados de vendas.
2. **Subselect na Coluna:** No SELECT, há um subselect que calcula o total geral de vendas de todos os pedidos, fornecendo um ponto de comparação direto na mesma linha de cada resultado.
3. **Agregação de Vendas por Cliente:** A consulta usa SUM(ic.preco_unitario * ic.quantidade) para calcular o total de vendas por cliente.
3. **Agrupamento de Resultados:** Os resultados são agrupados por nome do cliente para garantir que o total de vendas seja calculado por cliente.


## Navegação
- [Anterior](08-exemplos-tipo-de-joins.md)
- [Próximo](10-funcoes-de-agrupamento.md)
