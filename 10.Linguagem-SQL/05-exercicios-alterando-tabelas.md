# Exercício 3: Alterando Tabelas

## Adicionar uma coluna status à tabela pedido
```sql
ALTER TABLE pedido ADD COLUMN status VARCHAR(10) NOT NULL DEFAULT 'ativo';
```

## Modificar a tabela item_pedido para incluir desconto
```sql
ALTER TABLE item_pedido ADD COLUMN desconto DECIMAL(10, 2) DEFAULT 0;
```

## Navegação
- [Anterior](04-exercicios-criar-indices.md)
- [Próximo](06-exercicios-criar-view.md)
