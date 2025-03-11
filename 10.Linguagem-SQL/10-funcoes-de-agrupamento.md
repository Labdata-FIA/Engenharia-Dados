# Funções de Agrupamento em SQL

As funções de agrupamento são utilizadas para realizar cálculos em um conjunto de valores e retornar um único valor sumarizado. Essas funções são fundamentais em consultas SQL, especialmente úteis com a cláusula `GROUP BY`. Aqui estão os principais tipos de funções de agregação:

## 1. COUNT()
- **Descrição:** Conta o número de itens em um grupo.
- **Exemplo de Uso:** `COUNT(*)` para contar todos os registros em uma tabela; `COUNT(column_name)` para contar não nulos em uma coluna específica.

## 2. SUM()
- **Descrição:** Calcula a soma dos valores numéricos em uma coluna.
- **Exemplo de Uso:** `SUM(preco)` para calcular o total dos salários.

## 3. AVG()
- **Descrição:** Calcula a média dos valores numéricos.
- **Exemplo de Uso:** `AVG(preco)` para obter o preço médio dos produtos.

## 4. MAX()
- **Descrição:** Retorna o maior valor de uma coluna.
- **Exemplo de Uso:** `MAX(idade)` para encontrar a maior idade entre os participantes.

## 5. MIN()
- **Descrição:** Retorna o menor valor de uma coluna.
- **Exemplo de Uso:** `MIN(idade)` para encontrar a menor idade entre os participantes.

## 6. STDDEV()
- **Descrição:** Retorna o desvio padrão dos valores, uma medida da dispersão.
- **Exemplo de Uso:** `STDDEV(scores)` para calcular o desvio padrão de pontuações.

## 7. VAR() ou VARIANCE()
- **Descrição:** Calcula a variância dos valores, medindo a dispersão em relação à média.
- **Exemplo de Uso:** `VAR(population)` para analisar a variância da população entre cidades.

## Navegação
- [Anterior](09-exemplo-subselect.md)
- [Próximo](11-exemplos-funcoes-de-agrupamento.md)
