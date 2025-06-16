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

### Acesse:

* Elastic: http://localhost:9200/
* kibana: http://localhost:5601/


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

exit
```

### 🔹 Consultar índice

```bash
curl -X GET http://localhost:9200/alunos
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

### ❌ Excluir índice

```bash
curl -X DELETE http://localhost:9200/alunos
```

### Criar índice alunos com mapeamento

O mapeamento define a estrutura dos dados no Elasticsearch.

```bash
curl -X PUT http://localhost:9200/alunos -H "Content-Type: application/json" -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "idaluno": { "type": "integer" },
      "nomeAluno": { "type": "text", "fields": { "raw": { "type": "keyword" } } },
      "curso": { "type": "keyword" },
      "idade": { "type": "integer" },
      "dataCadastro": { "type": "date", "format": "yyyy-MM-dd" }
    }
  }
}'


curl -X GET  http://localhost:9200/alunos/_mapping

```

## 📄 Manipulação de Documentos

Aqui estão exemplos para criar, atualizar, excluir e consultar documentos.

### ➕ Criar documento

```bash
curl -X POST http://localhost:9200/alunos/_doc/1 -H "Content-Type: application/json" -d '{
  "idaluno": 1,
  "nomeAluno": "Fernanda Martins",
  "curso": "Engenharia",
  "idade": 27,
  "dataCadastro": "2024-05-01"
}'

curl -XGET  "http://localhost:9200/alunos/_doc/1"

```

### 🔄 Atualizar documento

> #### Substitui TODO o documento — se esquecer algum campo, o campo será apagado.
```bash
curl -X PUT http://localhost:9200/alunos/_doc/1 -H "Content-Type: application/json" -d '{
  "idaluno": 1,
  "nomeAluno": "Fernanda Martins",
  "curso": "Engenharia de Software",
  "idade": 27,
  "dataCadastro": "2024-05-01"
}'
```

> #### Apenas os campos informados serão atualizados.

```bash
curl -X POST http://localhost:9200/alunos/_update/1 -H "Content-Type: application/json" -d '{
  "doc": {
    "curso": "Engenharia de Produção",
    "idade": 28
  }
}'
```

> #### Atualização com script (exemplo de incremento de idade)

```bash
curl -X POST http://localhost:9200/alunos/_update/1 -H "Content-Type: application/json" -d '{
  "script": {
    "source": "ctx._source.idade += 1"
  }
}'
```

### ❌ Excluir documento

```bash
curl -X DELETE http://localhost:9200/alunos/_doc/1
```

| Operação               | Método         | Comportamento                    |
| ---------------------- | -------------- | -------------------------------- |
| Inserção               | `POST`         | Cria ou sobrescreve              |
| Atualização total      | `PUT`          | Substitui todo o documento       |
| Atualização parcial    | `POST _update` | Altera apenas os campos enviados |
| Atualização por script | `POST _update` | Executa lógica sobre o documento |
| Deleção                | `DELETE`       | Exclui o documento               |

```bash
curl -X POST http://localhost:9200/_bulk -H "Content-Type: application/json" --data-binary @07.NoSQL-Indexacao/alunos-bulk.json

```



### 🔍 Consultas

### 🔧 Busca simples com q=

```bash
curl -XGET "localhost:9200/alunos/_search?q=silva&pretty"
```


###  Busca com várias palavras (AND implícito)

```bash
curl -XGET "localhost:9200/alunos/_search?q=pedro+silva&pretty"
```
>Busca documentos que contenham ambos os termos: joao E silva.

###  Busca com OR explícito

```bash
curl -XGET "localhost:9200/alunos/_search?q=pedro+OR+maria&pretty"
```
>Retorna alunos com joao ou maria no nome.

###  Busca por frase exata (match_phrase)

```bash
curl -XGET "localhost:9200/alunos/_search?q=%22Maria%20Souza%22&pretty"
```

* %22 → aspas
* %20 → espaço

> busca exatamente Maria Souza


###   Busca com exclusão (NOT)

```bash
curl -XGET "localhost:9200/alunos/_search?q=pedro+-silva&pretty"
```
> Traz alunos que tenham Pedro mas não contenham silva.


### Busca com wildcard

```bash
curl -XGET "localhost:9200/alunos/_search?q=jo*&pretty"
```
> Pega qualquer token que comece com jo (ex: joao, jose).

### Busca com campo específico

```bash
curl -XGET "localhost:9200/alunos/_search?q=curso:Engenharia&pretty"

```
> Busca somente no campo curso (campo keyword).

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

**Exemplos:** Filtros exatos, códigos, identificadores únicos, status fixos.

>Se o Elasticsearch precisa pensar e entender o texto: match.
>Se eu quero que ele respeite a ordem exata: match_phrase.
>Se eu quero que ele só compare como se fosse um ==: term."


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


---

## 🔎 Analisando Tokens (Tokenização com `_analyze`)

### O que são tokens?

Tokens são as menores unidades de texto geradas durante o processo de análise no Elasticsearch. Por exemplo, a frase "João Pedro Silva" pode ser dividida em três tokens: "joão", "pedro" e "silva". A criação desses tokens permite buscas mais eficazes em campos do tipo `text`.

O comando `_analyze` permite simular esse processo e entender como o Elasticsearch transforma seu texto ao indexar ou buscar dados.

Veja como o Elasticsearch interpreta os termos de um campo:

```bash
curl -X POST http://localhost:9200/_analyze?pretty -H "Content-Type: application/json" -d '{
  "analyzer": "standard",
  "text": "João Pedro Silva"
}'
```

| Campo             | Significado                                                         |
| ----------------- | ------------------------------------------------------------------- |
| **token**         | O termo gerado. Ex: `joão`, `pedro`, `silva`                        |
| **start\_offset** | Onde começa esse token no texto original (em número de caracteres). |
| **end\_offset**   | Onde termina esse token (não inclusivo).                            |
| **type**          | O tipo de token (neste caso: `<ALPHANUM>`, ou seja, alfanumérico).  |
| **position**      | A posição do token na sequência de tokens (começando do zero).      |


> Campos do tipo `text` são tokenizados. Por isso, buscas exatas precisam de campos do tipo `keyword`.

### ✨ Analyzers comuns:

| Analyzer       | Descrição                                                    |
|----------------|--------------------------------------------------------------|
| `standard`     | Default – quebra por palavras, lowercase, remove pontuação   |
| `whitespace`   | Divide por espaço em branco, sem lowercase                   |
| `keyword`      | Trata o campo inteiro como um único token (ideal para `term`)|
| `custom`       | Você define seu próprio tokenizer e filtros                  |


### Normalizar o texto para evitar problemas com maiúsculas e acentuação.
```bash
curl -XPOST "localhost:9200/_analyze?pretty" -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "filter": ["lowercase", "asciifolding"],
  "text": "João Pédrô SílVA"
}'
```


### Eliminar palavras de baixo valor semântico para buscas.

```bash
curl -XPOST "localhost:9200/_analyze?pretty" -H "Content-Type: application/json" -d '{
  "tokenizer": "standard",
  "filter": ["lowercase", "stop"],
  "text": "the student fernando"
}'
```

## 🔧Trabalhando com sinônimos

### Criando analyzer com sinônimos:

```bash
curl -XPUT "localhost:9200/cursos?pretty" -H "Content-Type: application/json" -d '{
  "settings": {
    "analysis": {
      "filter": {
        "sinonimos_cursos": {
          "type": "synonym",
          "synonyms": [
            "Engenharia de Software, Desenvolvimento de Software, Programação",
            "Administração, Gestão, Negócios",
            "Marketing, Publicidade, Propaganda"
          ]
        }
      },
      "analyzer": {
        "analisador_com_sinonimos": {
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding", "sinonimos_cursos"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "idCurso": { "type": "integer" },
      "nomeCurso": { 
        "type": "text",
        "analyzer": "analisador_com_sinonimos"
      }
    }
  }
}'
```


### Testando o analyzer:

```bash
curl -XPOST "localhost:9200/cursos/_analyze?pretty" -H "Content-Type: application/json" -d '{
  "analyzer": "analisador_com_sinonimos",
  "text": "Administração"
}'
```

```bash
curl -XPOST "localhost:9200/cursos/_doc/1" -H "Content-Type: application/json" -d '{
  "idCurso": 1,
  "nomeCurso": "Engenharia de Software"
}'


curl -XPOST "localhost:9200/cursos/_doc/2" -H "Content-Type: application/json" -d '{
  "idCurso": 2,
  "nomeCurso": "Administração"
}'


curl -XPOST "localhost:9200/cursos/_search?pretty" -H "Content-Type: application/json" -d '{
  "query": {
    "match": {
      "nomeCurso": "Programação"
    }
  }
}'

curl -XPOST "localhost:9200/cursos/_search?pretty" -H "Content-Type: application/json" -d '{
  "query": {
    "match": {
      "nomeCurso": "Negócios"
    }
  }
}'

```
---


## Exemplo de Uso de Alias com Filtro no Elasticsearch


Este exemplo demonstra como criar dois índices (`matriz` e `filial`), adicionar documentos com os campos `id`, `nome` e `parceiro`, e configurar um **alias com filtro** para retornar apenas os documentos onde `parceiro = "VIP"`.

### 🧱 Criar os Índices

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


### 📟 Inserir Documentos


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



### 🏷️ Criar o Alias

```bash
curl -X POST http://localhost:9200/_aliases -H "Content-Type: application/json" -d '
{
  "actions": [
    { "add": { "index": "matriz", "alias": "empresas" } },
    { "add": { "index": "filial", "alias": "empresas" } }
  ]
}'
```


### 🔍 Buscar Documentos via Alias

```bash
curl -X GET  http://localhost:9200/empresas 

curl -X GET  http://localhost:9200/empresas/_search

curl -X GET  http://localhost:9200/_aliases

```



### 📟 Paginação Documentos

![Paginação](/content/paginacao-elastic.png)


Elasticsearch retorna os resultados em páginas.

Usamos dois parâmetros:

* from ➔ onde começar (offset)
* size ➔ quantos registros retornar por página

```bash
curl -XGET "localhost:9200/alunos/_search?pretty"
```

Por padrão: Traz os primeiros 10 documentos.

* from=0
* size=10


```bash
curl -XGET "localhost:9200/alunos/_search?from=0&size=5&pretty"
```

Começa do 0
Retorna os primeiros 5 documentos


```bash
curl -XGET "localhost:9200/alunos/_search?from=5&size=5&pretty"
```

Pula os 5 primeiros (from=5)
Retorna do documento 6 ao 10



### 🔬 O que é Fuzziness no Elasticsearch?
Fuzziness permite que o Elasticsearch encontre resultados aproximados, mesmo que o termo buscado tenha pequenas variações ou erros de digitação.

Por trás disso, o Elasticsearch usa o algoritmo de Levenshtein Distance (distância de edição), que calcula quantas operações de edição (inserção, remoção, substituição) são necessárias para transformar um termo em outro.


### 🔢 Exemplos de distância de edição:

| Palavra Original | Palavra Consultada | Distância |
| ---------------- | ------------------ | --------- |
| `sucesso`        | `sucesoo`          | 1         |
| `geracao`        | `geracap`          | 1         |
| `automatica`     | `automattica`      | 2         |


### 🚩 Observação prática:
O fuzziness funciona apenas em campos do tipo text (que passam por análise/tokenização).

Não funciona em keyword, pois o token inteiro seria comparado.

```bash
curl -XPOST "localhost:9200/alunos/_search?pretty" -H "Content-Type: application/json" -d '{
  "query": {
    "match": {
      "nomeAluno": {
        "query": "joao silvaa",
        "fuzziness": 1
      }
    }
  }
}'
```


### Fuzziness automático (AUTO)

```bash
curl -XPOST "localhost:9200/alunos/_search?pretty" -H "Content-Type: application/json" -d '{
  "query": {
    "match": {
      "nomeAluno": {
        "query": "joao silvaa",
        "fuzziness": "AUTO"
      }
    }
  }
}'
```

### O AUTO calcula o nível de tolerância com base no tamanho da palavra:

| Tamanho do termo | Fuzziness aplicado |
| ---------------- | ------------------ |
| 0-2 caracteres   | 0                  |
| 3-5 caracteres   | 1                  |
| 5+ caracteres    | 2                  |



## 📊 AGREGAÇÕES (E-COMMERCE)

```bash
curl -X PUT http://localhost:9200/produtos -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "idProduto": { "type": "integer" },
      "nome": { "type": "text" },
      "sku": { "type": "keyword" },
      "preco": { "type": "float" },
      "categoria": { "type": "keyword" }
    }
  }
}'
```

Inserir produtos (exemplo)

```bash
curl -X POST http://localhost:9200/produtos/_bulk -H "Content-Type: application/json" -d '
{ "index": { "_id": 1 } }
{ "idProduto": 1, "nome": "Notebook Dell", "sku": "N100", "preco": 3500, "categoria": "Eletrônicos" }
{ "index": { "_id": 2 } }
{ "idProduto": 2, "nome": "Smartphone Samsung", "sku": "S200", "preco": 2500, "categoria": "Eletrônicos" }
{ "index": { "_id": 3 } }
{ "idProduto": 3, "nome": "Tênis Nike", "sku": "T300", "preco": 400, "categoria": "Moda" }
{ "index": { "_id": 4 } }
{ "idProduto": 4, "nome": "Camisa Polo", "sku": "C400", "preco": 120, "categoria": "Moda" }
'

```


Agregação terms (por categoria)

```bash
curl -X POST "localhost:9200/produtos/_search?pretty" -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "por_categoria": {
      "terms": { "field": "categoria" }
    }
  }
}'

```


Agregação avg (média de preços)

```bash
curl -X POST "localhost:9200/produtos/_search?pretty" -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "media_preco": {
      "avg": { "field": "preco" }
    }
  }
}'

```

## 📊 Explorando o Kibana com os Índices Criados


### Acessando o Management

No menu lateral do Kibana, clique em:

Management → Kibana → Data Views


![Kibana](/content/elastic00.png)

### Criando um Data View

Clique em "Create data view".

Na tela de criação preencha:

* Data view name: alunos
* Index pattern: alunos
> (permite capturar qualquer índice que comece com alunos)

* Timestamp field: dataCadastro

> O campo dataCadastro deve estar mapeado no índice como tipo date.


![Kibana](/content/elastic01.png)


![Kibana](/content/elastic02.png)


### Acessando o Discover
Após criar o Data View, vá para o menu:

Analytics → Discover

![Kibana](/content/elastic03.png)


### Criando um Dashboard

No menu lateral, acesse:

Analytics → Dashboard

Clique em "Create Dashboard" para montar um novo painel.
Adicione visualizações já criadas ou crie novas diretamente.

Os dashboards podem unir várias visualizações do seu índice alunos.


![Kibana](/content/elastic04.png)

![Kibana](/content/elastic05.png)

### Criando uma Visualização
Dentro do Dashboard ou diretamente em Visualize Library, clique em:

"Create visualization"

Escolha o tipo de gráfico desejado, por exemplo:

Pie (Pizza Chart)

Selecione o Data View alunos e configure:

![Kibana](/content/elastic06.png)


![Kibana](/content/elastic07.png)

![Kibana](/content/elastic08.png)

### Usando o Dev Tools
Acesse:

Management → Dev Tools

Aqui podemos executar comandos direto na API REST do Elasticsearch.

![Kibana](/content/elastic09.png)

## Cluster


> https://www.elastic.co/docs/api/doc/elasticsearch/

```bash
curl -XGET "http://localhost:9200/_cluster/health?pretty"

http://localhost:9200/_cluster/state?pretty

http://localhost:9200/_cluster/stats?human&pretty

http://localhost:9200/_cluster/settings


http://localhost:9200/_nodes

```