# SELECT

Expressão simplificada que representa a estrutura formal do comando `SELECT` usando a forma BNF (Backus-Naur Form), uma notação usada para expressar gramáticas livres de contexto:

```
<consulta> ::= SELECT <lista_selecao>
               FROM <lista_tabelas>
               [ WHERE <condicao> ]
               [ GROUP BY <expressao_agrupamento> ]
               [ HAVING <condicao_agrupamento> ]
               [ ORDER BY <expressao_ordenacao> [ ASC | DESC ] ]

<lista_selecao> ::= <nome_coluna> | <nome_coluna> [ , <nome_coluna> ]...

<lista_tabelas> ::= <nome_tabela> | <nome_tabela> [ , <nome_tabela> ]...

<condicao> ::= <expressao>

<expressao_agrupamento> ::= <nome_coluna> | <nome_coluna> [ , <nome_coluna> ]...

<condicao_agrupamento> ::= <condicao>

<expressao_ordenacao> ::= <nome_coluna> | <nome_coluna> [ , <nome_coluna> ]...

<expressao> ::= <expressao_simples> | <expressao_simples> <operador> <expressao_simples>
<expressao_simples> ::= <nome_coluna> | <literal> | <funcao>([<nome_coluna>])
<operador> ::= = | != | > | < | >= | <= | AND | OR | NOT
<funcao> ::= COUNT | SUM | AVG | MIN | MAX | ...
```

## Explicação da Expressão BNF:

- **`<consulta>`**: Define a estrutura geral de uma consulta SQL usando `SELECT`. Inclui cláusulas opcionais para condições, agrupamentos, condições de grupo e ordenação.
- **`<lista_selecao>`**: Lista de colunas a serem selecionadas. Pode incluir várias colunas separadas por vírgulas.
- **`<lista_tabelas>`**: Lista de tabelas de onde os dados são extraídos. Pode também incluir várias tabelas separadas por vírgulas.
- **`<condicao>`, `<condicao_agrupamento>`**: Condições usadas para filtrar resultados na cláusula `WHERE` e para condições após um `GROUP BY` na cláusula `HAVING`.
- **`<expressao_agrupamento>`, `<expressao_ordenacao>`**: Especificam as colunas pelas quais os dados devem ser agrupados ou ordenados.
- **`<expressao>`**: Define expressões, que podem ser simples referências a colunas, literais, operações entre valores ou chamadas a funções de agregação.

# Tipos de Joins em SQL

Joins são usados para combinar registros de duas ou mais tabelas em um banco de dados, baseados em colunas relacionadas entre as tabelas. Abaixo estão os tipos principais de joins e suas características:

## 1. INNER JOIN
- **Descrição**: Retorna apenas os registros que têm correspondências em ambas as tabelas.
- **Uso comum**: Ideal para obter registros onde existem correspondências completas entre tabelas.

## 2. LEFT JOIN (ou LEFT OUTER JOIN)
- **Descrição**: Retorna todos os registros da tabela à esquerda e os registros correspondentes da tabela à direita. Resultados não correspondidos da direita terão `NULL`.
- **Uso comum**: Útil para encontrar registros na tabela à esquerda que podem ou não ter correspondentes na tabela à direita.

## 3. RIGHT JOIN (ou RIGHT OUTER JOIN)
- **Descrição**: Retorna todos os registros da tabela à direita e os registros correspondentes da tabela à esquerda. Resultados não correspondidos da esquerda terão `NULL`.
- **Uso comum**: Funciona como o LEFT JOIN, mas foca na tabela à direita.

## 4. FULL OUTER JOIN
- **Descrição**: Combina o resultado de LEFT e RIGHT JOINs. Retorna todos os registros quando há uma correspondência em pelo menos uma das tabelas.
- **Uso comum**: Utilizado para obter uma visão completa de ambos os conjuntos de dados, correspondentes ou não.

## 5. CROSS JOIN
- **Descrição**: Retorna o produto cartesiano das duas tabelas; combina cada linha de uma tabela com todas as linhas da outra tabela.
- **Uso comum**: Usado para análises e testes onde todas as combinações possíveis são necessárias.

## 6. SELF JOIN
- **Descrição**: Um join de uma tabela com ela mesma, utilizado para comparar registros na mesma tabela.
- **Uso comum**: Bom para encontrar registros relacionados ou duplicados dentro da mesma tabela.

## 7. NATURAL JOIN
- **Descrição**: Realiza um join usando colunas com o mesmo nome em ambas as tabelas.
- **Uso comum**: Simplifica joins entre tabelas onde colunas com nomes idênticos devem ser combinadas.

Cada tipo de join é escolhido com base nas necessidades específicas da consulta SQL e nos resultados desejados. A seleção adequada é essencial para a eficiência da consulta e precisão dos dados.


## Navegação
- [Anterior](06-exercicios-criar-view.md)
- [Próximo](08-exemplos-tipo-de-joins.md)
