# ❄️ Laboratório Prático — Snowflake

> **Objetivo:** Introduzir os conceitos fundamentais do Snowflake e aplicá-los em um pipeline real de ingestão e transformação de dados.

---

## 📋 Sumário

1. [O que é o Snowflake?](#1-o-que-é-o-snowflake)
2. [Histórico e Lançamento](#2-histórico-e-lançamento)
3. [Edições Disponíveis](#3-edições-disponíveis)
4. [Modelo de Custo](#4-modelo-de-custo)
5. [Conceitos Fundamentais](#5-conceitos-fundamentais)
   - Warehouse (Recurso Computacional)
   - Snowflake Projects: Guia de Funcionalidades
   - [Banco de Dados (Database)](#51-banco-de-dados-database)
   - [Schema](#52-schema)
   - [Tabela (Table)](#53-tabela-table)  
   - [Views](#56-views)
6. [Tasks](#8-tasks)
7. [Stream e CDC](#10-stream-e-cdc)
8. Exercícios
---

## 1. O que é o Snowflake?

O **Snowflake** é uma plataforma de dados em nuvem (Cloud Data Platform) projetada para armazenar, processar e analisar grandes volumes de dados. Ele é oferecido como **SaaS (Software as a Service)**, o que significa que não há necessidade de instalar ou gerenciar infraestrutura.

Suas principais características são:

- **Separação entre armazenamento e computação:** você pode escalar cada um de forma independente.
- **Multi-cloud:** roda sobre AWS, Azure e Google Cloud.
- **Elasticidade:** os recursos computacionais podem ser ligados, desligados e escalados conforme a demanda.
- **SQL nativo:** toda interação é feita através de SQL padrão, sem necessidade de linguagens proprietárias para a maioria das operações.
- **Compartilhamento de dados:** permite compartilhar dados entre organizações sem movimentar arquivos.

> 💡 **Analogia:** Pense no Snowflake como um banco de dados que vive 100% na nuvem, que você não precisa instalar, e onde você paga somente pelo que usa — como uma conta de luz.

---

## 2. Histórico e Lançamento

| Marco | Data |
|---|---|
| Fundação da empresa | 2012 — por Benoit Dageville, Thierry Cruanes e Marcin Zukowski |
| Lançamento em produção (AWS) | Outubro de **2014** |
| Disponibilização no Azure | 2018 |
| Disponibilização no Google Cloud | 2019 |
| IPO (abertura de capital) | Setembro de **2020** — maior IPO de software da história até então |

O Snowflake foi concebido com a premissa de **repensar o data warehouse** do zero para a era da nuvem, diferentemente de soluções tradicionais como Oracle ou SQL Server que foram adaptadas para a nuvem.

---

## 3. Edições Disponíveis

O Snowflake oferece quatro edições, cada uma com um conjunto crescente de funcionalidades:

| Edição | Perfil | Principais Recursos |
|---|---|---|
| **Standard** | Iniciantes e projetos menores | SQL completo, Time Travel (1 dia), compartilhamento básico |
| **Enterprise** | Empresas de médio e grande porte | Time Travel (90 dias), multi-cluster warehouse, materialização |
| **Business Critical** | Dados sensíveis e regulados | Criptografia avançada, suporte a HIPAA, PCI DSS |
| **Virtual Private Snowflake (VPS)** | Máxima segurança e isolamento | Ambiente 100% dedicado, sem compartilhamento de recursos |

> 💡 A maioria dos projetos corporativos usa a edição **Enterprise**.

---

## 4. Modelo de Custo

O Snowflake usa um modelo de **pagamento pelo uso (pay-as-you-go)** baseado em dois eixos:

### 4.1 Armazenamento
- Cobrado mensalmente com base no volume de dados comprimidos armazenados.
- Preço aproximado: **~$23/TB/mês** (on-demand) ou mais barato em capacidade pré-paga.

### 4.2 Computação (Créditos Snowflake)
- A unidade de cobrança é o **Snowflake Credit**.
- O consumo depende do **size** do warehouse e do tempo que ele fica ativo.
- Um warehouse `X-Small` consome **1 crédito/hora**. Um `Large` consome **8 créditos/hora**.
- Warehouses são **pausados automaticamente** quando inativas (configurável).

### 4.3 Serviços em Nuvem
- Uma pequena fração dos créditos cobre operações de metadados, autenticação e otimização de queries.

> ⚠️ **Dica:** Sempre pause o warehouse após os exercícios para não consumir créditos desnecessariamente.

```sql
-- Pausar warehouse manualmente
ALTER WAREHOUSE meu_warehouse SUSPEND;

-- Configurar auto-suspend em 60 segundos de inatividade
ALTER WAREHOUSE meu_warehouse SET AUTO_SUSPEND = 60;
```

---

## 5. Conceitos Fundamentais

### 5.1 Warehouse (Recurso Computacional)

![Cluster Showfloke](content/wharehouse.png)

O **Warehouse** é o motor de processamento do Snowflake. Ele é um cluster de servidores virtuais que executa as queries SQL. O armazenamento e a computação são completamente separados, então você pode ter múltiplos warehouses acessando o mesmo dado simultaneamente.

```sql
-- Criar um warehouse
CREATE WAREHOUSE lab_wh
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60        -- pausa após 60s de inatividade
    AUTO_RESUME = TRUE       -- liga automaticamente ao receber uma query
    INITIALLY_SUSPENDED = TRUE;

-- Usar o warehouse
USE WAREHOUSE lab_wh;
```

> 💡 **Importante:** O warehouse só consome créditos quando está **STARTED**. Ao pausar, o consumo cessa imediatamente.

---

### 1. Warehouse Type (Tipo)
Define a arquitetura do hardware. O tipo **Standard** é o mais comum para queries SQL e BI, enquanto o **Snowpark-optimized** oferece muito mais memória RAM por nó, sendo ideal para processamento de Machine Learning e códigos complexos em Python/Scala que rodam dentro do Snowflake.

### 2. Warehouse Size (Tamanho)
Refere-se à quantidade de recursos computacionais em um único cluster. Segue o modelo "T-shirt sizing":
* **X-Small (1 crédito/h):** Entrada, para tarefas leves.
* **Small (2 créditos/h):** Cargas de trabalho moderadas.
* **Medium (4 créditos/h):** Consultas mais pesadas.
* **Large a 6X-Large (8 a 512+ créditos/h):** Para processamento de Big Data em larga escala.
*Cada salto de tamanho dobra o poder de processamento (Scaling Up).*

### 3. Auto-Resume & Auto-Suspend (Gestão Automática)
Recursos de economia de custos. O **Auto-Suspend** desativa o warehouse automaticamente após um período de inatividade definido (evitando cobranças desnecessárias). O **Auto-Resume** reativa o warehouse instantaneamente assim que uma nova consulta é enviada.

### 4. Multi-cluster (Concorrência)

![Cluster Showfloke](content/wharehouse.png)

Permite que o warehouse escale horizontalmente (*Scaling Out*). Em vez de aumentar o tamanho de um único cluster, o Snowflake adiciona clusters idênticos para processar queries de múltiplos usuários ao mesmo tempo, eliminando filas de espera em horários de pico.

* Standard: Adicona e remove recuros (nós), conforme demanda. Muito bom para cargas que tem variações

* Economy: Adiciona e remove recursos (nós) baseado no processamento médio de um período

### 5. Query Acceleration Service - QAS (GPU)
Um serviço que atua como um "turbo" para consultas específicas que precisam ler volumes massivos de dados. Ele desvia o processamento de partes pesadas da query para recursos extras fora do seu warehouse, agilizando o resultado sem precisar redimensionar o warehouse inteiro.

### . Scale Factor (Fator de Escala)
É o limite configurável para o Query Acceleration Service. Ele define o quanto de recurso extra o QAS pode utilizar em relação ao tamanho atual do seu warehouse. Por exemplo, um Scale Factor de 10 permite que uma query use até 10 vezes a potência do seu tamanho base para ser concluída mais rápido.

---

### 5.2 Snowflake Projects: Guia de Funcionalidades

Dentro da interface do Snowflake, a secção de **Projects** agrupa ferramentas para desenvolvimento, visualização e automação. Abaixo estão os principais componentes:

![Cluster Showfloke](content/projects.png)


### 1. Workspaces
Permite que equipes agrupem componentes, Dashboards e outros recursos em ambientes compartilhados, facilitando a gestão de permissões e a organização por projeto.

### 2. Streamlit Apps
Permite desenvolver e hospedar aplicações interativas de dados diretamente no Snowflake usando Python. Ideal para criar ferramentas visuais para usuários finais.

### 3. Dashboards
Coleções de visualizações gráficas baseadas em queries SQL. Utilizados para monitoramento de métricas de negócio e compartilhamento de insights rápidos.

### 4. Add Packages
Integração com o repositório Anaconda para gerenciar bibliotecas Python externas. Essencial para usar pacotes como Pandas, NumPy ou Scikit-learn em Streamlit ou Snowpark.

### 5. Templates
Modelos pré-configurados que servem de ponto de partida. Ajudam a acelerar o desenvolvimento de novos Dashboards ou Apps garantindo consistência visual e estrutural.


### 5.3 Banco de Dados (Database)

O **Database** no Snowflake é o nível mais alto de organização de dados dentro de uma conta. Ele agrupa schemas e serve como um namespace isolado.

```sql
-- Criar um banco de dados
CREATE DATABASE lab_snowflake;

-- Usar o banco de dados
USE DATABASE lab_snowflake;
```

> 💡 Pense no Database como uma "pasta raiz" que contém todas as outras estruturas de dados do seu projeto.

---

### 5.3 Schema

O **Schema** é uma subdivisão dentro do banco de dados. Ele agrupa objetos relacionados como tabelas, views, stages e procedures.

```sql
-- Criar schemas dentro do banco
CREATE SCHEMA lab_snowflake.raw;       -- dados brutos
CREATE SCHEMA lab_snowflake.staging;   -- área de transformação
CREATE SCHEMA lab_snowflake.analytics; -- dados prontos para consumo

-- Selecionar o schema ativo
USE SCHEMA lab_snowflake.raw;
```

> 💡 É uma boa prática separar schemas por camada de dados (raw → staging → analytics), seguindo o padrão de arquitetura medallion.

---

### 5.4 Tabela (Table)

As **tabelas** no Snowflake são onde os dados ficam armazenados. Existem três tipos principais:

| Tipo | Descrição | Quando usar |
|---|---|---|
| **Permanent** | Dados persistentes com Time Travel e Fail-safe | Produção |
| **Transient** | Sem Fail-safe, menor custo de armazenamento | Staging, dados temporários |
| **Temporary** | Existem apenas durante a sessão atual | Queries intermediárias |

```sql
-- Tabela permanente
CREATE TABLE lab_snowflake.raw.vendas (
    id_venda     NUMBER AUTOINCREMENT PRIMARY KEY,
    id_cliente   NUMBER,
    produto      VARCHAR(100),
    valor        FLOAT,
    data_venda   TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Tabela transient (sem Fail-safe)
CREATE TRANSIENT TABLE lab_snowflake.staging.vendas_stg
    LIKE lab_snowflake.raw.vendas;
```

---


### 5.5 Views

Uma **View** é uma consulta SQL salva que se comporta como uma tabela virtual. O Snowflake oferece dois tipos principais:

**View padrão:** executa a query toda vez que é chamada.

```sql
CREATE VIEW lab_snowflake.analytics.vw_vendas_por_cliente AS
SELECT
    id_cliente,
    COUNT(*)    AS total_pedidos,
    SUM(valor)  AS total_gasto
FROM lab_snowflake.raw.vendas
GROUP BY id_cliente;
```

**Materialized View:** o resultado é armazenado fisicamente e atualizado automaticamente pelo Snowflake (disponível na edição Enterprise).

```sql
CREATE MATERIALIZED VIEW lab_snowflake.analytics.mv_vendas_diarias AS
SELECT
    DATE(data_venda) AS dia,
    SUM(valor)       AS total_dia
FROM lab_snowflake.raw.vendas
GROUP BY dia;
```

> 💡 Use **views padrão** para simplicidade e **materialized views** quando a query é cara e acessada com alta frequência.

---



## 6. Tasks

Uma **Task** é um objeto do Snowflake que permite **agendar e automatizar a execução de comandos SQL** em intervalos regulares, sem depender de ferramentas externas como Airflow ou Azure Data Factory.


### 6.1 Tasks em Cadeia 

```sql
-- Task B só executa após a Task A
CREATE TASK task_b
    AFTER task_a
AS
    MERGE INTO ...;
```

> 💡 Tasks são ideais para orquestrar pipelines simples dentro do próprio Snowflake. Para fluxos complexos com múltiplas dependências, considere ferramentas dedicadas de orquestração.

---


## 7. Stream e CDC

### O que é CDC?

**CDC (Change Data Capture)** é a técnica de capturar e rastrear todas as mudanças (INSERT, UPDATE, DELETE) que ocorrem em uma tabela ao longo do tempo, sem precisar fazer um scan completo toda vez.

### O que é um Stream?

Um **Stream** no Snowflake é a implementação nativa de CDC. Ele é um objeto que **monitora as alterações** em uma tabela e expõe essas mudanças como um conjunto de linhas que pode ser consultado e consumido.

Cada linha do Stream contém metadados especiais:

| Coluna | Descrição |
|---|---|
| `METADATA$ACTION` | Tipo da ação: `INSERT` ou `DELETE` |
| `METADATA$ISUPDATE` | `TRUE` se a linha faz parte de um UPDATE |
| `METADATA$ROW_ID` | Identificador único da linha alterada |

> 💡 Um UPDATE no Snowflake aparece no Stream como um **DELETE + INSERT** (par de linhas).

```sql
-- Criar um stream sobre a tabela de vendas brutas
CREATE STREAM lab_snowflake.raw.stream_vendas
    ON TABLE lab_snowflake.raw.vendas
    APPEND_ONLY = FALSE;  -- FALSE = captura INSERT, UPDATE e DELETE

-- Visualizar as mudanças pendentes
SELECT
    *,
    METADATA$ACTION,
    METADATA$ISUPDATE
FROM lab_snowflake.raw.stream_vendas;
```

### Como o Stream funciona?

O Stream mantém um **offset (ponteiro)** que indica até onde as mudanças já foram consumidas. Ao fazer um DML (INSERT/MERGE) que lê o Stream dentro de uma transação, o offset avança automaticamente. Isso garante que cada mudança seja processada **exatamente uma vez**.

```sql
-- Consumir o stream: mover dados novos para a tabela de staging
INSERT INTO lab_snowflake.staging.vendas_stg
SELECT id_venda, id_cliente, produto, valor, data_venda
FROM lab_snowflake.raw.stream_vendas
WHERE METADATA$ACTION = 'INSERT';
-- Após este INSERT, o offset do stream avança
```

## 8. Exercícios
---

## 📚 Referências

- [Documentação oficial do Snowflake](https://docs.snowflake.com)
- [Snowflake Quickstarts](https://quickstarts.snowflake.com)
- [Snowflake Pricing](https://www.snowflake.com/pricing/)
- [Snowpipe com Azure](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-azure)
- [Time Travel & Fail-safe](https://docs.snowflake.com/en/user-guide/data-time-travel)

---
