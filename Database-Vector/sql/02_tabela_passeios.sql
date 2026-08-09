-- ============================================================
-- Bloco 2 | Script 02 — Criando a tabela e carregando dados
-- Retomamos o exemplo das viagens visto na teoria
-- ============================================================

-- Cada passeio é descrito por 3 características, numa escala 0 a 10.
-- Essas 3 características SÃO as 3 dimensões do vetor:
--   dimensão 1 = quanto tem de praia
--   dimensão 2 = quanto tem de aventura
--   dimensão 3 = quanto custa
-- Em um sistema real essas dimensões viriam de um modelo de ML
-- e seriam centenas ou milhares. Aqui são 3 para você conseguir
-- conferir a matemática de cabeça.

DROP TABLE IF EXISTS passeios;

CREATE TABLE passeios (
    id          SERIAL PRIMARY KEY,
    nome        TEXT NOT NULL,
    perfil      vector(3),                  -- [praia, aventura, custo]
    atributos   JSONB DEFAULT '{}',         -- metadados para filtros
    criado_em   TIMESTAMP DEFAULT NOW()
);

INSERT INTO passeios (nome, perfil, atributos) VALUES
('Cancún, México',        '[9.5, 3.0, 6.0]', '{"continente":"America","estacao":"verao","dias":7}'),
('Maldivas',              '[9.8, 2.5, 9.5]', '{"continente":"Asia","estacao":"verao","dias":10}'),
('Fernando de Noronha',   '[9.7, 4.0, 8.0]', '{"continente":"America","estacao":"verao","dias":6}'),
('Patagônia, Argentina',  '[1.0, 9.5, 7.0]', '{"continente":"America","estacao":"verao","dias":12}'),
('Nepal, trilha do Everest','[0.5, 9.9, 8.5]','{"continente":"Asia","estacao":"outono","dias":14}'),
('Chapada Diamantina',    '[2.0, 8.5, 3.0]', '{"continente":"America","estacao":"inverno","dias":5}'),
('Paris, França',         '[1.0, 2.0, 8.0]', '{"continente":"Europa","estacao":"primavera","dias":7}'),
('Roma, Itália',          '[1.5, 2.5, 7.5]', '{"continente":"Europa","estacao":"primavera","dias":6}'),
('Bangkok, Tailândia',    '[5.0, 5.0, 4.0]', '{"continente":"Asia","estacao":"inverno","dias":9}'),
('Cabo Frio, Brasil',     '[8.5, 3.5, 2.5]', '{"continente":"America","estacao":"verao","dias":4}');

-- Conferência: 10 linhas, 3 dimensões cada.
SELECT COUNT(*) AS total, vector_dims(perfil) AS dimensoes
FROM passeios
GROUP BY vector_dims(perfil);

SELECT id, nome, perfil, atributos->>'continente' AS continente
FROM passeios
ORDER BY id;

-- Estrutura da tabela (no DBeaver o \d não funciona; use isto):
SELECT column_name, data_type, udt_name
FROM information_schema.columns
WHERE table_name = 'passeios'
ORDER BY ordinal_position;
