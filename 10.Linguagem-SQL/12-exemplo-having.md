# Exemplo usando HAVING

## Identificar Produtos de Alto Desempenho Usando HAVING

### Contexto de Negócio
Uma empresa deseja identificar produtos que consistentemente geram altos volumes de vendas. O objetivo é focar em produtos que ultrapassaram um determinado limiar de unidades vendidas em múltiplos pedidos, para que possam ser destacados em promoções futuras ou considerados para expansão de linha.

### Estrutura de Tabelas Envolvidas
- **Produtos** (tabela `Produto`) com colunas como `id`, `nome`, `preco`, etc.
- **Itens de Pedido** (tabela `item_pedido`) com colunas como `pedido_id`, `produto_id`, `quantidade`, `preco_unitario`, etc.

### SQL Query com HAVING
Objetivo: Encontrar produtos cujas vendas totais ultrapassaram 100 unidades em todos os pedidos.

```sql
SELECT p.id AS ProdutoID, p.nome AS ProdutoNome, SUM(ip.quantidade) AS UnidadesVendidas
FROM Produto p
JOIN item_pedido ip ON p.id = ip.produto_id
GROUP BY p.id, p.nome
HAVING SUM(ip.quantidade) > 100;
```

#### Explicação da Query
- **Junção de Tabelas:** A consulta junta a tabela `Produto` com a tabela `item_pedido` usando o `produto_id` para acessar a quantidade de cada item pedido.
- **Agregação:** Utiliza a função `SUM()` para calcular o total de unidades vendidas de cada produto.
- **Filtragem com HAVING:** Após o agrupamento dos produtos, a cláusula `HAVING` é usada para filtrar e listar apenas aqueles produtos cujas unidades vendidas totalizam mais de 100. Diferentemente da cláusula `WHERE`, que filtra linhas antes da agregação, o `HAVING` filtra os resultados após a agregação.


## Navegação
- [Anterior](11-exemplos-funcoes-de-agrupamento.md)
- [Próximo](13-tipos-de-union.md)
