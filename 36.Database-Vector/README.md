# Laboratório Prático — Banco de Dados Vetorizado com pgvector

---
## Disclaimer
> **Esta configuração é puramente para fins de desenvolvimento local e estudos**
> 

---


O foco é **SQL**. Os notebooks Python são demonstrações opcionais para mostrar de onde vêm os vetores no mundo real.

---



## Preparando o ambiente


### Subindo os containers

```bash
docker compose up -d pgvector notebook_pgvector pgadmin_vector
```


A imagem `pgvector/pgvector:pg16` já traz a extensão compilada. Uma imagem `postgres` comum **não** traz — você teria que compilar dentro do container.

---

##  Conectando no Banco PostgreSql


### Provisionando Banco de dados PostgreSQL e a ferramenta PgAdmin


Acesso para o PgAdmin http://localhost:5433/


* Login: lab-pgadmin4@pgadmin.org
* Senha : postgres    

* Nome do server: postgres
* Nome do Host Name: pgvector
* database: postgres
* Username: postgres
* password: postgres

### Tela de login do PgAdmin
![Exemplo Kafka Conect](../content/login-pgadmin.png)

### Preencha:

| Campo | Valor |
|---|---|
| Host | `pgvector` |
| Porta | `5432` |
| Database | `postgres` |
| Usuário | `postgres` |
| Senha | `postgres` |



### Abrindo os scripts

**SQL Editor → Abrir arquivo SQL** e selecione o script da pasta `sql/`.


---

##  Habilitando o pgvector

**Arquivos:** `00_habilitar_extensao.sql`, `01_tipos_e_operadores.sql`

### O script de habilitação

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Uma extensão no PostgreSQL adiciona tipos, operadores e funções novas ao banco.
O `IF NOT EXISTS` deixa o script **idempotente**: rodar duas vezes não dá erro.
Escreva sempre assim em script de setup.

```sql
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
```

`pg_extension` é o catálogo do sistema. Se esta consulta não retornar nada, a
extensão não foi habilitada — provavelmente você está conectado no banco errado.
**Extensão é por banco de dados, não por servidor.**

```sql
SELECT '[1.0, 2.0, 3.0]'::vector AS vetor_teste;
```

O `::` é o operador de cast do PostgreSQL. Aqui um texto vira um valor do tipo
`vector`. Se este SELECT funcionar, o tipo está operacional.

### As classes de operador

```sql
SELECT am.amname AS metodo_indice, opc.opcname AS classe_operador
FROM pg_opclass opc
JOIN pg_am am ON am.oid = opc.opcmethod
WHERE opc.opcname LIKE 'vector%';
```

Guarde esta tabela — ela reaparece no Bloco 4 e é a origem do erro mais comum
em produção:

| Classe de operador | Serve ao operador | Métrica |
|---|---|---|
| `vector_l2_ops` | `<->` | Distância euclidiana |
| `vector_cosine_ops` | `<=>` | Distância de cosseno |
| `vector_ip_ops` | `<#>` | Produto interno |

**Se a classe do índice não casar com o operador da consulta, o PostgreSQL
ignora o índice — sem erro, sem aviso.** A query continua funcionando, só que
lenta. Muita gente descobre isso em produção.

### Os operadores

```sql
SELECT
    '[1,2,3]'::vector <=> '[2,4,6]'::vector AS cosseno,
    '[1,2,3]'::vector <-> '[2,4,6]'::vector AS euclidiana;
```


- **Cosseno:** distância `0` — mesma direção, considerados idênticos.
- **Euclidiana:** distância `3,74` — pontos bem separados no espaço.

Os mesmos dois vetores, duas respostas opostas. A pergunta "qual está certo?"
não tem resposta, porque cada métrica responde a uma pergunta diferente:

| Operador | Pergunta que responde |
|---|---|
| `<->` euclidiana | Quão longe um ponto está do outro? |
| `<=>` cosseno | Os dois apontam para o mesmo lado? |

**A regra de decisão:** a magnitude do vetor carrega informação que me interessa?
Se sim, euclidiana. Se não, cosseno.

Em busca semântica a resposta é quase sempre "não": duas resenhas do mesmo filme,
uma de 3 linhas e outra de 3 páginas, têm o mesmo assunto mas magnitudes bem
diferentes. Por isso RAG usa cosseno por padrão.

> **Alívio:** quando os vetores estão normalizados (norma = 1), as duas métricas
> produzem exatamente a mesma **ordenação**. Vários modelos de embedding já
> entregam vetores normalizados — nesses casos a escolha não altera o ranking.
> O script `01` demonstra isso com `l2_normalize()`.

---

## Armazenando e buscando vetores

**Arquivos:** `02_tabela_passeios.sql`, `03_busca_similaridade.sql`

### A tabela

```sql
CREATE TABLE passeios (
    id          SERIAL PRIMARY KEY,
    nome        TEXT NOT NULL,
    perfil      vector(3),
    atributos   JSONB DEFAULT '{}',
    criado_em   TIMESTAMP DEFAULT NOW()
);

-- 1. Passeio focado em Aventura / Natureza (Trilha na Serra)
INSERT INTO passeios (nome, perfil, atributos) VALUES (
    'Trilha do Pico das Almas',
    '[0.95, 0.10, 0.30]',
    '{"categoria": "Ecoturismo", "dificuldade": "Alta", "duracao_horas": 6, "pet_friendly": false}'
);

-- 2. Passeio focado em Cultura e História (Museu/Centro Histórico)
INSERT INTO passeios (nome, perfil, atributos) VALUES (
    'Visita Guiada ao Centro Histórico',
    '[0.10, 0.98, 0.17]',
    '{"categoria": "Cultura", "dificuldade": "Baixa", "duracao_horas": 3, "guia_incluso": true}'
);

-- 3. Passeio focado em Custo / Gastronomia e Lazer (Tour Gastronômico)
INSERT INTO passeios (nome, perfil, atributos) VALUES (
    'Tour Gastronômico Noturno',
    '[0.20, 0.30, 0.93]',
    '{"categoria": "Gastronomia", "dificuldade": "Baixa", "duracao_horas": 4, "inclui_bebidas": true}'
);

-- 4. Passeio Equilibrado (Aventura + Cultura)
INSERT INTO passeios (nome, perfil, atributos) VALUES (
    'Expedição Arqueológica de Caiaque',
    '[0.71, 0.71, 0.00]',
    '{"categoria": "Aventura Cultural", "dificuldade": "Media", "duracao_horas": 5, "equipamento_incluso": true}'
);

-- 5. Passeio de Relaxamento / Baixo Custo
INSERT INTO passeios (nome, perfil, atributos) VALUES (
    'Piquenique no Parque Florestal',
    '[0.30, 0.20, 0.93]',
    '{"categoria": "Lazer", "dificuldade": "Baixa", "duracao_horas": 2, "pet_friendly": true}'
);

```

Observe: o vetor é **apenas mais uma coluna**. Ao lado dele convivem texto, JSONB
e timestamp, todos indexáveis e filtráveis, com transações ACID e joins normais.
Essa é a tese inteira do pgvector — você não precisa de um banco separado.

O `vector(3)` fixa a dimensão. Tentar inserir um vetor de tamanho diferente dá
erro, e isso é bom: pega na hora o bug de ter trocado de modelo de embedding sem
migrar os dados.

Usamos 3 dimensões — praia, aventura e custo — porque você consegue conferir a
matemática de cabeça. Um modelo real produziria 384, 768 ou 1536 dimensões, sem
nomes legíveis.

### A busca k-NN

```sql
SELECT nome,
       1 - (perfil <=> '[9,2,3]'::vector) AS similaridade
FROM passeios
ORDER BY perfil <=> '[9,2,3]'::vector
LIMIT 3;
```

* Forte busca por Aventura (peso $9$)
* Pouco interesse em Cultura (peso $2$)
* Interesse moderado em Gastronomia/Lazer (peso $3$)

Três partes:

- `<=>` calcula a distância de cada linha até o vetor de consulta.
- `ORDER BY` ordena do mais próximo ao mais distante.
- `LIMIT 3` corta nos 3 primeiros — o **k** do k-NN.

O `1 - distância` converte para similaridade de 0 a 1. Distância é melhor para
ordenar; similaridade é melhor para exibir ao usuário. "94% de compatibilidade"
comunica; "distância 0,06" não.

### Como o PostgreSQL executa isso

```sql
EXPLAIN ANALYZE
SELECT nome FROM passeios
ORDER BY perfil <=> '[9,2,3]'::vector LIMIT 3;
```

Procure por `Seq Scan` no plano. Sem índice, o algoritmo é:

1. **Seq Scan** — lê todas as N linhas da tabela.
2. **Projeção** — calcula a distância de cada uma. Com N linhas e d dimensões,
   são N × d operações.
3. **Top-N heapsort** — com `LIMIT`, não ordena tudo: mantém uma heap de tamanho
   k e descarta o resto.

Isso é uma busca **exata** e **O(N)**. Com 10 linhas, instantâneo. Guarde essa
observação: no Bloco 4 repetimos com 50 mil linhas.

### O corte de relevância

```sql
WHERE 1 - (perfil <=> '[9,2,3]'::vector) >= 0.95
```

Sem essa cláusula, a busca **sempre** devolve k resultados — mesmo que todos
sejam irrelevantes. Em RAG, é exatamente assim que nasce a alucinação: o LLM
recebe contexto ruim e responde com confiança sobre nada.

---

## Busca híbrida com metadados

**Arquivo:** `04_metadados_e_filtros.sql`

### O argumento central do pgvector

```sql
SELECT nome,
       1 - (perfil <=> '[9,2,3]'::vector) AS similaridade
FROM passeios
WHERE atributos->>'dificuldade' = 'Baixa'
ORDER BY perfil <=> '[9,2,3]'::vector
LIMIT 3;
```

* - Aventura: 9
* - Cultura: 2
* - Gastronomia: 3


Uma única consulta combinando **semântica** (`ORDER BY` vetorial) com **regra de
negócio** (`WHERE` tradicional). Num banco vetorial dedicado você precisaria de
dois sistemas, sincronização entre eles e uma consistência que ninguém garante.

Operadores JSONB que aparecem no script:

| Operador | O que faz |
|---|---|
| `->>` | Extrai o valor como **texto** |
| `->` | Extrai o valor como **JSON** |
| `@>` | Testa se o JSON **contém** outro (usa índice GIN) |

### Índice para os filtros

```sql
CREATE INDEX passeios_atributos_gin ON passeios USING gin (atributos);
```

Este índice acelera as buscas dentro do JSONB. Ele é **complementar** ao índice
vetorial, não substituto — um cuida do `WHERE`, o outro do `ORDER BY`.


---

## Índices e desempenho

**Arquivos:** `05_dataset_massa.sql`, `06_indice_hnsw.sql`, `07_indice_ivfflat.sql`

### Gerando volume sem API

```sql

CREATE TABLE IF NOT EXISTS vetores_massa (
    id        SERIAL PRIMARY KEY,
    rotulo    TEXT NOT NULL,
    embedding vector(128) NOT NULL,
    criado_em TIMESTAMP DEFAULT NOW()
);

INSERT INTO vetores_massa (rotulo, embedding)
SELECT 'documento_' || i,
       (SELECT array_agg(random())::vector(128) FROM generate_series(1, 128))
FROM generate_series(1, 50000) AS i;
```

Lendo de dentro para fora: `generate_series(1,128)` cria 128 linhas, `random()`
gera um número em cada, `array_agg` junta num array e `::vector(128)` converte.
O `generate_series(1, 50000)` externo repete isso 50 mil vezes.

Vetores aleatórios não têm significado semântico, mas para medir desempenho de
índice isso não importa — o custo de calcular distância é o mesmo.

### HNSW — a intuição

Imagine um mapa rodoviário em camadas. A camada de cima só tem rodovias entre
grandes cidades; as de baixo têm ruas locais. Para achar um endereço você pega a
rodovia, chega perto da cidade certa, desce de camada e refina. Você nunca visita
todos os pontos — só percorre um caminho até o destino.

```sql
CREATE INDEX vetores_massa_hnsw_idx
ON vetores_massa USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

| Parâmetro | O que controla | Padrão |
|---|---|---|
| `m` | Conexões por nó no grafo. Maior = mais preciso, mais RAM | 16 |
| `ef_construction` | Buffer de Exploração, Esforço na construção. Maior = índice melhor, build mais lento | 64 |

---


## Referência rápida

### Operadores

| Operador | Métrica | Faixa | Quando usar |
|---|---|---|---|
| `<->` | Euclidiana (L2) | 0 a ∞ | Magnitude importa |
| `<=>` | Cosseno | 0 a 2 | Busca semântica (padrão) |
| `<#>` | Produto interno negativo | negativo | Vetores já normalizados |

### Funções úteis

```sql
vector_dims(v)      -- número de dimensões
vector_norm(v)      -- magnitude (comprimento)
l2_normalize(v)     -- devolve o vetor com norma 1
```


### Diagnóstico

```sql
-- Tamanho dos índices
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass))
FROM pg_indexes WHERE tablename = 'sua_tabela';

-- O índice está sendo usado?
EXPLAIN ANALYZE SELECT ... ORDER BY embedding <=> '[...]' LIMIT 5;
-- "Index Scan" = sim | "Seq Scan" = não
```

### Dimensões por modelo

| Modelo | Dimensões |
|---|---|
| BGE-small | 384 |
| Gemini embedding | 768 |
| OpenAI text-embedding-3-small | 1536 |
| OpenAI text-embedding-3-large | 3072 |

---
