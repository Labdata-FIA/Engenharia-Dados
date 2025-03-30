# Lab DuckDB


## Disclaimer
> **As configurações dos Laboratórios é puramente para fins de desenvolvimento local e estudos**


## Pré-requisitos?
* Docker
* Docker-Compose

# Introdução ao DuckDB

DuckDB é um banco de dados OLAP embutido, projetado para consultas analíticas de alto desempenho em tabelas de colunas. Ele é eficiente para trabalhar com arquivos de dados locais como CSV, Parquet e JSON, sendo uma ótima alternativa para workloads analíticos em notebooks e pipelines de dados.

## Principais Características


- Permite consultas SQL diretas em arquivos CSV, Parquet e JSON.
- Suporte a operações vetorizadas, aumentando a eficiência de execução.
- Pode ser usado via CLI, Python, R e C++.
- Integração com pandas e Apache Arrow.

## Quando Usar o DuckDB?

- Para análises locais em grandes volumes de dados sem necessidade de um servidor dedicado.
- Para leitura e processamento de arquivos CSV e Parquet de forma rápida.
- Para integração com pandas e processamento analítico em notebooks Jupyter.
- Para workloads OLAP leves em ambientes embarcados.

## Instalação

>https://duckdb.org/docs/installation


## Trabalhando com a CLI do DuckDB

### Criando um banco de dados e uma tabela

```sh

docker compose up -d duckdb

docker exec -it duckdb bash

duckdb
```

Dentro da CLI, crie uma tabela:

```sql
CREATE TABLE clientes (
    id INTEGER,
    nome TEXT,
    idade INTEGER
);
```

### Listando as tabelas
```sql
.tables
```

### Inserindo Dados

```sql
INSERT INTO clientes VALUES (1, 'João', 30), (2, 'Maria', 25);
```

### Consultando Dados

```sql
SELECT * FROM clientes;
```

### Importando dados de um CSV

```sql
CREATE TABLE vendas AS SELECT * FROM read_csv('data/vendas.csv', delim = '|',
    header = true,
    columns = {
        'ID_Venda':'INTEGER',
        'Data_Venda':'DATE',
        'Produto':'VARCHAR',
        'Quantidade':'SMALLINT',
        'Preco_Unitario':'DOUBLE',
        'Total_Venda':'DOUBLE'
    });
SELECT * FROM vendas LIMIT 5;
```

### Exportando para Parquet

```sql
COPY vendas TO 'vendas.parquet' (FORMAT 'parquet');

SELECT * FROM read_parquet('vendas.parquet');

SELECT * 
FROM read_parquet('vendas.parquet')
WHERE Data_Venda > '2025-03-01';

```

## Executando Consultas no DuckDB

DuckDB otimiza planos de execução utilizando operações vetorizadas.

Verificando o plano de execução:

```sql
EXPLAIN SELECT * FROM vendas WHERE Total_Venda > 10;
```

### O que são Extensions no DuckDB?
Extensions no DuckDB são pacotes adicionais que expandem as capacidades do banco de dados. Eles permitem ao usuário interagir com fontes de dados externas, como sistemas de arquivos distribuídos, ou ler e escrever em formatos específicos de dados, como Parquet, CSV, JSON, entre outros. O plugin httpfs, por exemplo, permite que o DuckDB acesse dados de arquivos armazenados em servidores HTTP ou S3.

```sql
SELECT * FROM duckdb_extensions();
```


### Utilizando CTE (Common Table Expressions)

As CTEs permitem estruturar consultas complexas de maneira mais legível e organizada.

#### Exemplo 1: Filtrando clientes com mais de 25 anos

```sql
WITH clientes_filtrados AS (
    SELECT * FROM clientes WHERE idade > 25
)
SELECT * FROM clientes_filtrados;
```

#### Exemplo 2: Calculando total de vendas por cliente

```sql
WITH vendas_por_cliente AS (
    SELECT cliente_id, SUM(valor) AS total_vendas 
    FROM vendas 
    GROUP BY cliente_id
)
SELECT c.nome, v.total_vendas 
FROM clientes c
JOIN vendas_por_cliente v ON c.id = v.cliente_id;
```

## Ingestão de Dados no MinIO e Exportação para Parquet

```sql
INSTALL httpfs;
LOAD httpfs;

CREATE SECRET secret_minio  (
                TYPE S3,
                KEY_ID 'cursolab',
                SECRET 'cursolab',
                REGION 'us-east-1',
                ENDPOINT 'minio:9000',
                URL_STYLE 'path',
                USE_SSL false
                );

FROM duckdb_secrets();

COPY vendas TO 's3://bronze/vendas.parquet' (FORMAT 'parquet');
```


## Exemplo em Python (Jupyter Notebook)

Para exemplos práticos com Python, veja o arquivo `notebook.ipynb` incluído neste material.


