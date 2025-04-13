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
- **SimpleStrategy**: Ideal para ambiente local ou de teste. Todos os dados são replicados dentro de um único data center.
  ```sql
  CREATE KEYSPACE exemplo_simple
  WITH replication = {
    'class': 'SimpleStrategy', 'replication_factor' : 2
  };
  ```

- **NetworkTopologyStrategy**: Recomendado para produção, pois permite configurar a quantidade de réplicas por data center.
  ```sql
  CREATE KEYSPACE exemplo_topologia
  WITH replication = {
    'class': 'NetworkTopologyStrategy', 'dc1': 2, 'dc2': 3
  };
  ```

---

## Caso de uso: Sistema de Pesquisa Acadêmica (Pós / MBA)
**Contexto**: Vamos simular um sistema para registrar publicações e orientações acadêmicas.

### Criando a tabela de pesquisadores:
```sql
CREATE TABLE pesquisadores (
    id UUID PRIMARY KEY,
    nome TEXT,
    area_pesquisa TEXT,
    email TEXT
);
```

### Criando a tabela de publicações:
```sql
CREATE TABLE publicacoes (
    id_publicacao UUID,
    id_pesquisador UUID,
    titulo TEXT,
    ano INT,
    evento TEXT,
    PRIMARY KEY (id_pesquisador, ano, id_publicacao)
);
```

### Inserindo dados
```sql
INSERT INTO pesquisadores (id, nome, area_pesquisa, email)
VALUES (uuid(), 'Dra. Ana Silva', 'Inteligência Artificial', 'ana@universidade.edu');

select * from pesquisadores;
 
INSERT INTO publicacoes (id_publicacao, id_pesquisador, titulo, ano, evento)
VALUES (uuid(), "550e8400-e29b-41d4-a716-446655440000", 'Redes Neurais Aplicadas', 2023, 'SBIA');
```

### Consultas
```sql
SELECT * FROM pesquisadores;
SELECT * FROM publicacoes WHERE id_pesquisador = 550e8400-e29b-41d4-a716-446655440000;
```

---

## Explorando mais
```bash
DESCRIBE TABLE publicacoes;
SELECT release_version FROM system.local;
```

---

