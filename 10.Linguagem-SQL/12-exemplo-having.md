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
FROM produto p
JOIN item_pedido ip ON p.id = ip.produto_id
GROUP BY p.id, p.nome
HAVING SUM(ip.quantidade) > 100;
```

#### Explicação da Query
- **Junção de Tabelas:** A consulta junta a tabela `Produto` com a tabela `item_pedido` usando o `produto_id` para acessar a quantidade de cada item pedido.
- **Agregação:** Utiliza a função `SUM()` para calcular o total de unidades vendidas de cada produto.
- **Filtragem com HAVING:** Após o agrupamento dos produtos, a cláusula `HAVING` é usada para filtrar e listar apenas aqueles produtos cujas unidades vendidas totalizam mais de 100. Diferentemente da cláusula `WHERE`, que filtra linhas antes da agregação, o `HAVING` filtra os resultados após a agregação.


# CTE

## O que é CTE?

CTE significa **Common Table Expression**.

É uma consulta temporária nomeada criada com `WITH`.

Ela existe apenas durante a execução da consulta.

## Para que serve?

Serve para:

- organizar consultas grandes;
- dividir uma análise em etapas;
- evitar repetição de subqueries;
- melhorar a legibilidade;
- preparar dados para ranking, acumulado e comparações.

```sql
WITH total_por_cliente AS (
    SELECT
        p.cliente_id,
        SUM(ip.quantidade * ip.preco_unitario) AS total_gasto
    FROM pedido p
    JOIN item_pedido ip
        ON ip.pedido_id = p.id
    GROUP BY
        p.cliente_id
)
SELECT *
FROM total_por_cliente t;
```



##  CTE com múltiplas etapas

## Caso de uso

Listar clientes que gastaram acima da média.

```sql
WITH clientes_sp AS (
    SELECT
        id,
        nome,
        estado
    FROM cliente
    WHERE estado = 'SP'
),
total_por_cliente AS (
    SELECT
        c.id AS cliente_id,
        c.nome,
        SUM(ip.quantidade * ip.preco_unitario) AS total_gasto
    FROM clientes_sp c
    INNER JOIN pedido p
        ON p.cliente_id = c.id
    INNER JOIN item_pedido ip
        ON ip.pedido_id = p.id
    GROUP BY
        c.id,
        c.nome
),

clientes_acima_100 AS (
    SELECT
        cliente_id,
        nome,
        total_gasto
    FROM total_por_cliente
    WHERE total_gasto > 100
)

SELECT
    cliente_id,
    nome,
    ROUND(total_gasto, 2) AS total_gasto
FROM clientes_acima_100
ORDER BY
    total_gasto DESC;
```


---

# Window Functions


Window Functions são funções que fazem cálculos olhando para um conjunto de linhas relacionadas, sem remover as linhas originais da consulta.

Elas são muito úteis para:

* criar ranking;
* numerar linhas;
* comparar posições;
* buscar Top N;
* remover duplicidades;
* analisar dados mantendo o detalhe.

A estrutura básica é:

```sql
FUNCAO() OVER (
    PARTITION BY coluna
    ORDER BY coluna
)
```

Onde:

* `OVER()` indica que será usada uma Window Function.
* `PARTITION BY` separa os dados em grupos.
* `ORDER BY` define a ordem dentro de cada grupo.

---

Vamos usar uma tabela simples chamada `venda_cliente`.

```sql
DROP TABLE IF EXISTS venda_cliente;

CREATE TABLE venda_cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL
);
```

Inserindo dados:

```sql
INSERT INTO venda_cliente (cliente, estado, valor_total) VALUES
('Ana', 'SP', 1500.00),
('João', 'SP', 1200.00),
('Maria', 'SP', 1200.00),
('Carlos', 'SP', 800.00),
('Paula', 'RJ', 2000.00),
('Bruno', 'RJ', 1800.00),
('Fernanda', 'RJ', 1800.00),
('Rafael', 'RJ', 900.00);
```

Consultar os dados:

```sql
SELECT *
FROM venda_cliente
ORDER BY estado, valor_total DESC;
```

---

# ROW_NUMBER

## O que é?

`ROW_NUMBER()` cria uma numeração sequencial para as linhas.

Mesmo que duas linhas tenham o mesmo valor, ele gera números diferentes.


Usar quando você precisa numerar registros ou pegar o primeiro registro de cada grupo.

Exemplo:

> Criar uma posição dos clientes por estado, ordenando pelo maior valor vendido.

```sql
SELECT
    estado,
    cliente,
    valor_total,
    ROW_NUMBER() OVER (
        PARTITION BY estado
        ORDER BY valor_total DESC
    ) AS posicao
FROM venda_cliente
ORDER BY
    estado,
    posicao;
```

---

# RANK

## O que é?

`RANK()` cria ranking considerando empates.

Quando existe empate, ele dá a mesma posição para os empatados e pula a próxima posição.


Usar quando o empate deve ocupar a mesma posição no ranking.

Exemplo:

> Criar ranking dos clientes por estado, considerando empate de valor.

```sql
SELECT
    estado,
    cliente,
    valor_total,
    RANK() OVER (
        PARTITION BY estado
        ORDER BY valor_total DESC
    ) AS ranking
FROM venda_cliente
ORDER BY
    estado,
    ranking;
```

---

# DENSE_RANK

## O que é?

`DENSE_RANK()` também cria ranking considerando empates.

A diferença é que ele não pula posições depois do empate.


Usar quando você quer ranking com empate, mas sem saltar números.

Exemplo:

```sql
SELECT
    estado,
    cliente,
    valor_total,
    DENSE_RANK() OVER (
        PARTITION BY estado
        ORDER BY valor_total DESC
    ) AS ranking
FROM venda_cliente
ORDER BY
    estado,
    ranking;
```

---

# Comparando ROW_NUMBER, RANK e DENSE_RANK

```sql
SELECT
    estado,
    cliente,
    valor_total,

    ROW_NUMBER() OVER (
        PARTITION BY estado
        ORDER BY valor_total DESC
    ) AS row_number_posicao,

    RANK() OVER (
        PARTITION BY estado
        ORDER BY valor_total DESC
    ) AS rank_posicao,

    DENSE_RANK() OVER (
        PARTITION BY estado
        ORDER BY valor_total DESC
    ) AS dense_rank_posicao

FROM venda_cliente
ORDER BY
    estado,
    valor_total DESC;
```


## Resumo da diferença

| Função         | Considera empate? | Pula posição? |
| -------------- | ----------------- | ------------- |
| `ROW_NUMBER()` | Não               | Não se aplica |
| `RANK()`       | Sim               | Sim           |
| `DENSE_RANK()` | Sim               | Não           |

---

#  Deduplicação com ROW_NUMBER

## O que é deduplicação?

Deduplicação é o processo de remover registros duplicados, mantendo apenas um registro válido.

Em bases reais, duplicidades podem aparecer por vários motivos:

* carga repetida;
* integração com erro;
* reprocessamento de arquivo;
* cadastro duplicado;
* eventos recebidos mais de uma vez.

---

##  Criar tabela de exemplo

Vamos criar uma tabela chamada `cliente_evento2`.

Ela representa eventos de cadastro de clientes vindos de diferentes sistemas.

```sql
DROP TABLE IF EXISTS cliente_evento2;

CREATE TABLE cliente_evento2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    origem VARCHAR(50) NOT NULL,
    data_evento DATETIME NOT NULL
);
```

---

## Inserir dados duplicados

```sql
INSERT INTO cliente_evento2 (email, nome, origem, data_evento) VALUES
('ana@email.com', 'Ana', 'SITE', '2024-01-10 10:00:00'),
('ana@email.com', 'Ana Silva', 'CRM', '2024-01-12 09:00:00'),
('joao@email.com', 'João', 'APP', '2024-01-11 11:00:00'),
('joao@email.com', 'João Santos', 'CRM', '2024-01-15 08:00:00'),
('maria@email.com', 'Maria', 'SITE', '2024-01-13 14:00:00');
```

Observe que existem e-mails repetidos:

```text
ana@email.com
joao@email.com
```

A regra será:

> Para cada e-mail, manter apenas o registro mais recente.

---

##  Identificar o registro mais recente por e-mail

```sql
SELECT
    id,
    email,
    nome,
    origem,
    data_evento,
    ROW_NUMBER() OVER (
        PARTITION BY email
        ORDER BY data_evento DESC
    ) AS posicao
FROM cliente_evento2
ORDER BY
    email,
    posicao;
```

---

##  Retornar somente os registros deduplicados

```sql
WITH eventos_ordenados AS (
    SELECT
        id,
        email,
        nome,
        origem,
        data_evento,
        ROW_NUMBER() OVER (
            PARTITION BY email
            ORDER BY data_evento DESC
        ) AS posicao
    FROM cliente_evento2
)

SELECT
    id,
    email,
    nome,
    origem,
    data_evento
FROM eventos_ordenados
WHERE posicao = 1
ORDER BY
    email;
```


## Navegação
- [Anterior](11-exemplos-funcoes-de-agrupamento.md)
- [Próximo](13-tipos-de-union.md)
