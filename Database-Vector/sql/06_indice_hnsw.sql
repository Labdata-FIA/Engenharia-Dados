-- ============================================================
-- Bloco 4 | Script 06 — Índice HNSW (o padrão recomendado)
-- ⏱️ A criação leva de 1 a 3 minutos. É normal.
-- ============================================================

-- COMO O HNSW FUNCIONA (intuição):
-- Imagine um mapa rodoviário em camadas. A camada de cima só tem
-- rodovias entre grandes cidades; as de baixo têm ruas locais.
-- Para achar um endereço você pega a rodovia, chega perto da
-- cidade certa, desce de camada e refina. É isso: um grafo
-- navegável em múltiplas camadas (Hierarchical Navigable Small World).
-- Você nunca visita todos os pontos — só um caminho até o destino.

DROP INDEX IF EXISTS vetores_massa_hnsw_idx;

-- ⚠️ vector_cosine_ops precisa CASAR com o operador <=> da query.
--    Se você indexar com l2_ops e consultar com <=>, o Postgres
--    ignora o índice e faz Seq Scan sem avisar.
CREATE INDEX vetores_massa_hnsw_idx
ON vetores_massa
USING hnsw (embedding vector_cosine_ops)
WITH (
    m = 16,               -- conexões por nó. Maior = mais preciso, mais RAM
    ef_construction = 64  -- qualidade da construção. Maior = índice melhor, build mais lento
);

-- Tamanho do índice (compare com o tamanho da tabela!)
SELECT indexname,
       pg_size_pretty(pg_relation_size(indexname::regclass)) AS tamanho
FROM pg_indexes
WHERE tablename = 'vetores_massa';

-- ------------------------------------------------------------
-- Consultando com o índice
-- ------------------------------------------------------------
-- ef_search controla quantos candidatos são examinados na busca.
-- É o botão de ajuste entre VELOCIDADE e PRECISÃO, e vale só
-- para a sessão atual.
SET hnsw.ef_search = 40;

EXPLAIN ANALYZE
SELECT rotulo
FROM vetores_massa
ORDER BY embedding <=> (SELECT v FROM consulta_teste)
LIMIT 5;

-- 📝 Agora deve aparecer "Index Scan using vetores_massa_hnsw_idx".
--    Compare o Execution Time com o baseline do script 05.

-- ------------------------------------------------------------
-- Experimento: o efeito do ef_search
-- ------------------------------------------------------------
SET hnsw.ef_search = 10;    -- rápido e menos preciso
EXPLAIN ANALYZE
SELECT rotulo FROM vetores_massa
ORDER BY embedding <=> (SELECT v FROM consulta_teste) LIMIT 5;

SET hnsw.ef_search = 200;   -- lento e mais preciso
EXPLAIN ANALYZE
SELECT rotulo FROM vetores_massa
ORDER BY embedding <=> (SELECT v FROM consulta_teste) LIMIT 5;

SET hnsw.ef_search = 40;    -- volta ao padrão recomendado

-- ------------------------------------------------------------
-- ⚠️ O ponto mais importante deste bloco
-- ------------------------------------------------------------
-- O índice HNSW é APROXIMADO (ANN = Approximate Nearest Neighbor).
-- Ele pode NÃO encontrar o vizinho realmente mais próximo.
-- Você trocou exatidão por velocidade — conscientemente.
-- Rode a comparação abaixo e veja se os resultados batem:

-- Resultado APROXIMADO (usa o índice)
SET hnsw.ef_search = 10;
SELECT rotulo FROM vetores_massa
ORDER BY embedding <=> (SELECT v FROM consulta_teste) LIMIT 5;

-- Resultado EXATO (força varredura completa, ignorando o índice)
SET enable_indexscan = off;
SELECT rotulo FROM vetores_massa
ORDER BY embedding <=> (SELECT v FROM consulta_teste) LIMIT 5;
SET enable_indexscan = on;
SET hnsw.ef_search = 40;

-- As duas listas são iguais? Se não, você acabou de ver o
-- "recall" do índice na prática. Em produção mede-se isso.
