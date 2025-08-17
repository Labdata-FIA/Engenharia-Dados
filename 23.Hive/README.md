# Lab Armazenamento Distribuido


## Disclaimer
> **As configurações dos Laboratórios é puramente para fins de desenvolvimento local e estudos**


## Pré-requisitos?
* Docker
* Docker-Compose


Este laboratório foi criado para praticar, de ponta a ponta, os conceitos principais do Hive. A ideia é mostrar, na prática, como usar Hive para consultar dados em HDFS, incluindo criação de bancos, tabelas, inserções, particionamento, tabelas externas, uso de múltiplos arquivos CSV, propriedades, e execução de scripts `.hql`.

## 📦 Estrutura de diretórios HDFS

A estrutura a ser criada no HDFS será a seguinte:

```

├── bronze/
│   └── alunos/
    └── produtos/

```

> [!IMPORTANT]
> Criando as pastas para o container PostGreSql


```bash

mkdir ./postgresql/volume/pg_notify
mkdir ./postgresql/volume/pg_tblspc
mkdir ./postgresql/volume/pg_twophase
mkdir ./postgresql/volume/pg_stat
mkdir ./postgresql/volume/pg_logical/mappings
mkdir ./postgresql/volume/pg_commit_ts
mkdir ./postgresql/volume/pg_snapshots
mkdir ./postgresql/volume/pg_stat_tmp
```


---



```bash
docker container rm $(docker ps -a -q) -f
docker volume prune

docker compose up -d datanode namenode hive metastore minio

docker exec -it namenode bash

```

* > http://localhost:9864/
* > http://localhost:9870/
* > http://localhost:10002/

### 🔍 Verificar modo seguro (Safe Mode)

```bash
hdfs dfsadmin -safemode get
```

### Se o retorno for `Safe mode is OFF` então não está, pode pular o proximo comando.

### 🚫 Sair do modo seguro manualmente

```bash
hdfs dfsadmin -safemode leave

hdfs fsck -delete

exit
```

## 🚀 Comandos iniciais

### Criar diretórios no HDFS

```bash
//Caso esteja o container namenode
exit 

docker exec -it hive bash
hdfs dfs -mkdir -p /bronze/alunos
hdfs dfs -mkdir -p /bronze/produtos/
```
### Deu certo ?
> http://localhost:9870/

> Se Precisar subir muitos arquivo - hdfs dfs -put /tmp/exercicio_vendas/* /user/hive/warehouse/exercicio_vendas/
---

## 📂 Exercícios práticos


### Enviando arquivos `alunos.csv` `produtos.csv` para o HDFS

```bash
hdfs dfs -put /util/alunos.csv /bronze/alunos/
hdfs dfs -put /util/produtos.csv /bronze/produtos/
```

### Visualização dos dados

```bash
hdfs dfs -ls /bronze/alunos/
hdfs dfs -cat /bronze/produtos/produtos.csv
```


### Conectar no Beeline

```bash
beeline -u jdbc:hive2://localhost:10000
```

> Se pedir login, use qualquer usuário (ex: `hive`) e pressione Enter para senha vazia.


### Conectar pelo Dbeaver
![HFDS](/content/hive-01.png)

![HFDS](/content/hive-02.png)


### Criando o  banco de dados

```sql
CREATE DATABASE IF NOT EXISTS db;

SHOW DATABASES;

DROP DATABASE db CASCADE;



```
#### CASCADE
* Remove o banco de dados e todas as tabelas dentro dele.
* Tabelas internas: arquivos apagados do HDFS.
* Tabelas externas: arquivos permanecem no HDFS, mas o metadado é removido.


```sql
CREATE DATABASE IF NOT EXISTS aula_hive;
USE aula_hive;

SELECT current_database();
```

### Encontre o caminho do banco de dados 

> /opt/hive/data/warehouse
> No arquivo  `23.Hive/config/hive-site.xml`tem a propriedade `metastore.warehouse.dir`definindo esse diretorio


```sql
CREATE DATABASE IF NOT EXISTS dbhive location '/fia/aula';
```


```sql

USE aula_hive;

CREATE TABLE pessoas (
  id INT,
  nome STRING,
  idade INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

INSERT INTO pessoas VALUES (1, 'Maria', 22);
INSERT INTO pessoas VALUES (2, 'João', 25);
INSERT INTO pessoas VALUES (3, 'Ana', 20);

SELECT * FROM pessoas;

show tables;
```

|                                  | **Tabela Interna**             | **Tabela Externa**        |
|----------------------------------|--------------------------------|---------------------------|
| **Local dos dados**              | HDFS (gerenciado pelo Hive)    | HDFS (ou outro local), gerenciado pelo usuário |
| **Quem gerencia os dados?**      | Hive                           | Usuário                  |
| **Arquivos apagados ao dropar?** | ✅ Sim                          | ❌ Não                 |
| **Quando usar?**                 | Quando o Hive controla tudo    | Quando os dados já existem ou são compartilhados |


- Tabelas internas são totalmente gerenciadas pelo Hive.  
- Tabelas externas só armazenam metadados; os arquivos físicos permanecem após o drop.

### Metadados

```sql

DESCRIBE DATABASE aula_hive;
DESCRIBE pessoas;
DESCRIBE FORMATTED pessoas;

```

### Consultando Hcatalog (Conectando ao PostgreSql)

![HFDS](/content/hive-postgres.png)


![HFDS](/content/hive-postgres_01.png)
```sql
select * from public."DBS";

select * from  public."TBLS" where "DB_ID"= <<pegar o id do banco do resulta da query acima>>

select * from "COLUMNS_V2" where "CD_ID" = <<pegar o id da tabela do resultada da query acima>>
```


### Carregando dados do HFDS

```sql

CREATE TABLE alunos (
  id INT,
  nome STRING,
  idade INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

LOAD DATA INPATH '/bronze/alunos/alunos.csv' into table alunos;

select * from alunos;

```

```sql

CREATE EXTERNAL TABLE IF NOT EXISTS produtos (
  id_produto INT,
  nome_produto STRING,  
  valor_total DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/bronze/produtos/'
TBLPROPERTIES ("skip.header.line.count"="1");

select * from produtos;

```

>Com skip.header.line.count=1, apenas as linhas com dados serão carregadas.
>Por padrão, o valor é 0, ou seja, não ignora nenhuma linha.
>Se o seu arquivo não tiver cabeçalho, mantenha 0.


### Criando tabelas de uma query

```sql
create table produto_cafe as select * from produtos where id_produto =  2;
```

### Exemplos de queries Hive

### WHERE
```sql
SELECT * 
FROM alunos 
WHERE idade > 23;
```

### ORDER BY
```sql
SELECT * 
FROM alunos 
ORDER BY idade DESC;
```

### LIMIT
```sql
SELECT * 
FROM alunos 
ORDER BY idade DESC
LIMIT 2;
```

### Agregação (COUNT e AVG)
```sql
SELECT COUNT(*) as total_alunos, AVG(idade) as media_idade
FROM alunos;
```

### GROUP BY
```sql
SELECT idade, COUNT(*) as qtd
FROM alunos
GROUP BY idade;
```

### LIKE
```sql
SELECT * 
FROM alunos
WHERE nome LIKE 'M%';
```

### BETWEEN
```sql
SELECT * 
FROM alunos
WHERE idade BETWEEN 21 AND 25;
```


### JOIN

> [!IMPORTANT]
> Precisa criar a tabela compras para os alunos

```sql
SELECT a.nome, c.valor_total
FROM alunos a
JOIN compras c
ON a.id = c.id_cliente;
```


### Salvando resultados de consultas no HDFS
```sql
insert overwrite directory
'/result-alunos/' select * from alunos;

```

### Em outro terminal
```bash

docker exec -it hive bash
hdfs dfs -ls '/result-alunos/'
hdfs dfs -cat  /result-alunos/000000_0
```


## Particionamento

### No outro terminal, onde esta ativo o container do Hive.

```bash
hdfs dfs -mkdir -p /bronze/aluno_particionamento/ano=2025/mes=06/dia=01
hdfs dfs -put /util/alunos.csv /bronze/aluno_particionamento/ano=2025/mes=06/dia=01/

```

### No terminal do Hive, criar tabela particionada
```sql
USE aula_hive;

CREATE EXTERNAL TABLE IF NOT EXISTS aluno_particionamento (
  id INT,
  nome STRING,
  idade INT
)
PARTITIONED BY (ano INT, mes INT, dia INT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/bronze/aluno_particionamento';

```
> [!IMPORTANT]
> No HDFS, as pastas representam as partições: 
> Os nomes das pastas devem ter o mesmo nome das colunas de partição (ano, mes, dia), para o Hive reconhecer.

```sql
MSCK REPAIR TABLE aluno_particionamento;
SELECT * FROM aluno_particionamento;
```
> O comando MSCK REPAIR TABLE nome_tabela; serve para atualizar as informações de partições no metastore do Hive. 



## Exemplo de View no Hive

### O que é uma View?

Uma view no Hive é uma definição lógica de uma consulta. Ela não armazena dados físicos no HDFS, apenas a query fica salva no metastore.

```sql
CREATE VIEW alunos_maiores_23_view AS
SELECT *
FROM alunos
WHERE idade > 23;

SELECT * FROM alunos_maiores_23_view;

SHOW VIEWS;

SHOW TABLES;

SHOW CREATE TABLE alunos_maiores_23_view;

```

### No PostgreSql

```sql
select * from  public."TBLS"
```


### O que acontece internamente?

* Não é criado nenhum arquivo no HDFS.
* O Hive apenas salva o SQL da view no metastore.
* Quando você faz um SELECT na view, o Hive executa a query original na hora, como se fosse uma query normal.




## Exemplo completo usando ORC

### O que é ORC?

ORC (Optimized Row Columnar) é um formato de arquivo colunar otimizado, muito usado no Hive para melhorar compressão e performance de leitura.



### Criar tabela ORC
```bash
CREATE TABLE alunos_orc (
  id INT,
  nome STRING,
  idade INT
)
STORED AS ORC;

INSERT INTO alunos_orc SELECT * FROM alunos;

```


### O que acontece no HDFS?

* O Hive cria uma pasta para a tabela, por exemplo: /opt/hive/data/warehouse/aula_hive.db/alunos_orc.
* Os arquivos dentro dessa pasta são salvos no formato ORC (compactados e colunar).
* Cada arquivo ORC armazena dados em blocos, otimizando leitura e reduzindo espaço em disco.


### Vantagens do ORC


* Leituras mais rápidas para consultas analíticas.
* Suporte nativo a predicate pushdown (filtros mais eficientes).

> Para grandes volumes, use ORC para performance e economia de armazenamento. 


### Preparando estrutura para tabela Parquet
```sql

CREATE EXTERNAL TABLE IF NOT EXISTS bf (
  User_ID BIGINT,
  Product_ID STRING,
  Gender STRING,
  Age STRING,
  Occupation INT,
  City_Category STRING,
  Stay_In_Current_City_Years STRING,
  Marital_Status INT,
  Product_Category_1 INT,
  Product_Category_2 INT,
  Product_Category_3 INT,
  Purchase FLOAT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/bronze/bf/';

```

### No outro terminal, dentro do container do hive
```bash
hdfs dfs -put '/util/bf.csv' /bronze/bf/
```

```sql

select  * from  bf ;

```


### Criando o Tipo Parquet

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS  bf_parquet (
  User_ID BIGINT,
  Product_ID STRING,
  Gender STRING,
  Age STRING,
  Occupation INT,
  City_Category STRING,
  Stay_In_Current_City_Years STRING,
  Marital_Status INT,
  Product_Category_1 INT,
  Product_Category_2 INT,
  Product_Category_3 INT,
  Purchase FLOAT
)
STORED AS parquet
LOCATION '/bronze/bf_parquet/';

insert into bf_parquet
select * from bf ;

```

## Armazenando os arquivo no Minio

> http://localhost:9001/login

* Usuario: admin
* Senha: minioadmin

![HFDS](/content/hive-03.png)

![HFDS](/content/hive-04.png)

```sql

CREATE DATABASE aula LOCATION 's3a://raw/aula';

show databases;

CREATE EXTERNAL TABLE IF NOT EXISTS aula.bf (
  User_ID BIGINT,
  Product_ID STRING,
  Gender STRING,
  Age STRING,
  Occupation INT,
  City_Category STRING,
  Stay_In_Current_City_Years STRING,
  Marital_Status INT,
  Product_Category_1 INT,
  Product_Category_2 INT,
  Product_Category_3 INT,
  Purchase FLOAT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3a://raw//aula/bf/'
TBLPROPERTIES ("skip.header.line.count"="1");

```

![HFDS](/content/hive-05.png)

### Depois que subiu o arquivo
```sql
select *  from aula.bf;
```
