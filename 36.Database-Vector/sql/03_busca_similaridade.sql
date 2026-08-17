-- ============================================================
-- Bloco 2 | Script 03 — Busca por similaridade (k-NN)
-- ============================================================

-- ------------------------------------------------------------
-- 1. "Quero uma viagem de praia, barata, sem aventura"
--    Traduzido em vetor: praia alta, aventura baixa, custo baixo
-- ------------------------------------------------------------
SELECT
    nome,
    perfil,
    perfil <=> '[9,2,3]'::vector          AS distancia,
    1 - (perfil <=> '[9,2,3]'::vector)    AS similaridade
FROM passeios
ORDER BY distancia          -- ordena do mais parecido ao menos
LIMIT 3;                    -- k = 3 vizinhos mais próximos

-- Isto é uma busca k-NN: para CADA linha da tabela o Postgres
-- calcula a distância, ordena e devolve as k primeiras.

-- ------------------------------------------------------------
-- 2. "Quero aventura, custo não importa"
-- ------------------------------------------------------------
SELECT nome, 1 - (perfil <=> '[1,9,5]'::vector) AS similaridade
FROM passeios
ORDER BY perfil <=> '[1,9,5]'::vector
LIMIT 3;

-- ------------------------------------------------------------
-- 3. As três métricas na mesma consulta
-- ------------------------------------------------------------
-- Os números NÃO são comparáveis entre colunas: cada métrica tem
-- sua própria escala. Compare a ORDEM, não os valores.
--   euclidiana: 0 a infinito
--   cosseno:    0 a 2
--   prod.interno: negativo, quanto mais negativo mais similar
SELECT
    nome,
    perfil <-> '[9,2,3]'::vector AS euclidiana,
    perfil <=> '[9,2,3]'::vector AS cosseno,
    perfil <#> '[9,2,3]'::vector AS produto_interno
FROM passeios
ORDER BY euclidiana;

-- ⚠️ EXPERIMENTO: rode a consulta acima ordenando por cada coluna
-- (troque o ORDER BY) e compare os rankings. Onde eles divergem?

-- ------------------------------------------------------------
-- 4. Itens parecidos com um item existente ("quem viu isso, viu também")
-- ------------------------------------------------------------
-- Padrão clássico de sistema de recomendação: usa o vetor de um
-- registro como consulta, excluindo ele mesmo do resultado.
SELECT
    p.nome,
    1 - (p.perfil <=> base.perfil) AS similaridade
FROM passeios p,
     (SELECT perfil FROM passeios WHERE nome = 'Cancún, México') AS base
WHERE p.nome <> 'Cancún, México'
ORDER BY p.perfil <=> base.perfil
LIMIT 3;

-- ------------------------------------------------------------
-- 5. Corte por limiar de similaridade
-- ------------------------------------------------------------
-- Sem o corte, uma busca SEMPRE devolve k resultados, mesmo que
-- todos sejam irrelevantes. Em RAG isso vira alucinação: o LLM
-- recebe contexto ruim e responde com confiança sobre nada.
SELECT nome, 1 - (perfil <=> '[9,2,3]'::vector) AS similaridade
FROM passeios
WHERE 1 - (perfil <=> '[9,2,3]'::vector) >= 0.95
ORDER BY perfil <=> '[9,2,3]'::vector;

-- ------------------------------------------------------------
-- 6. Como o Postgres executa isso hoje (sem índice)
-- ------------------------------------------------------------
EXPLAIN ANALYZE
SELECT nome FROM passeios
ORDER BY perfil <=> '[9,2,3]'::vector
LIMIT 3;

-- Procure no plano por "Seq Scan": o banco leu TODAS as linhas.
-- Com 10 linhas é instantâneo. Guarde essa observação — no Bloco 4
-- vamos repetir com 50.000 linhas e a história muda.
