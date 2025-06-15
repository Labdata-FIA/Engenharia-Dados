## Disclaimer
> **As configurações dos Laboratórios são puramente para fins de desenvolvimento local e estudos**

## Pré-requisitos
* Docker
* Docker Compose

---

## Subindo o Apache Cassandra com Docker Compose

```bash
docker-compose up -d cassandra cassandra-web
```

---

## Entrando no container Cassandra
```bash
docker exec -it cassandra bash
```

---

## Conectando no Cassandra (via cqlsh)
```bash
cqlsh
```
Se preferir conectar direto:
```bash
cqlsh 127.0.0.1 9042
```

---

## Explorando o help do CQLSH
```bash
help
help DESCRIBE
help CREATE_KEYSPACE
```

Exemplos:
```bash
DESCRIBE keyspaces;
DESCRIBE tables;
DESCRIBE KEYSPACE system;
```

---

## Criando um Keyspace
```sql
CREATE KEYSPACE universidade
WITH replication = {
  'class': 'SimpleStrategy', 
  'replication_factor': 1
};
```
Use o keyspace:
```sql
USE universidade;
```

### Estratégias de Replicação
 
O parâmetro `class` define **como os dados serão replicados no cluster**. Os valores mais comuns são:


| class | Descrição | Quando usar |
|-------|-----------|-------------|
| `SimpleStrategy` | Replica os dados para `replication_factor` nós, sem considerar topologia de data centers. | **Ambiente local, testes ou desenvolvimento.** Não indicado para produção. |
| `NetworkTopologyStrategy` | Permite definir quantidade de réplicas por data center. Respeita topologia física do cluster. | **Produção, ambientes multi data center ou nuvem.** |
| `LocalStrategy` | Usado internamente pelo keyspace `system` do próprio Cassandra. | **Não usar manualmente.** |


## Caso de uso: Sistema de Alunos e Produtos

**Contexto**: Sistema para registrar informações de alunos e produtos adquiridos.

### Criando a tabela de pesquisadores:

### Tabela de Alunos

```sql
CREATE TABLE alunos (
    id UUID PRIMARY KEY,
    nome TEXT,
    curso TEXT,
    email TEXT
);

describe table alunos;

drop table alunos;

alter table alunos
add nota decimal;

```

![Lab](/content/cassandra00.png)


> https://www.scylladb.com/glossary/cassandra-data-types/



### Conceitos Importantes: Partition Key e Clustering Columns

* Partition Key: é o primeiro campo (ou conjunto de campos) da chave primária. Ele determina em qual nó do cluster os dados serão armazenados. Cada valor de partition key gera uma "partição física" distinta no cluster. Exemplo: id_aluno é a partition key da tabela produtos.

* Clustering Columns: são os campos que aparecem após a partition key na chave primária. Eles definem como os dados serão organizados e ordenados dentro da partição. Exemplo: ano, id_produto são clustering columns na tabela produtos.

> Essa estrutura permite que o Cassandra otimize consultas que filtram por partition key e ordenam pelos clustering columns.


### Tabela de Produtos (Exemplo de Particionamento)

```sql
CREATE TABLE produtos (
    id_produto UUID,
    ano INT,   
    nome_produto TEXT,
    categoria TEXT,
    PRIMARY KEY (id_produto, ano)
);
```

### PRIMARY KEY:

- **Partition Key**: id_produto
- **Clustering Key**: ano
- Os dados são particionados por id_produto e ordenados pelo ano e dentro de cada particao.


### Inserindo Dados

```sql
INSERT INTO alunos (id, nome, curso, email, nota)
VALUES (uuid(), 'Carlos Silva', 'Engenharia de Dados', 'carlos@escola.edu', 10);

INSERT INTO produtos (id_produto,  nome_produto, ano, categoria)
VALUES (uuid(),  'Notebook Lenovo', 2023, 'Informática');
```


### Inserindo Dados com TTL (Time To Live)

O TTL define um tempo de expiração (em segundos) para o dado inserido.

Exemplo: o dado expira após 1 hora (3600 segundos):

```sql
INSERT INTO produtos (id_produto,  nome_produto, ano, categoria)
VALUES (uuid(), 'Licença Temporária', 2024, 'Software') USING TTL 3600;
```


### Inserindo dados
```sql
INSERT INTO pesquisadores (id, nome, area_pesquisa, email)
VALUES (uuid(), 'Dra. Ana Silva', 'Inteligência Artificial', 'ana@universidade.edu');

```

### Inserindo os mesmos dados
```sql
INSERT INTO pesquisadores (id, nome, area_pesquisa, email)
VALUES (<<pegar o id>>, 'Dra. Ana Silva', 'Inteligência Artificial', 'ana@universidade.edu');

```


### Consultando Dados

```sql
SELECT * FROM alunos;
SELECT * FROM produtos WHERE id_aluno = 550e8400-e29b-41d4-a716-446655440000;

```

### Consultando Dados

```sql
SELECT * FROM produtos WHERE id_aluno = 550e8400-e29b-41d4-a716-446655440000 LIMIT 5;
```

### Filtros sem usar Partition Key

Por padrão o Cassandra não permite filtrar diretamente por colunas que não pertencem à chave de particao. Exemplo abaixo vai falhar sem ALLOW FILTERING

```sql
SELECT * FROM produtos WHERE categoria = 'Software';
```
Para forçar a consulta (com risco de performance):
```sql
SELECT * FROM produtos WHERE categoria = 'Software' ALLOW FILTERING;
```

> Atenção: ALLOW FILTERING deve ser usado com muita cautela, pois pode gerar full scan e impactar desempenho.


### Criando um Índice Secundário

Para permitir consultas por uma coluna que não faz parte da chave primária, podemos criar um índice secundário. Exemplo:
```sql
CREATE INDEX ON produtos (categoria);
```

### Usando LIMIT

```sql
UPDATE alunos SET email = 'carlos.silva@escola.edu' WHERE id = 550e8400-e29b-41d4-a716-446655440000;
```

### Aggregate (exemplo com SUM)
>Importante: Agregações no Cassandra exigem que a partição esteja especificada
```sql
SELECT SUM(ano) FROM produtos WHERE id_aluno = 550e8400-e29b-41d4-a716-446655440000;
```

### GROUP BY
> O GROUP BY no Cassandra funciona apenas sobre uma partição completa.
```sql
SELECT ano, COUNT(*) FROM produtos WHERE id_aluno = 550e8400-e29b-41d4-a716-446655440000 GROUP BY ano;
```


### Update de Dados

```sql
UPDATE alunos SET email = 'carlos.silva@escola.edu' WHERE id = 550e8400-e29b-41d4-a716-446655440000;
```

### Update sem Where

```sql
UPDATE alunos SET email = 'carlos.silva@escola.edu' ;
```


### Se o registro não existir !?

```sql
UPDATE alunos SET email = 'carlos.silva@escola.edu'  WHERE id = 550e8400-e29b-41d4-a716-446655440000;
```

## Trabalhando com Collections: LIST, SET e MAP

### List (mantém ordem de inserção)

```sql
CREATE TABLE cursos_completos (
    id UUID PRIMARY KEY,
    nome TEXT,
    modulos LIST<TEXT>
);

INSERT INTO cursos_completos (id, nome, modulos)
VALUES (uuid(), 'Engenharia de Dados Completo', ['SQL', 'Cassandra', 'Kafka']);

UPDATE cursos_completos SET modulos = modulos + ['Spark'] WHERE id = <ID>;
```
> List pode ter dados repetidos

### Set (elementos únicos, sem ordem garantida)

```sql
CREATE TABLE certificados (
    id UUID PRIMARY KEY,
    nome TEXT,
    certificacoes SET<TEXT>
);

INSERT INTO certificados (id, nome, certificacoes)
VALUES (uuid(), 'João Pedro', {'Azure', 'AWS', 'GCP', 'AWS'});
```


### Map (chave-valor)

```sql
CREATE TABLE notas_finais (
    id UUID PRIMARY KEY,
    nome TEXT,
    notas MAP<TEXT, FLOAT>
);

INSERT INTO notas_finais (id, nome, notas)
VALUES (uuid(), 'Maria', {'Matematica': 8.5, 'IA': 9.0});

UPDATE notas_finais SET notas['BigData'] = 10.0 WHERE id = <ID>;
```


## Consistência (Consistency Level)
No cqlsh podemos ajustar o nível de consistência:

```sql
CONSISTENCY QUORUM;
CONSISTENCY ONE;
CONSISTENCY ALL;
```

* ONE: Apenas um nó precisa responder
* QUORUM: Maioria dos nós
* ALL: Todos os nós precisam responder


### Boas práticas de modelagem no Cassandra

* Modelagem orientada a consulta (query-based modeling)
* Evitar muitos updates (Cassandra prioriza insert-overwrite)
* Pensar em particionamento para escalabilidade
* Evitar particionamentos muito grandes (hot partitions)
* Clustering key bem definido permite ordenação eficiente

