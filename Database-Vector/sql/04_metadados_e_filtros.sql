-- ============================================================
-- Bloco 3 | Script 04 — Metadados JSONB + busca híbrida
-- Esta é a maior vantagem do pgvector sobre bancos vetoriais puros
-- ============================================================

-- ------------------------------------------------------------
-- 1. Consultando o JSONB
-- ------------------------------------------------------------
-- Operadores: ->> devolve TEXTO, -> devolve JSON
SELECT nome,
       atributos->>'continente' AS continente,
       (atributos->>'dias')::int AS dias
FROM passeios
WHERE atributos->>'continente' = 'America';

-- ------------------------------------------------------------
-- 2. Busca vetorial COM filtro estruturado
-- ------------------------------------------------------------
-- "Praia barata, mas só na América"
SELECT nome,
       atributos->>'continente' AS continente,
       1 - (perfil <=> '[9,2,3]'::vector) AS similaridade
FROM passeios
WHERE atributos->>'continente' = 'America'
ORDER BY perfil <=> '[9,2,3]'::vector
LIMIT 3;

-- É ISSO que justifica escolher pgvector: uma única query mistura
-- semântica (ORDER BY vetor) com regra de negócio (WHERE). Em um
-- banco vetorial separado você precisaria de dois sistemas e
-- sincronização entre eles.

-- ------------------------------------------------------------
-- 3. Vários filtros combinados
-- ------------------------------------------------------------
SELECT nome,
       atributos->>'estacao' AS estacao,
       (atributos->>'dias')::int AS dias,
       1 - (perfil <=> '[9,3,5]'::vector) AS similaridade
FROM passeios
WHERE atributos->>'estacao' = 'verao'
  AND (atributos->>'dias')::int <= 7
  AND 1 - (perfil <=> '[9,3,5]'::vector) >= 0.90
ORDER BY perfil <=> '[9,3,5]'::vector;

-- ------------------------------------------------------------
-- 4. Filtro por data
-- ------------------------------------------------------------
SELECT nome, criado_em
FROM passeios
WHERE criado_em > NOW() - INTERVAL '30 days'
ORDER BY perfil <=> '[9,2,3]'::vector
LIMIT 5;

-- ------------------------------------------------------------
-- 5. Índice para o filtro (não confundir com índice vetorial!)
-- ------------------------------------------------------------
-- O índice GIN acelera as buscas dentro do JSONB. Ele é
-- COMPLEMENTAR ao índice vetorial, não substituto.
CREATE INDEX IF NOT EXISTS passeios_atributos_gin
ON passeios USING gin (atributos);

EXPLAIN ANALYZE
SELECT nome FROM passeios
WHERE atributos @> '{"continente":"Asia"}';

-- ⚠️ ARMADILHA DE PRODUÇÃO: quando você combina WHERE restritivo
-- com índice vetorial, o índice ANN busca os k vizinhos PRIMEIRO
-- e só depois aplica o filtro. Se o filtro for muito seletivo,
-- você pode receber MENOS resultados que o LIMIT pedido — ou
-- nenhum. Soluções: aumentar hnsw.ef_search, ou usar índice
-- parcial por categoria. Teste isso com seus dados reais.
