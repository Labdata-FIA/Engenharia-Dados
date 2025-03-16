# Exemplo do uso de UNION ALL

## Contexto de Negócio
Uma empresa deseja analisar o impacto de promoções e feriados específicos nas vendas para planejar melhor as campanhas futuras e ajustar a gestão de estoque. Os períodos de interesse incluem a Black Friday e o Ano Novo, ambos de alta atividade comercial.

## Cenários e SQL Queries

### Cenário 1: Pedidos Durante a Black Friday
**Objetivo:** Determinar o volume de pedidos durante a Black Friday para avaliar a eficácia de estratégias de desconto e promoção.

```sql
SELECT Pedido.id AS PedidoID, Pedido.data_pedido AS DataPedido, Cliente.nome AS ClienteNome
FROM Pedido
JOIN Cliente ON Pedido.cliente_id = Cliente.id
WHERE Pedido.data_pedido BETWEEN '2022-11-24' AND '2022-11-25';
```

### Cenário 2: Pedidos Durante o Ano Novo
**Objetivo:** Analisar os pedidos feitos durante o Ano Novo para entender a demanda de produtos e a eficiência das promoções de fim de ano.

```sql
SELECT Pedido.id AS PedidoID, Pedido.data_pedido AS DataPedido, Cliente.nome AS ClienteNome
FROM Pedido
JOIN Cliente ON Pedido.cliente_id = Cliente.id
WHERE Pedido.data_pedido BETWEEN '2022-12-26' AND '2023-01-01';
```

### Combinação dos Cenários com UNION ALL
**Objetivo:** Produzir um relatório detalhado que mostra a atividade total de pedidos para ambos os eventos sem eliminar duplicatas, permitindo uma análise detalhada da atividade em cada evento.

```sql
-- Pedidos durante a Black Friday
SELECT 'Black Friday' AS Evento, Pedido.id AS PedidoID, Pedido.data_pedido AS DataPedido, Cliente.nome AS ClienteNome
FROM Pedido
JOIN Cliente ON Pedido.cliente_id = Cliente.id
WHERE Pedido.data_pedido BETWEEN '2022-11-24' AND '2022-11-25'
UNION ALL
-- Pedidos durante o Ano Novo
SELECT 'Ano Novo' AS Evento, Pedido.id AS PedidoID, Pedido.data_pedido AS DataPedido, Cliente.nome AS ClienteNome
FROM Pedido
JOIN Cliente ON Pedido.cliente_id = Cliente.id
WHERE Pedido.data_pedido BETWEEN '2022-12-26' AND '2023-01-01';
```

Este relatório combinado proporciona uma visão completa do impacto de cada evento nas vendas, crucial para planejamento estratégico, marketing e operações.



## Navegação
- [Anterior](14-exemplo-union.md)
- [Próximo](16-fase2-o-escopo-aumentou.md)
