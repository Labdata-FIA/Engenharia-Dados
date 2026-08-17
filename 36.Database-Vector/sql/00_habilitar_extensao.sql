-- ============================================================
-- Bloco 1 | Script 00 — Habilitar a extensão pgvector
-- Execute no DBeaver, conectado ao banco "postgres"
-- ============================================================

-- 1. Habilita a extensão. O "IF NOT EXISTS" torna o script
--    idempotente: pode rodar quantas vezes quiser sem erro.
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Confirma que a extensão está registrada no catálogo.
--    A coluna extversion mostra a versão instalada.
SELECT extname, extversion
FROM pg_extension
WHERE extname = 'vector';

-- 3. Testa o tipo vector: o texto é convertido (cast) para vector.
--    Se este SELECT funcionar, o tipo está operacional.
SELECT '[1.0, 2.0, 3.0]'::vector AS vetor_teste;

-- 4. Lista as classes de operador disponíveis.
--    ATENÇÃO: esta lista é a chave dos índices. Cada classe
--    serve a UM operador de distância específico:
--      vector_l2_ops      -> operador <->  (euclidiana)
--      vector_cosine_ops  -> operador <=>  (cosseno)
--      vector_ip_ops      -> operador <#>  (produto interno)
--    Criar índice com a classe errada faz o Postgres IGNORAR
--    o índice silenciosamente. Esse é o erro nº 1 em produção.
SELECT
    am.amname       AS metodo_indice,
    opc.opcname     AS classe_operador
FROM pg_opclass opc
JOIN pg_am am ON am.oid = opc.opcmethod
WHERE opc.opcname LIKE 'vector%'
ORDER BY am.amname, opc.opcname;

-- 5. Versão do PostgreSQL, para registro.
SELECT version();
