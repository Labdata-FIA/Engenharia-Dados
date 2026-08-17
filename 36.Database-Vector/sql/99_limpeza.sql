-- ============================================================
-- Script 99 — Limpeza do ambiente
-- Use ao final do laboratório, ou para recomeçar do zero.
-- ============================================================

DROP INDEX IF EXISTS vetores_massa_hnsw_idx;
DROP INDEX IF EXISTS vetores_massa_ivfflat_idx;
DROP INDEX IF EXISTS passeios_atributos_gin;

DROP TABLE IF EXISTS vetores_massa;
DROP TABLE IF EXISTS consulta_teste;
DROP TABLE IF EXISTS passeios;
DROP TABLE IF EXISTS documentos;

-- Conferência: nenhuma tabela do lab deve restar
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public';

-- A extensão pode ficar instalada. Se quiser remover mesmo:
-- DROP EXTENSION vector CASCADE;
