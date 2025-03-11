# Exemplo do uso de UNION

## Contexto de Negócio
Uma empresa deseja analisar a atividade de pedidos em duas condições diferentes para planejar estratégias de marketing e operações logísticas mais eficazes. Os focos são pedidos durante o Natal para entender a demanda sazonal e pedidos em uma região específica para avaliar a penetração de mercado.

## Cenários e SQL Queries

### Cenário 1: Pedidos Durante o Natal
**Objetivo:** Analisar os pedidos feitos durante o período do Natal para identificar tendências de consumo e planejar estoque para o próximo ano.

```sql
SELECT Pedido.id AS PedidoID, Pedido.data_pedido AS DataPedido, Cliente.nome AS ClienteNome
FROM Pedido
JOIN Cliente ON Pedido.cliente_id = Cliente.id
WHERE Pedido.data_pedido BETWEEN '2022-12-24' AND '2022-12-26';
```

### Cenário 2: Pedidos na Região Sul
**Objetivo:** Avaliar a quantidade de pedidos na região Sul para ajustar estratégias de marketing e distribuição.

```sql
SELECT Pedido.id AS PedidoID, Pedido.data_pedido AS DataPedido, Cliente.nome AS ClienteNome
FROM Pedido
JOIN Cliente ON Pedido.cliente_id = Cliente.id
WHERE Cliente.estado IN ('PR', 'SC', 'RS');
```

### Combinação dos Cenários com UNION
**Objetivo:** Obter um relatório consolidado que apresente uma visão abrangente das atividades de pedidos em condições especiais, permitindo à empresa preparar melhor suas operações e estratégias de marketing.

```sql
-- Pedidos durante o Natal
SELECT 'Natal' AS Evento, Pedido.id AS PedidoID, Pedido.data_pedido AS DataPedido, Cliente.nome AS ClienteNome
FROM Pedido
JOIN Cliente ON Pedido.cliente_id = Cliente.id
WHERE Pedido.data_pedido BETWEEN '2022-12-24' AND '2022-12-26'
UNION
-- Pedidos na região Sul
SELECT 'Região Sul' AS Evento, Pedido.id AS PedidoID, Pedido.data_pedido AS DataPedido, Cliente.nome AS ClienteNome
FROM Pedido
JOIN Cliente ON Pedido.cliente_id = Cliente.id
WHERE Cliente.estado IN ('PR', 'SC', 'RS');
```

Este relatório combinado oferece uma análise diversificada que ajuda a empresa a entender melhor as demandas específicas em diferentes tempos e locais.

## Navegação
- [Anterior](13-tipos-de-union.md)
- [Próximo](15-exemplo-union-all.md)
