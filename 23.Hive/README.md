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

---

* > http://localhost:9864/
* > http://localhost:9870/

```bash
docker container rm $(docker ps -a -q) -f
docker volume prune

docker compose up -d datanode namenode hive metastore minio

docker exec -it namenode bash

```


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

DROP DATABASE aula_hive CASCADE;

```
#### CASCADE
* Remove o banco de dados e todas as tabelas dentro dele.
* Tabelas internas: arquivos apagados do HDFS.
* Tabelas externas: arquivos permanecem no HDFS, mas o metadado é removido.


```sql
CREATE DATABASE IF NOT EXISTS aula_hive;
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

### Local do arquivo
/user/hive/warehouse/<nome_tabela>

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

```

>Com skip.header.line.count=1, apenas as linhas com dados serão carregadas.
>Por padrão, o valor é 0, ou seja, não ignora nenhuma linha.
>Se o seu arquivo não tiver cabeçalho, mantenha 0.

### Em outro terminal

```bash
docker exec -it hive bash
hdfs dfs -put /util/produtos.csv /bronze/produtos/
```

### Volte para terminal que esta o hive ativo 
```sql
select * from produtos;
```

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

hdfs dfs -ls '/result-alunos/'
```
>Formato: JSON Serializado (padrão)

### Salvando resultados de consultas no HDFS, formato Delimitado

```sql
insert overwrite local directory
'/result-alunos-delimited/' row format 
delimited fields terminated by ','
select * from alunos;

hdfs dfs -ls '/result-alunos-delimited/'
```

## Particionamento

### No outro terminal, onde esta ativo o container do Hive.

```bash
hdfs dfs -mkdir -p /bronze/aluno_particionamento/ano=2025/mes=06/dia=01
hdfs dfs -put /util/alunos.csv /bronze/aluno_particionamento/ano=2025/mes=06/dia=01/

```

### Criar tabela particionada
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

### Configuração recomendada
Antes de criar tabelas ORC, configurar compressão (opcional):

```bash
SET hive.exec.compress.output=true;
SET orc.compress=SNAPPY;
```

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

### Inserir dados
```bash
INSERT INTO alunos_orc VALUES (1, 'Maria', 22);
INSERT INTO alunos_orc VALUES (2, 'João', 25);
INSERT INTO alunos_orc VALUES (3, 'Ana', 20);

SELECT * FROM alunos_orc;

```


### O que acontece no HDFS?

* O Hive cria uma pasta para a tabela, por exemplo: /user/hive/warehouse/alunos_orc.
* Os arquivos dentro dessa pasta são salvos no formato ORC (compactados e colunar).
* Cada arquivo ORC armazena dados em blocos, otimizando leitura e reduzindo espaço em disco.




### Vantagens do ORC

* Melhor compressão (até 75% menor).
* Leituras mais rápidas para consultas analíticas.
* Suporte nativo a predicate pushdown (filtros mais eficientes).

> Para grandes volumes, use ORC para performance e economia de armazenamento. 

