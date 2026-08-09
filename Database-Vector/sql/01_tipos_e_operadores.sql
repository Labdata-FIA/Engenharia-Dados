-- ============================================================
-- Bloco 1 | Script 01 — O tipo vector e os operadores
-- Objetivo: entender a matemática ANTES de criar tabelas
-- ============================================================

-- ------------------------------------------------------------
-- 1. O tipo vector aceita conversão a partir de texto e de array
-- ------------------------------------------------------------
SELECT '[1,2,3]'::vector                AS de_texto;
SELECT ARRAY[1,2,3]::vector             AS de_array;
SELECT vector_dims('[1,2,3,4,5]'::vector) AS quantidade_dimensoes;

-- Norma (magnitude) do vetor: o "comprimento" da seta.
-- Para [3,4] a norma é 5 — o velho triângulo 3-4-5.
SELECT vector_norm('[3,4]'::vector) AS magnitude;

-- ------------------------------------------------------------
-- 2. Os  operadores de distância, lado a lado
-- ------------------------------------------------------------
-- Em TODOS eles: quanto MENOR o valor, mais parecidos os vetores.
SELECT
    '[1,2,3]'::vector <-> '[1,2,3]'::vector AS l2_identicos,
    '[1,2,3]'::vector <-> '[4,5,6]'::vector AS l2_diferentes,
    '[1,2,3]'::vector <=> '[2,4,6]'::vector AS cosseno_proporcionais,
    '[1,2,3]'::vector <-> '[2,4,6]'::vector AS l2_proporcionais;


-- ⚠️ PARE E OBSERVE a última linha do resultado acima.
-- [2,4,6] é exatamente [1,2,3] multiplicado por 2.
--   Pelo COSSENO  -> distância 0    (mesma direção, "idênticos")
--   Pela EUCLIDIANA -> distância 3,74 (pontos bem separados)
-- Mesma dupla de vetores, duas respostas. A escolha da métrica
-- não é detalhe: ela DEFINE o que significa "parecido".

-- ------------------------------------------------------------
-- 3. Por que isso importa em busca semântica
-- ------------------------------------------------------------
-- Imagine duas resenhas do mesmo filme, com a mesma opinião:
-- uma de 3 linhas e outra de 3 páginas. O embedding do texto
-- longo tende a ter magnitude maior, mas MESMA direção.
-- Se você usar euclidiana, o texto longo "afasta" artificialmente.
-- Por isso a recomendação padrão em RAG é o cosseno (<=>).

-- ------------------------------------------------------------
-- 4. Convertendo distância em SIMILARIDADE (0 a 1)
-- ------------------------------------------------------------
-- A distância de cosseno vai de 0 (igual) a 2 (oposto).
-- Usuário final entende melhor "95% similar" que "distância 0,05".
SELECT
    '[1,2,3]'::vector <=> '[1,2,3.1]'::vector       AS distancia,
    1 - ('[1,2,3]'::vector <=> '[1,2,3.1]'::vector) AS similaridade;

-- ------------------------------------------------------------
-- 5. Vetores normalizados: quando as métricas se equivalem
-- ------------------------------------------------------------
-- Normalizar = dividir o vetor pela própria norma, deixando
-- magnitude 1. Repare que as normas viram 1 e a distância de
-- cosseno entre os originais e os normalizados é a mesma.
SELECT
    vector_norm(l2_normalize('[3,4]'::vector))   AS norma_apos_normalizar,
    l2_normalize('[3,4]'::vector)                AS vetor_normalizado,
    '[1,2,3]'::vector <=> '[2,4,6]'::vector      AS cosseno_original,
    l2_normalize('[1,2,3]'::vector) <=> l2_normalize('[2,4,6]'::vector) AS cosseno_normalizado;

-- CONCLUSÃO: com vetores normalizados (norma = 1), euclidiana e
-- cosseno produzem a MESMA ORDENAÇÃO. Vários modelos de embedding
-- já entregam vetores normalizados — nesses casos a escolha da
-- métrica não muda o ranking, só o número exibido.
