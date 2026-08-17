-- ============================================================
-- Bloco 4 | Script 07 — Índice IVFFlat (a alternativa)
-- ⏱️ A criação é bem mais rápida que a do HNSW.
-- ============================================================

-- COMO O IVFFLAT FUNCIONA (intuição):
-- Em vez de um grafo, ele divide o espaço em "bairros" (listas)
-- usando clusterização k-means. Cada vetor pertence ao bairro
-- cujo centro está mais próximo. Na busca, o banco olha só os
-- bairros mais promissores, não a cidade inteira.

DROP INDEX IF EXISTS vetores_massa_ivfflat_idx;

-- Quantas listas usar? Regra prática:
--   até 1M linhas   -> lists = linhas / 1000
--   acima de 1M     -> lists = sqrt(linhas)
-- Para 50.000 linhas: 50.000 / 1000 = 50
CREATE INDEX vetores_massa_ivfflat_idx
ON vetores_massa
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 50);

-- ⚠️ ARMADILHA: o IVFFlat precisa de DADOS na tabela para treinar
-- os clusters. Se você criar o índice numa tabela vazia e inserir
-- depois, os clusters ficam sem sentido e o recall despenca.
-- Regra: carregue os dados PRIMEIRO, crie o índice DEPOIS.

SELECT indexname,
       pg_size_pretty(pg_relation_size(indexname::regclass)) AS tamanho
FROM pg_indexes
WHERE tablename = 'vetores_massa'
ORDER BY indexname;

-- ------------------------------------------------------------
-- probes: quantos bairros visitar na busca
-- ------------------------------------------------------------
-- Padrão é 1 (rápido e impreciso). Regra prática: sqrt(lists).
SET ivfflat.probes = 7;

-- Desabilitamos o HNSW temporariamente para forçar o uso do IVFFlat
-- (com os dois índices presentes, o planejador prefere o HNSW).
BEGIN;
DROP INDEX vetores_massa_hnsw_idx;

EXPLAIN ANALYZE
SELECT rotulo FROM vetores_massa
ORDER BY embedding <=> (SELECT v FROM consulta_teste) LIMIT 5;

ROLLBACK;  -- desfaz o DROP: o índice HNSW continua existindo

-- ------------------------------------------------------------
-- Quando o IVFFlat vence o HNSW?
-- ------------------------------------------------------------
-- Compare o tempo de CRIAÇÃO e o TAMANHO dos dois índices acima.
--   IVFFlat: build rápido, ocupa pouco, recall menor (~95%)
--   HNSW:    build lento, ocupa mais RAM, recall alto (~99%)
-- Escolha IVFFlat quando: dados estáticos, memória limitada,
-- reindexação frequente é aceitável.
-- Escolha HNSW quando: dados mudam, precisão importa. (padrão)

-- ⚠️ MANUTENÇÃO: o IVFFlat degrada conforme você insere dados,
-- porque os centros dos clusters não se atualizam sozinhos.
-- Após inserir mais de ~10% de linhas novas:
--   REINDEX INDEX vetores_massa_ivfflat_idx;
-- O HNSW não tem esse problema — absorve inserções bem.
