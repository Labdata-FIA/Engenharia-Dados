# Lab ElasticSearch


## Disclaimer
> **As configurações dos Laboratórios é puramente para fins de desenvolvimento local e estudos**


## Pré-requisitos?
* Docker
* Docker-Compose


Este laboratório demonstra como executar um ambiente local com Elasticsearch via Docker, criar e manipular índices, inserir documentos, realizar buscas e entender os mapeamentos de campos.


## 🚀 Executando o Elasticsearch

Para subir o ambiente local com Elasticsearch:

```bash
docker compose up -d elasticsearch  kibana
```

* Elastic
http://localhost:9200/

* kibana
http://localhost:5601/


## 📁 Índices

Nesta seção, vamos criar, alterar e excluir índices, além de entender brevemente o propósito de cada comando.

### 🔹 Criar índice

```bash
curl -X PUT http://localhost:9200/alunos -H "Content-Type: application/json"
```

```bash
curl -X PUT http://localhost:9200/aulas -H "Content-Type: application/json"
```

### O que aconteceu ?
```bash
docker exec -it elasticsearch /bin/bash
ls data/indices/

```

### 🔹 Consultar índice

```bash
curl -X GET http://localhost:9200/alunos
```


### ❌ Excluir índice

```bash

curl -X PUT http://localhost:9200/teste -H "Content-Type: application/json"

curl -X GET http://localhost:9200/teste

curl -X DELETE http://localhost:9200/teste
```

### 🔹 Criar índice com Mapeamento

> Cria o índice `alunos-custom` com um shard primário e sem réplica, definindo o mapeamento dos campos.


```bash
curl -X PUT http://localhost:9200/aluno-custom -H "Content-Type: application/json" -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "idaluno": { "type": "integer" },
      "nomeAluno": { "type": "text" },
      "data": { "type": "date", "format": "yyyy-MM-dd" }
    }
  }
}'
```

### 🔧 Alterar configurações do índice (ex: número de réplicas)

```bash
curl -X PUT http://localhost:9200/alunos/_settings -H "Content-Type: application/json" -d '{
  "index": {
    "number_of_replicas": 1
  }
}'
```


## 📄 Manipulação de Documentos

Aqui estão exemplos para criar, atualizar, excluir e consultar documentos.

### ➕ Criar documento

```bash
curl -X POST http://localhost:9200/alunos/_doc/1 -H "Content-Type: application/json" -d '{
  "idaluno": 1,
  "nomeAluno": "João Silva",
  "data": "2024-03-31"
}'

curl -X POST http://localhost:9200/alunos/_doc/2 -H "Content-Type: application/json" -d '{
  "idaluno": 2,
  "nomeAluno": "João Silva 2",
  "data": "2024-03-31"
}'

curl -X POST http://localhost:9200/alunos/_doc/3 -H "Content-Type: application/json" -d '{
  "idaluno": 3,
  "nomeAluno": "Maria",
  "data": "2024-03-31"
}'

```

### 🔄 Atualizar documento

```bash
curl -X POST http://localhost:9200/alunos/_update/1 -H "Content-Type: application/json" -d '{
  "doc": {
    "nomeAluno": "João Pedro Silva"
  }
}'
```


### ❌ Excluir documento

```bash
curl -X DELETE http://localhost:9200/alunos/_doc/3
```


### 🔍 Consultas com `_search`




No Elasticsearch, a forma como você busca por dados depende do tipo de consulta utilizada. Três das mais comuns são `match`, `match_phrase` e `term`, e cada uma possui uma finalidade específica:


#### ✅ `match` – Busca por termos analisados
Usada para campos do tipo `text`. O valor é processado (tokenizado e normalizado) pelo analyzer do campo antes da busca. Ideal para buscas mais flexíveis.

**Exemplo de uso:** Buscar alunos cujo nome contenha a palavra "João".

```bash
curl -X GET http://localhost:9200/alunos/_search -H "Content-Type: application/json" -d '{
 "query": {
  "match": {
    "nomeAluno": "João"
  }
  }
}'
```

**Caso de uso:** Busca por nomes, descrições ou campos textuais com múltiplas palavras.

#### ✅ `match_phrase` – Busca por frase exata
Também usada em campos `text`, mas considera a ordem e a proximidade das palavras.

**Exemplo de uso:** Buscar "João Pedro Silva" exatamente nessa ordem.
```bash
curl -X GET http://localhost:9200/alunos/_search -H "Content-Type: application/json" -d '{
"query": {
  "match_phrase": {
    "nomeAluno": "João Pedro Silva"
  }
}
}'
```

**Caso de uso:** Títulos, nomes completos, endereços, frases exatas.

#### ✅ `term` – Busca exata (não analisada)
Usada para campos `keyword`, `integer`, `boolean`, etc. O valor não é analisado.

**Exemplo de uso:** Buscar por um ID específico.
```bash
curl -X GET http://localhost:9200/alunos/_search -H "Content-Type: application/json" -d '{
"query": {
  "term": {
    "idaluno": 1
  }
}
}'
```

**Caso de uso:** Filtros exatos, códigos, identificadores únicos, status fixos.

#### `prefix` — busca por prefixo (ex: autocomplete)
```bash
curl -X GET http://localhost:9200/alunos/_search -H "Content-Type: application/json" -d '{
"query": {
  "prefix": {
    "nomeAluno": "joão"
  }
}
}'
```

#### `ids` — busca por múltiplos `_id`
```bash
curl -X GET http://localhost:9200/alunos/_search -H "Content-Type: application/json" -d '{
"query": {
  "ids": {
    "values": ["1", "2"]
  }
}
}'
```

#### `match_all` — retorna todos os documentos
```bash
curl -X GET http://localhost:9200/alunos/_search -H "Content-Type: application/json" -d '{
"query": {
  "match_all": {}
}
}'
```

## 🧬 Mapeamento de Documentos

O mapeamento define a estrutura dos dados no Elasticsearch.

### 📌 Exemplo de mapeamento

```json
"mappings": {
  "properties": {
    "idaluno":    { "type": "integer" },
    "nomeAluno":  { 
      "type": "text",
      "fields": {
        "raw": { "type": "keyword" }
      }
    },
    "data":       { "type": "date", "format": "yyyy-MM-dd" }
  }
}
```

```bash
curl -X GET  http://localhost:9200/alunos/_mapping
```


```bash
curl -X PUT  http://localhost:9200/materias -H "Content-Type: application/json" -d '{
  
  "mappings": {
    "properties": {
      "idmateria":   { "type": "integer" },
      "nomeMateria": { "type": "text" },
      "data":        { "type": "date", "format": "yyyy-MM-dd" }
    }
  }
}'
```

---

## 🔎 Analisando Tokens (Tokenização com `_analyze`)

### O que são tokens?

Tokens são as menores unidades de texto geradas durante o processo de análise no Elasticsearch. Por exemplo, a frase "João Pedro Silva" pode ser dividida em três tokens: "joão", "pedro" e "silva". A criação desses tokens permite buscas mais eficazes em campos do tipo `text`.

O comando `_analyze` permite simular esse processo e entender como o Elasticsearch transforma seu texto ao indexar ou buscar dados.

Veja como o Elasticsearch interpreta os termos de um campo:

```bash
curl -X POST http://localhost:9200/_analyze -H "Content-Type: application/json" -d '{
  "analyzer": "standard",
  "text": "João Pedro Silva"
}'
```

> Campos do tipo `text` são tokenizados. Por isso, buscas exatas precisam de campos do tipo `keyword`.

### ✨ Analyzers comuns:

| Analyzer       | Descrição                                                    |
|----------------|--------------------------------------------------------------|
| `standard`     | Default – quebra por palavras, lowercase, remove pontuação   |
| `whitespace`   | Divide por espaço em branco, sem lowercase                   |
| `keyword`      | Trata o campo inteiro como um único token (ideal para `term`)|
| `custom`       | Você define seu próprio tokenizer e filtros                  |

---


## Exemplo de Uso de Alias com Filtro no Elasticsearch


Este exemplo demonstra como criar dois índices (`matriz` e `filial`), adicionar documentos com os campos `id`, `nome` e `parceiro`, e configurar um **alias com filtro** para retornar apenas os documentos onde `parceiro = "VIP"`.

### 🧱 1. Criar os Índices

```bash
curl -X PUT http://localhost:9200/matriz -H "Content-Type: application/json" -d '
{
  "mappings": {
    "properties": {
      "id": { "type": "integer" },
      "nome": { "type": "text" },
      "parceiro": { "type": "keyword" }
    }
  }
}'


curl -X PUT http://localhost:9200/filial -H "Content-Type: application/json" -d '
{
  "mappings": {
    "properties": {
      "id": { "type": "integer" },
      "nome": { "type": "text" },
      "parceiro": { "type": "keyword" }
    }
  }
}'

```

### 📟 2. Inserir Documentos


```bash
curl -X POST http://localhost:9200/matriz/_doc/1 -H "Content-Type: application/json" -d '
{
  "id": 1,
  "nome": "Empresa João Silva",
  "parceiro": "CLASS"
}'

curl -X POST http://localhost:9200/filial/_doc/1 -H "Content-Type: application/json" -d '
{
  "id": 1,
  "nome": "Empresa João Silva",
  "parceiro": "VIP"
}'

curl -X POST http://localhost:9200/filial/_doc/2 -H "Content-Type: application/json" -d '
{
  "id": 1,
  "nome": "Empresa Maria Silva",
  "parceiro": "CLASS"
}'
```



### 🏷️ 3. Criar o Alias

```bash
curl -X POST http://localhost:9200/_aliases -H "Content-Type: application/json" -d '
{
  "actions": [
    { "add": { "index": "matriz", "alias": "empresas" } },
    { "add": { "index": "filial", "alias": "empresas" } }
  ]
}'
```


### 🔍 4. Buscar Documentos via Alias

```bash
curl -X GET  http://localhost:9200/empresas 
```

### 🏷️ 3. Criar o Alias com filtros
```bash
curl -X POST http://localhost:9200/_aliases -H "Content-Type: application/json" -d '
{
  "actions": [
    {
      "add": {
        "index": "matriz",
        "alias": "class",
        "filter": {
          "term": {
            "parceiro": "CLASS"
          }
        }
      }
    },
    {
      "add": {
        "index": "filial",
        "alias": "class",
        "filter": {
          "term": {
            "parceiro": "CLASS"
          }
        }
      }
    }
  ]
}'
```

```bash
curl -X GET http://localhost:9200/_aliases

curl -X GET http://localhost:9200/class
```

## 🔍 4. Buscar Documentos via Alias de filtro

```bash
curl -X GET http://localhost:9200/class/_search 
```