-- ============================================================
-- Bloco 4 | Script 05 — Gerando volume para testar índices
-- ⏱️ Leva de 30s a 2min. Rode e aguarde.
-- ============================================================

-- Com 10 linhas todo índice parece inútil. Precisamos de escala
-- para que a diferença apareça. Vamos gerar 50.000 vetores
-- aleatórios de 128 dimensões — sem precisar de API nenhuma.

DROP TABLE IF EXISTS vetores_massa;

CREATE TABLE vetores_massa (
    id        SERIAL PRIMARY KEY,
    rotulo    TEXT,
    embedding vector(128)
);

-- Como funciona a geração:
--   generate_series(1,128) cria 128 linhas
--   random() gera um número por linha
--   array_agg junta tudo num array
--   ::vector(128) converte para o tipo vector
INSERT INTO vetores_massa (rotulo, embedding)
SELECT
    'documento_' || i,
    (SELECT array_agg(random())::vector(128)
     FROM generate_series(1, 128))
FROM generate_series(1, 50000) AS i;

-- Conferência
SELECT COUNT(*) AS total_linhas FROM vetores_massa;

-- Tamanho da tabela em disco.
-- Faça a conta: 128 dimensões x 4 bytes = 512 bytes por vetor.
-- Agora imagine 1536 dimensões e 10 milhões de linhas.
SELECT pg_size_pretty(pg_total_relation_size('vetores_massa')) AS tamanho;

-- ------------------------------------------------------------
-- BASELINE: quanto demora SEM índice?
-- ------------------------------------------------------------
-- Fixamos um vetor de consulta para que todos os testes usem
-- exatamente a mesma busca e sejam comparáveis.
DROP TABLE IF EXISTS consulta_teste;
CREATE TABLE consulta_teste AS
SELECT (SELECT array_agg(random())::vector(128)
        FROM generate_series(1,128)) AS v;

EXPLAIN ANALYZE
SELECT rotulo
FROM vetores_massa
ORDER BY embedding <=> (SELECT v FROM consulta_teste)
LIMIT 5;

-- 📝 ANOTE o "Execution Time" e confirme que aparece "Seq Scan".
-- Vamos comparar com os índices nos próximos scripts.
