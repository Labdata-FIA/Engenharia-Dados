# Revisão — Pronto-Socorro em Tempo Real (Kafka Connect para iniciantes)

---
## Disclaimer
> **As configurações dos Laboratórios é puramente para fins de desenvolvimento local e estudos**
>
> **Todos os dados de pacientes deste lab são fictícios.**

## Pré-requisitos
* Docker Desktop instalado e **aberto**
* Nenhum conhecimento de SQL ou de Kafka é necessário: tudo é explicado aqui

---

## Antes de começar: entrar na pasta da aula

Abra o terminal (PowerShell no Windows, Terminal no Mac/Linux), vá até a pasta onde você clonou o repositório do curso e entre na pasta desta aula, um comando por vez:

```sh
cd "engenharia-dados"
cd "02. Aula complementar"
cd "2. Revisao-Kafka+SQL"
```

> As aspas são necessárias porque os nomes das pastas têm espaços.

Confira se você está no lugar certo:

```sh
ls
```

Devem aparecer o `docker-compose.yaml` e as pastas `sql` e `conectores`. Os comandos `docker compose` desta aula precisam ser rodados **dentro desta pasta**.

---

## Parte 0 — Subir o ambiente (faça primeiro)

Na primeira vez, o Docker baixa várias imagens, e isso leva alguns minutos. Por isso subimos tudo **antes** de começar a explicação.

Abra um terminal **na pasta desta aula** e rode:

```sh
docker compose up -d zookeeper kafka-broker connect postgres pgadmin minio
```

**O que esse comando faz:** lê o arquivo `docker-compose.yaml`, baixa os programas necessários e liga cada um deles num "container" (uma caixinha isolada), em segundo plano (`-d`).

Enquanto baixa, siga para a Parte 1. Quando terminar, confira:

```sh
docker container ls
```

**O que esse comando faz:** lista os containers que estão ligados. Devem aparecer `postgres`, `pgadmin_container`, `zookeeper`, `kafka-broker`, `kafkaConect` e `minio`.
---

## Parte 1 — Entendendo o problema

### 1.1 A história

O **pronto-socorro** de um hospital registra tudo num banco de dados: quem são os pacientes, quem são os médicos e cada atendimento.

A coordenação quer duas coisas:

1. **Saber de cada atendimento novo na hora em que ele acontece**, e não no dia seguinte.
2. **Guardar uma cópia de tudo num "arquivo central"** (o Data Lake), para análises futuras.


### 1.2 As peças, com analogias

| Peça | O que é | Analogia |
|---|---|---|
| **PostgreSQL** | O banco de dados do hospital, onde ficam as tabelas | O **arquivo de fichas** da recepção |
| **pgAdmin** | Uma tela no navegador para mexer no PostgreSQL | A **mesa da recepcionista**, de onde ela consulta e preenche as fichas |
| **WAL** | O "diário" do PostgreSQL: toda mudança é anotada nele antes de ir para a tabela | O **livro de ocorrências**: tudo o que acontece é anotado, em ordem |
| **Kafka** | Uma "esteira" que transporta mensagens, na ordem em que chegam | A **esteira de uma fábrica**: as caixas entram de um lado e saem do outro, em ordem |
| **Tópico** | Uma das "esteiras" do Kafka, com um nome | Uma **esteira com etiqueta**: "atendimentos", "pacientes"... |
| **Kafka Connect** | Um programa que liga outros sistemas ao Kafka, só com configuração | Uma **tomada universal**: você não fabrica o aparelho, só escolhe o adaptador |
| **Debezium** | O "adaptador" que lê o diário (WAL) do PostgreSQL e manda cada mudança para o Kafka | Um **funcionário que lê o livro de ocorrências** e coloca cada anotação na esteira |
| **S3 Sink** | O "adaptador" que tira as mensagens do Kafka e grava arquivos no MinIO | Um **funcionário no fim da esteira**, que guarda as caixas no depósito |
| **MinIO** | Um armazenamento de arquivos, igual ao S3 da Amazon. É o nosso **Data Lake** | O **depósito central** do hospital |
| **Docker** | Liga cada programa numa caixinha isolada, sem instalar nada no seu computador | Um **prédio com salas prontas**: cada programa ocupa uma sala |

### 1.3 O caminho de um atendimento

```
  Recepção (pgAdmin)
        │  1. alguém cadastra um atendimento (INSERT)
        ▼
  PostgreSQL ── 2. anota a mudança no diário (WAL)
        │
        │  3. o Debezium lê o diário
        ▼
  Kafka Connect (Debezium) ── 4. transforma a mudança numa mensagem
        │
        ▼
  Kafka (tópico) ── 5. a mensagem fica na esteira
        │
        │  6. o S3 Sink pega as mensagens da esteira
        ▼
  Kafka Connect (S3 Sink) ── 7. junta 3 mensagens e grava um arquivo
        │
        ▼
  MinIO (bucket bronze) ── 8. o arquivo fica guardado no Data Lake
```

Tudo isso acontece **em poucos segundos**, sozinho, depois de configurado.

### 1.4 Como cada peça se conecta à outra

Esta é a parte mais importante: **quem fala com quem, como e por quê.**

Todos os containers estão na mesma **rede interna do Docker** (chamada `rede_fia`). Dentro dessa rede, um programa encontra o outro **pelo nome**, como num ramal interno de empresa: o Connect "liga" para `postgres`, para `kafka-broker` e para `minio`.

| Conexão | Como é feita | Por quê |
|---|---|---|
| **Você → pgAdmin** | Pelo navegador, em `http://localhost:5433` | Para você ver e mexer no banco sem decorar comandos |
| **pgAdmin → PostgreSQL** | Pelo nome `postgres`, porta `5432`, usuário `postgres` e senha `postgres` | O pgAdmin está dentro da rede do Docker, por isso usa o nome, e não `localhost` |
| **Debezium → PostgreSQL** | Pelo nome `postgres`, porta `5432`, numa **conexão de replicação**: em vez de consultar as tabelas, ele pede ao banco "me envie cada nova anotação do diário (WAL)" | Ler o diário não pesa no banco e mostra **todas** as mudanças, até as apagadas |
| **Debezium → Kafka** | O Connect envia as mensagens para `kafka-broker:29092` | É o endereço do Kafka dentro da rede do Docker |
| **Você → Kafka Connect** | Com o comando `curl`, na porta `8083` (a "API REST"), enviando arquivos JSON | O Connect não tem tela: você dá ordens a ele por mensagens HTTP |
| **S3 Sink → Kafka** | Lê os tópicos de `kafka-broker:29092`, como um consumidor | Para pegar as mensagens da esteira |
| **S3 Sink → MinIO** | Grava em `http://minio:9000`, com usuário `admin` e senha `minioadmin` | O MinIO fala a mesma "língua" do S3 da Amazon, então o mesmo adaptador serve para os dois |
| **Você → MinIO** | Pelo navegador, em `http://localhost:9001` | Para ver os arquivos que chegaram |

> 💡 **`localhost` ou nome do serviço?** Do **seu computador** (navegador, terminal), use `localhost` + a porta. **De dentro** de um container para outro, use o **nome** do serviço (`postgres`, `kafka-broker`, `minio`).

### 1.5 Quando usar isso (e quando não)

O que estamos montando tem nome: **CDC** (*Change Data Capture*, ou "captura de mudanças"). O Debezium é uma ferramenta de CDC.

| Use CDC + Kafka Connect quando... | Não precisa quando... |
|---|---|
| Outro sistema precisa saber das mudanças **em segundos** | Um relatório por dia já basta: um `SELECT` agendado de madrugada resolve |
| Você precisa saber também o que foi **alterado** e **apagado** | Os dados só são inseridos, nunca alterados |
| Você não pode (ou não quer) mexer no sistema que grava no banco | Você mesmo controla a aplicação e pode enviar os eventos direto |
| Vários sistemas querem as mesmas mudanças (Data Lake, alertas, painéis) | Só um sistema precisa do dado, uma vez |

> 💡 **Por que não fazer um `SELECT` a cada 5 minutos?** Porque ele não vê o que foi **apagado**, perde mudanças que aconteceram entre uma leitura e outra, e pesa no banco. O CDC lê o diário: vê **tudo**, **em ordem**, sem atrapalhar o banco.

---

## Parte 2 — SQL para quem nunca usou

### 2.1 O que é um banco de dados

Um banco de dados guarda informações em **tabelas**, parecidas com planilhas do Excel:

**Tabela `pacientes`:**

| id | nome | cpf | data_nascimento | convenio |
|---|---|---|---|---|
| 1 | Maria Silva | 111.111.111-11 | 1958-03-12 | SUS |
| 2 | Joao Santos | 222.222.222-22 | 1990-07-25 | Unimed |

| Termo | O que é | No exemplo |
|---|---|---|
| **Tabela** | Um conjunto de informações do mesmo tipo | `pacientes` |
| **Coluna** | Um tipo de informação | `nome`, `cpf`, `convenio` |
| **Linha** (ou registro) | Um item da tabela | A Maria Silva é uma linha |
| **Chave primária** (*primary key*) | Uma coluna que **identifica cada linha sem repetir** | `id`: não existem dois pacientes com o mesmo `id` |
| **Chave estrangeira** (*foreign key*) | Uma coluna que **aponta para uma linha de outra tabela** | Em `atendimentos`, a coluna `paciente_id` aponta para o `id` de `pacientes` |
| **Schema** | Uma "pasta" que agrupa tabelas | `prontosocorro` |

**SQL** é a linguagem para conversar com o banco. Os comandos são quase frases em inglês.

### 2.2 Abrindo o pgAdmin

1. Acesse http://localhost:5433
2. Entre com o e-mail `lab-pgadmin4@pgadmin.org` e a senha `postgres`
3. Clique em **Add New Server** e preencha:

| Campo | Valor | Por quê |
|---|---|---|
| Name (aba General) | `postgres` | Só um apelido para o servidor |
| Host name/address (aba Connection) | `postgres` | O **nome** do container do banco na rede do Docker |
| Port | `5432` | A porta padrão do PostgreSQL |
| Username | `postgres` | O usuário do banco |
| Password | `postgres` | A senha do banco |

4. No menu da esquerda, abra **Servers → postgres → Databases → postgres**
5. Clique com o botão direito em **postgres** → **Query Tool**. É nessa janela que se escreve o SQL. Para executar, aperte **F5** ou o botão ▶

### 2.3 Criando o banco do pronto-socorro

Abra o arquivo **`sql/hospital.sql`** desta pasta, copie **todo** o conteúdo, cole no Query Tool e aperte **F5**.

> ⚠️ **Faça este passo antes de tudo.** O banco começa vazio: enquanto o `hospital.sql` não for executado, o schema `prontosocorro` não existe e qualquer `SELECT` dá o erro `relation "prontosocorro.pacientes" does not exist`.

O script completo é este (é o mesmo conteúdo do arquivo). Copie **do começo ao fim**:

```sql
-- Banco do pronto-socorro (dados fictícios)
CREATE SCHEMA IF NOT EXISTS prontosocorro;

-- Cadastro de pacientes
CREATE TABLE prontosocorro.pacientes (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    cpf             VARCHAR(14)  NOT NULL,
    data_nascimento DATE         NOT NULL,
    convenio        VARCHAR(50)  NOT NULL
);

-- Cadastro de médicos
CREATE TABLE prontosocorro.medicos (
    id            SERIAL PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL,
    crm           VARCHAR(20)  NOT NULL,
    especialidade VARCHAR(50)  NOT NULL
);

-- Atendimentos do pronto-socorro (classificação de risco: Protocolo de Manchester)
CREATE TABLE prontosocorro.atendimentos (
    id                  SERIAL PRIMARY KEY,
    paciente_id         INT          NOT NULL REFERENCES prontosocorro.pacientes(id),
    medico_id           INT          NOT NULL REFERENCES prontosocorro.medicos(id),
    classificacao_risco VARCHAR(10)  NOT NULL
        CHECK (classificacao_risco IN ('VERMELHO','LARANJA','AMARELO','VERDE','AZUL')),
    queixa              VARCHAR(200),
    status              VARCHAR(20)  NOT NULL DEFAULT 'AGUARDANDO'
        CHECK (status IN ('AGUARDANDO','EM_ATENDIMENTO','ALTA')),
    aberto_em           TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Grava a linha "antiga" completa no WAL: o campo "before" do Debezium vem preenchido no UPDATE
ALTER TABLE prontosocorro.pacientes    REPLICA IDENTITY FULL;
ALTER TABLE prontosocorro.medicos      REPLICA IDENTITY FULL;
ALTER TABLE prontosocorro.atendimentos REPLICA IDENTITY FULL;

-- Dados iniciais
INSERT INTO prontosocorro.pacientes (nome, cpf, data_nascimento, convenio) VALUES
  ('Maria Silva',    '111.111.111-11', '1958-03-12', 'SUS'),
  ('Joao Santos',    '222.222.222-22', '1990-07-25', 'Unimed'),
  ('Ana Oliveira',   '333.333.333-33', '1975-11-02', 'Bradesco Saude'),
  ('Carlos Souza',   '444.444.444-44', '1983-01-30', 'SulAmerica'),
  ('Beatriz Lima',   '555.555.555-55', '2018-05-18', 'SUS');

INSERT INTO prontosocorro.medicos (nome, crm, especialidade) VALUES
  ('Dra. Fernanda Costa', 'CRM-SP 100001', 'Clinica Geral'),
  ('Dr. Ricardo Alves',   'CRM-SP 100002', 'Cardiologia'),
  ('Dra. Juliana Rocha',  'CRM-SP 100003', 'Pediatria'),
  ('Dr. Paulo Mendes',    'CRM-SP 100004', 'Ortopedia');

INSERT INTO prontosocorro.atendimentos (paciente_id, medico_id, classificacao_risco, queixa, status) VALUES
  (1, 2, 'LARANJA',  'Dor no peito',             'EM_ATENDIMENTO'),
  (2, 4, 'VERDE',    'Torcao no tornozelo',      'AGUARDANDO'),
  (3, 1, 'AMARELO',  'Febre e tosse ha 3 dias',  'AGUARDANDO');
```

> 💡 **No pgAdmin, se houver algum texto selecionado, o F5 executa só a seleção.** Clique dentro do editor, aperte **Ctrl+A** (Mac: **Cmd+A**) para selecionar tudo e só então aperte **F5**.
>
> Se aparecer `schema "prontosocorro" does not exist`, é porque o `CREATE TABLE` rodou sem a primeira linha do script (`CREATE SCHEMA IF NOT EXISTS prontosocorro;`). O *schema* é a "pasta" das tabelas, então precisa existir antes delas.

O script cria três tabelas. Veja a principal, `atendimentos`, explicada linha por linha (**este trecho é só para leitura, não precisa rodar de novo**):

```sql
CREATE TABLE prontosocorro.atendimentos (
    id                  SERIAL PRIMARY KEY,
    paciente_id         INT          NOT NULL REFERENCES prontosocorro.pacientes(id),
    medico_id           INT          NOT NULL REFERENCES prontosocorro.medicos(id),
    classificacao_risco VARCHAR(10)  NOT NULL
        CHECK (classificacao_risco IN ('VERMELHO','LARANJA','AMARELO','VERDE','AZUL')),
    queixa              VARCHAR(200),
    status              VARCHAR(20)  NOT NULL DEFAULT 'AGUARDANDO'
        CHECK (status IN ('AGUARDANDO','EM_ATENDIMENTO','ALTA')),
    aberto_em           TIMESTAMPTZ  NOT NULL DEFAULT now()
);
```

| Trecho | O que significa |
|---|---|
| `id SERIAL PRIMARY KEY` | Número que o banco gera sozinho (1, 2, 3...) e que identifica cada atendimento |
| `INT` | Número inteiro |
| `VARCHAR(10)` | Texto de até 10 letras |
| `TIMESTAMPTZ` | Data e hora, com fuso horário |
| `DATE` | Só a data (em `pacientes`, na data de nascimento) |
| `NOT NULL` | O campo é **obrigatório** |
| `REFERENCES prontosocorro.pacientes(id)` | **Chave estrangeira**: só aceita um `paciente_id` que exista na tabela de pacientes |
| `CHECK (... IN (...))` | Só aceita os valores da lista. Aqui, as 5 cores do Protocolo de Manchester |
| `DEFAULT 'AGUARDANDO'` | Se ninguém informar o status, ele começa como `AGUARDANDO` |
| `DEFAULT now()` | Se ninguém informar a hora, usa a hora atual |

**A classificação de risco (Protocolo de Manchester):**

| Cor | Prioridade |
|---|---|
| 🔴 `VERMELHO` | Emergência: atendimento imediato |
| 🟠 `LARANJA` | Muito urgente |
| 🟡 `AMARELO` | Urgente |
| 🟢 `VERDE` | Pouco urgente |
| 🔵 `AZUL` | Não urgente |

O script também tem esta linha para cada tabela:

```sql
ALTER TABLE prontosocorro.atendimentos REPLICA IDENTITY FULL;
```

**O que faz:** manda o banco anotar no diário (WAL) a linha **inteira de antes** de cada alteração. Sem isso, num `UPDATE` o diário guardaria só como a linha **ficou**, e não como ela **era**.

No fim, o script insere 5 pacientes, 4 médicos e 3 atendimentos.

### 2.4 Os 5 comandos, na prática

Agora que as tabelas existem, **rode cada exemplo abaixo no Query Tool** (cole, selecione e aperte **F5**) e veja o resultado.

| Comando | Para que serve | Em português |
|---|---|---|
| `CREATE TABLE` | Criar uma tabela | "Crie uma tabela com estas colunas" |
| `INSERT` | Adicionar linhas | "Insira esta linha" |
| `SELECT` | Consultar linhas | "Mostre estas colunas" |
| `UPDATE` | Alterar linhas | "Altere este valor" |
| `DELETE` | Apagar linhas | "Apague estas linhas" |

**`SELECT`: consultar**

```sql
SELECT nome, convenio FROM prontosocorro.pacientes WHERE convenio = 'SUS';
```

Lendo: *"Mostre o nome e o convênio da tabela pacientes, mas só onde o convênio for SUS."*

**Resultado esperado:** 2 linhas, `Maria Silva` e `Beatriz Lima`. Tire o `WHERE convenio = 'SUS'` e rode de novo: aparecem os 5 pacientes.

| Parte | Significado |
|---|---|
| `SELECT nome, convenio` | Quais colunas mostrar. Use `*` para mostrar **todas** |
| `FROM prontosocorro.pacientes` | De qual tabela (`schema.tabela`) |
| `WHERE convenio = 'SUS'` | O **filtro**: só as linhas que atendem à condição. É opcional |
| `;` | Fim do comando |

**`INSERT`: adicionar**

```sql
INSERT INTO prontosocorro.pacientes (nome, cpf, data_nascimento, convenio)
VALUES ('Pedro Teste', '666.666.666-66', '2000-01-01', 'SUS');
```

Lendo: *"Insira na tabela pacientes, nas colunas nome, cpf, data de nascimento e convênio, os valores Pedro Teste, 666..., 2000-01-01 e SUS."*

* A lista de colunas e a lista de valores vão **na mesma ordem**.
* Textos e datas vão entre **aspas simples** (`'...'`). Números, sem aspas.
* O `id` não foi informado: o banco gera o próximo número sozinho.

**Confira:** rode `SELECT * FROM prontosocorro.pacientes;` e veja o Pedro com `id` 6.

**`UPDATE`: alterar**

```sql
UPDATE prontosocorro.pacientes SET convenio = 'Amil' WHERE nome = 'Pedro Teste';
```

Lendo: *"Na tabela pacientes, mude o convênio para Amil onde o nome for Pedro Teste."*

**Confira:** rode o `SELECT` de novo. O convênio do Pedro agora é `Amil`.

> ⚠️ **Nunca esqueça o `WHERE` num `UPDATE` ou `DELETE`.** Sem ele, o comando vale para **todas as linhas da tabela**.

**`DELETE`: apagar**

```sql
DELETE FROM prontosocorro.pacientes WHERE nome = 'Pedro Teste';
```

Lendo: *"Apague da tabela pacientes as linhas onde o nome for Pedro Teste."*

**Confira:** rode o `SELECT` de novo. O Pedro sumiu e voltam os 5 pacientes originais.


### 2.5 Conferindo

Rode no Query Tool, um de cada vez:

```sql
SELECT * FROM prontosocorro.atendimentos;
```

**O que mostra:** os 3 atendimentos. Repare que só aparecem **números** de paciente e de médico (`paciente_id`, `medico_id`): são as chaves estrangeiras.

```sql
SHOW wal_level;
```

**O que mostra:** precisa ser `logical`. Isso quer dizer que o diário do banco guarda informação suficiente para o Debezium entender cada mudança. O banco deste laboratório já vem configurado assim.

---

## Parte 3 — Capturando as mudanças do banco (CDC)

### 3.1 Conferindo o Kafka Connect

O Kafka Connect não tem tela. Para dar ordens a ele, entramos no container dele e usamos o comando `curl`, que envia mensagens pela internet (aqui, pela rede interna).

Abra um terminal e entre no container do Connect:

```sh
docker exec -it kafkaConect bash
```

**O que faz:** abre um terminal **dentro** do container do Kafka Connect. Os próximos comandos rodam lá dentro. Vamos chamar esta janela de **Terminal do Connect**.

Pergunte ao Connect quais "adaptadores" ele tem instalados:

```sh
curl -s http://localhost:8083/connector-plugins
```

**O que faz:** o `curl` pede ao Connect (porta `8083`) a lista de plugins. Dentro do container, `localhost` é o próprio Connect.

Na resposta, procure estes dois nomes:

```
io.debezium.connector.postgresql.PostgresConnector   (source)
io.confluent.connect.s3.S3SinkConnector              (sink)
```

| Plugin | Tipo | O que faz |
|---|---|---|
| `PostgresConnector` (Debezium) | **Source** (origem) | **Traz** dados de fora **para dentro** do Kafka |
| `S3SinkConnector` | **Sink** (destino) | **Leva** dados de dentro do Kafka **para fora** |

> Se aparecer `Connection refused`, o Connect ainda está ligando. Espere um minuto e tente de novo.

### 3.2 O arquivo de configuração do conector

Um **conector** é um plugin + a configuração dele. A configuração é um arquivo **JSON**: uma lista de `"nome": "valor"`.

Veja o arquivo **`conectores/connector-hospital-cdc.json`**:

```json
{
  "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
  "tasks.max": "1",
  "database.hostname": "postgres",
  "database.port": "5432",
  "database.user": "postgres",
  "database.password": "postgres",
  "database.dbname": "postgres",
  "topic.prefix": "cdc",
  "slot.name": "debezium_cdc",
  "schema.include.list": "prontosocorro"
}
```

Lendo em voz alta: *"Use o adaptador Debezium para PostgreSQL. Conecte no banco `postgres`, na porta 5432, com usuário e senha `postgres`. Fique de olho no schema `prontosocorro`. Marque até onde você leu num marcador chamado `debezium_cdc`. Coloque as mensagens em esteiras com nomes começando por `cdc`."*

| Linha | O que faz |
|---|---|
| `connector.class` | Qual adaptador usar: o Debezium para PostgreSQL |
| `tasks.max` | Quantos "funcionários" trabalham nesse conector. Para ler o diário em ordem, é sempre 1 |
| `database.hostname` / `database.port` | **Onde está o banco**: o nome do container e a porta |
| `database.user` / `database.password` | **Com que usuário entrar** no banco |
| `database.dbname` | **Qual banco** acompanhar |
| `schema.include.list` | **Quais tabelas**: todas do schema `prontosocorro` |
| `slot.name` | O **marcador de página** no diário. O banco guarda o diário até o Debezium ler, e o Debezium nunca perde o lugar |
| `topic.prefix` | O começo do nome das esteiras. Cada tabela vira um tópico: `cdc.prontosocorro.atendimentos` |

**É aqui que a conexão com o banco acontece.** Quando você cria o conector, o Debezium usa essas informações para abrir uma conexão de replicação com o PostgreSQL e começar a ler o diário.

### 3.3 Criando o conector

No **Terminal do Connect**:

```sh
curl -s -X PUT -H 'Content-Type: application/json' -d @/conectores/connector-hospital-cdc.json http://localhost:8083/connectors/connector-hospital-cdc/config
```

| Parte do comando | O que faz |
|---|---|
| `curl -s` | Envia uma mensagem para o Connect, sem barra de progresso |
| `-X PUT` | O tipo da mensagem: "crie ou atualize" |
| `-H 'Content-Type: application/json'` | Avisa que estamos enviando um JSON |
| `-d @/conectores/connector-hospital-cdc.json` | O conteúdo vem deste arquivo (o `@` quer dizer "leia do arquivo"). A pasta `conectores` do seu computador aparece dentro do container em `/conectores` |
| `http://localhost:8083/connectors/connector-hospital-cdc/config` | O endereço: "a configuração do conector chamado `connector-hospital-cdc`" |

**O que acontece agora, sozinho:**

1. O Debezium se conecta ao PostgreSQL
2. Cria o marcador `debezium_cdc` no diário
3. **Copia tudo o que já existe** nas tabelas e manda para o Kafka. Isso se chama **snapshot**, uma "foto inicial"
4. Fica esperando novas anotações no diário

Confira se está funcionando:

```sh
curl -s http://localhost:8083/connectors/connector-hospital-cdc/status
```

**O que faz:** pergunta o estado do conector. O esperado é `"state":"RUNNING"` (rodando) duas vezes: no conector e na task. Se aparecer `FAILED`, o texto do campo `trace` diz o erro.

### 3.4 Vendo as esteiras (tópicos)

Abra **outro terminal** e entre no container do Kafka:

```sh
docker exec -it kafka-broker bash
```

Vamos chamar esta janela de **Terminal do Kafka**. Liste as esteiras:

```sh
kafka-topics --bootstrap-server localhost:9092 --list
```

| Parte | O que faz |
|---|---|
| `kafka-topics` | Programa do Kafka para mexer com tópicos |
| `--bootstrap-server localhost:9092` | Onde está o Kafka. Dentro do container do Kafka, é `localhost` |
| `--list` | Lista os tópicos |

Você deve ver uma esteira **para cada tabela**, mais três do próprio Connect:

| Tópico | Quem criou | O que tem |
|---|---|---|
| `cdc.prontosocorro.atendimentos` | Debezium | As mudanças da tabela de atendimentos |
| `cdc.prontosocorro.medicos` | Debezium | As mudanças da tabela de médicos |
| `cdc.prontosocorro.pacientes` | Debezium | As mudanças da tabela de pacientes |
| `connect-configs` | Connect | A configuração dos conectores |
| `connect-offsets` | Connect | Até onde cada conector já leu |
| `connect-status` | Connect | Se cada conector está rodando ou não |

Leia uma mensagem da esteira de pacientes:

```sh
kafka-console-consumer --bootstrap-server localhost:9092 --topic cdc.prontosocorro.pacientes --from-beginning --property print.key=true --max-messages 1
```

| Parte | O que faz |
|---|---|
| `kafka-console-consumer` | Mostra na tela as mensagens de um tópico |
| `--topic cdc.prontosocorro.pacientes` | Qual esteira ler |
| `--from-beginning` | Desde a primeira mensagem |
| `--property print.key=true` | Mostra também a **chave** da mensagem |
| `--max-messages 1` | Mostra só 1 mensagem e para |

### 3.5 Entendendo a mensagem

```
{"id":1}    {"before":null,"after":{"id":1,"nome":"Maria Silva",...,"convenio":"SUS"},"source":{...},"op":"r","ts_ms":...}
 └ chave     └ valor: o "envelope" do Debezium
```

* A **chave** é o `id` da linha (a chave primária da tabela).
* O **valor** é um "envelope" com várias partes:

| Parte | O que guarda |
|---|---|
| `before` | Como a linha era **antes** da mudança |
| `after` | Como a linha ficou **depois** da mudança |
| `op` | **Qual foi a mudança** |
| `source` | De onde veio: banco, tabela, momento |
| `ts_ms` | Quando o Debezium leu a mudança |

| `op` | Significa | `before` | `after` |
|---|---|---|---|
| `r` | *read*: estava na "foto inicial" (snapshot) | vazio (`null`) | a linha |
| `c` | *create*: um `INSERT` | vazio | a linha nova |
| `u` | *update*: um `UPDATE` | a linha antiga | a linha nova |
| `d` | *delete*: um `DELETE` | a linha apagada | vazio |

> 📌 A data de nascimento chegou como `-4313`? O Debezium manda datas como **número de dias desde 01/01/1970**. Negativo quer dizer antes de 1970.

### 3.6 Vendo acontecer ao vivo

No **Terminal do Kafka**, deixe um leitor **aberto**, esperando novas mensagens:

```sh
kafka-console-consumer --bootstrap-server localhost:9092 --topic cdc.prontosocorro.pacientes --property print.key=true
```

Sem o `--from-beginning`, ele mostra **só o que chegar daqui para frente**.

Agora, no **pgAdmin**, rode um comando por vez e olhe o terminal depois de cada um:

```sql
INSERT INTO prontosocorro.pacientes (nome, cpf, data_nascimento, convenio)
VALUES ('Pedro Teste', '666.666.666-66', '2000-01-01', 'SUS');
```

Chega uma mensagem com `"op":"c"`: o `before` está vazio e o `after` tem o Pedro.

```sql
UPDATE prontosocorro.pacientes SET convenio = 'Amil' WHERE nome = 'Pedro Teste';
```

Chega uma mensagem com `"op":"u"`: o `before` mostra o convênio `SUS` e o `after` mostra `Amil`.

**Você acabou de ver o CDC funcionando:** o comando no banco virou uma mensagem no Kafka em segundos, sem nenhum programa feito por nós.

> 🔒 **Atenção (LGPD):** o **CPF** está passando pelo Kafka em texto aberto. Dado de saúde é **dado pessoal sensível**. Veja o desafio no final.

Pare o leitor com `Ctrl + C`.

---

## Parte 4 — Limpando as mensagens (SMT)

### 4.1 O incômodo

A mensagem "crua" funciona, mas dá trabalho para quem vai usar:

* os dados estão "embrulhados" dentro de `after`
* a chave é `{"id":1}`, e não só `1`

**SMT** (*Single Message Transform*) é um **ajuste automático em cada mensagem**, feito pelo próprio Connect, antes de ela entrar na esteira. É configuração, não programação.

**Analogia:** é como colocar uma **máquina de desembrulhar** no começo da esteira. As caixas entram embrulhadas e seguem já abertas.

### 4.2 O conector com SMT

Veja o arquivo **`conectores/connector-hospital.json`**. Ele é igual ao anterior, com estas diferenças:

```json
  "topic.prefix": "hospital",
  "slot.name": "debezium_hospital",
  "transforms": "unwrap,extractKey",
  "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
  "transforms.unwrap.add.fields": "op,source.ts_ms",
  "transforms.unwrap.delete.tombstone.handling.mode": "tombstone",
  "transforms.extractKey.type": "org.apache.kafka.connect.transforms.ExtractField$Key",
  "transforms.extractKey.field": "id"
```

| Linha | O que faz |
|---|---|
| `topic.prefix: hospital` | Esteiras novas (`hospital.prontosocorro.*`), para comparar com as `cdc.*` |
| `slot.name: debezium_hospital` | **Outro marcador de página.** Cada conector precisa do seu, senão dá erro |
| `transforms: unwrap,extractKey` | A lista de ajustes, feitos **nessa ordem**. Os nomes são apelidos que nós escolhemos |
| `unwrap` (`ExtractNewRecordState`) | **Desembrulha:** tira o envelope e deixa só a linha como ficou |
| `add.fields: op,source.ts_ms` | Mesmo desembrulhado, guarda o tipo da mudança no campo `__op` |
| `delete.tombstone.handling.mode: tombstone` | Um `DELETE` vira uma mensagem vazia, que quer dizer "apague essa chave" |
| `extractKey` (`ExtractField$Key`) | Troca a chave `{"id":1}` por só `1` |

### 4.3 Criando e comparando

No **Terminal do Connect**:

```sh
curl -s -X PUT -H 'Content-Type: application/json' -d @/conectores/connector-hospital.json http://localhost:8083/connectors/connector-hospital/config

curl -s http://localhost:8083/connectors
```

O primeiro comando cria o segundo conector. O segundo lista os conectores: agora são dois.

No **Terminal do Kafka**, compare o **mesmo atendimento** nas duas versões:

```sh
kafka-console-consumer --bootstrap-server localhost:9092 --topic cdc.prontosocorro.atendimentos --from-beginning --property print.key=true --max-messages 1

kafka-console-consumer --bootstrap-server localhost:9092 --topic hospital.prontosocorro.atendimentos --from-beginning --property print.key=true --max-messages 1
```

**Antes (cru):**

```
{"id":1}    {"before":null,"after":{"id":1,"paciente_id":1,...},"source":{...},"op":"r",...}
```

**Depois (com SMT):**

```
1    {"id":1,"paciente_id":1,"medico_id":2,"classificacao_risco":"LARANJA","queixa":"Dor no peito","status":"EM_ATENDIMENTO","aberto_em":"2026-...Z","__op":"r",...}
```

Mesmo dado, mesmo banco, mesmo adaptador. **Só mudou a configuração.**

### 4.4 Pausar não perde nada

No **Terminal do Connect**, pause o conector:

```sh
curl -s -X PUT http://localhost:8083/connectors/connector-hospital/pause
```

No **pgAdmin**, registre um atendimento:

```sql
INSERT INTO prontosocorro.atendimentos (paciente_id, medico_id, classificacao_risco, queixa)
VALUES (5, 3, 'AMARELO', 'Febre alta e vomito');
```

Leia a esteira `hospital.prontosocorro.atendimentos` no **Terminal do Kafka** (com `--from-beginning`): o atendimento novo **não chegou**.

Agora retome:

```sh
curl -s -X PUT http://localhost:8083/connectors/connector-hospital/resume
```

Leia de novo: **chegou**. O marcador de página guardou onde o Debezium parou, e ele continuou dali.

---

## Parte 5 — Gravando no Data Lake (Sink)

### 5.1 O que é o Sink

Até aqui, os dados estão **na esteira** (Kafka). O **Sink** é o funcionário no fim da esteira: pega as mensagens e grava arquivos no **MinIO**, o nosso Data Lake.

| Pergunta | Resposta |
|---|---|
| **Por que gravar num Data Lake?** | O Kafka guarda mensagens por um tempo; o Data Lake guarda **para sempre**, barato, para análises |
| **Por que não ler direto do banco?** | Para não pesar no banco do hospital: os analistas consultam o Data Lake |
| **O que é "bronze"?** | O nome do bucket (a "pasta principal") onde fica o dado como chegou. Depois viriam as camadas "silver" (tratada) e "gold" (pronta para relatórios) |

### 5.2 O arquivo do Sink

Veja o arquivo **`conectores/connector-minio-bronze.json`**:

```json
{
  "connector.class": "io.confluent.connect.s3.S3SinkConnector",
  "tasks.max": "1",
  "topics": "hospital.prontosocorro.atendimentos",
  "s3.bucket.name": "bronze",
  "store.url": "http://minio:9000",
  "flush.size": 3,
  "storage.class": "io.confluent.connect.s3.storage.S3Storage",
  "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
  "s3.region": "us-east-1",
  "aws.access.key.id": "admin",
  "aws.secret.access.key": "minioadmin",
  "behavior.on.null.values": "ignore"
}
```

Lendo em voz alta: *"Use o adaptador S3. Pegue as mensagens da esteira de atendimentos já limpos. A cada 3 mensagens, grave um arquivo JSON no bucket `bronze` do MinIO, usando o usuário `admin`."*

| Linha | O que faz |
|---|---|
| `topics` | **De qual esteira** pegar as mensagens |
| `store.url` | **Onde está o MinIO**: pelo nome do container, na porta 9000 |
| `aws.access.key.id` / `aws.secret.access.key` | **Com que usuário entrar** no MinIO |
| `s3.bucket.name` | **Em qual bucket** gravar. O `bronze` foi criado pelo container `mc` |
| `flush.size` | Quantas mensagens juntar antes de gravar **um arquivo** |
| `format.class` | O formato do arquivo: JSON |
| `s3.region` | Exigido pelo padrão S3; o MinIO ignora |
| `behavior.on.null.values` | Ignora as mensagens vazias (dos `DELETE`), porque não há o que gravar |

**É aqui que a conexão com o MinIO acontece.** O Sink usa o endereço e o usuário do arquivo para gravar no MinIO.

### 5.3 Criando o Sink

No **Terminal do Connect**:

```sh
curl -s -X PUT -H 'Content-Type: application/json' -d @/conectores/connector-minio-bronze.json http://localhost:8083/connectors/connector-minio-bronze/config

curl -s http://localhost:8083/connectors/connector-minio-bronze/status
```

O primeiro comando cria o Sink. O segundo confere se está `RUNNING`.

### 5.4 Vendo os arquivos

Abra http://localhost:9001 e entre com usuário `admin` e senha `minioadmin`. Vá em **Object Browser** → **bronze** e navegue pelas pastas:

```
bronze/topics/hospital.prontosocorro.atendimentos/partition=0/hospital.prontosocorro.atendimentos+0+0000000000.json
              └ nome da esteira                    └ parte     └ esteira + parte + número da 1ª mensagem
```

Abra um arquivo: cada linha é um atendimento, já limpo.

> 🧪 Cada arquivo tem **3 mensagens** (`flush.size: 3`). Se chegar só 1 atendimento novo, o arquivo **não aparece** até chegarem mais 2.

### 5.5 Teste final: do pgAdmin ao Data Lake

Um paciente chega de ambulância e mais dois dão entrada. No **pgAdmin**, rode um comando por vez:

```sql
-- 1. A recepção cadastra o paciente
INSERT INTO prontosocorro.pacientes (nome, cpf, data_nascimento, convenio)
VALUES ('Roberto Dias', '777.777.777-77', '1949-09-09', 'SUS');
```

```sql
-- 2. A triagem classifica como VERMELHO e encaminha para a cardiologia (médico 2)
INSERT INTO prontosocorro.atendimentos (paciente_id, medico_id, classificacao_risco, queixa)
SELECT id, 2, 'VERMELHO', 'Falta de ar intensa'
FROM prontosocorro.pacientes WHERE cpf = '777.777.777-77';
```

> 💡 Este `INSERT` usa um `SELECT` para descobrir o `id` do Roberto pelo CPF, em vez de digitar o número. É um jeito comum de inserir dados que dependem de outra tabela.

```sql
-- 3. Mais dois atendimentos (para completar as 3 mensagens do flush.size)
INSERT INTO prontosocorro.atendimentos (paciente_id, medico_id, classificacao_risco, queixa) VALUES
  (4, 4, 'VERDE', 'Dor nas costas'),
  (1, 1, 'AZUL',  'Renovacao de receita');
```

Atualize o MinIO: um **arquivo novo** apareceu no `bronze`.

**O que aconteceu, em segundos:**

1. O PostgreSQL anotou os `INSERT`s no diário (WAL)
2. O Debezium leu o diário e, com a SMT, mandou as mensagens limpas para a esteira
3. O Sink pegou as 3 mensagens e gravou um arquivo no Data Lake

**Tudo isso sem escrever um programa.**

---

## Resumo: o que levar desta aula

1. **CDC** captura cada mudança do banco **lendo o diário (WAL)**, e não as tabelas: vê tudo, em ordem, sem pesar no banco.
2. **Kafka Connect** liga sistemas ao Kafka **só com configuração** (arquivos JSON enviados pela API, com `curl`).
3. **Source** traz dados **para** o Kafka (Debezium). **Sink** leva dados **do** Kafka para fora (S3 Sink → MinIO).
4. A mensagem do Debezium é um **envelope** (`before`, `after`, `op`). Uma **SMT** desembrulha a mensagem, também só com configuração.
5. Os containers se encontram **pelo nome** (`postgres`, `kafka-broker`, `minio`) dentro da rede do Docker. Do seu computador, use `localhost`.

| Conector | Tipo | Lê de | Escreve em |
|---|---|---|---|
| `connector-hospital-cdc` | Source | PostgreSQL (diário) | `cdc.prontosocorro.*` (com envelope) |
| `connector-hospital` | Source + SMT | PostgreSQL (diário) | `hospital.prontosocorro.*` (limpo) |
| `connector-minio-bronze` | Sink | `hospital.prontosocorro.atendimentos` | MinIO, bucket `bronze` |

> 📌 **O que ficou para a aula completa:** juntar atendimento + paciente + médico em tempo real com o **ksqlDB** (para o atendimento chegar com nomes, e não só números) e consultar o Data Lake com SQL usando o **DuckDB**.

---

## Desafio (para casa)

**Proteger o CPF:** no arquivo `connector-hospital.json`, troque a linha `"transforms"` e acrescente as duas últimas:

```json
"transforms": "unwrap,extractKey,removeCpf",
"transforms.removeCpf.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
"transforms.removeCpf.exclude": "cpf"
```

Rode de novo o `curl -X PUT` da Parte 4.3, cadastre um paciente novo e confira na esteira `hospital.prontosocorro.pacientes`: o CPF não aparece mais.

**Pergunta:** por que é melhor tirar o dado sensível **antes** de ele entrar no Kafka?

---

## Limpeza

No **Terminal do Connect**, apague os conectores:

```sh
curl -s -X DELETE http://localhost:8083/connectors/connector-minio-bronze
curl -s -X DELETE http://localhost:8083/connectors/connector-hospital
curl -s -X DELETE http://localhost:8083/connectors/connector-hospital-cdc
```

No **pgAdmin**, apague os marcadores de página:

```sql
SELECT slot_name, active FROM pg_replication_slots;

SELECT pg_drop_replication_slot('debezium_hospital');
SELECT pg_drop_replication_slot('debezium_cdc');
```

| Comando | O que faz |
|---|---|
| `SELECT ... FROM pg_replication_slots` | Lista os marcadores que existem no banco |
| `pg_drop_replication_slot('...')` | Apaga um marcador |

> ⚠️ **Apagar o conector não apaga o marcador.** Um marcador esquecido faz o banco **guardar o diário para sempre**, esperando alguém ler, até o disco encher. Na vida real, esse é um erro clássico.

Desligue o ambiente, na pasta da aula:

```sh
docker compose down -v
```

**O que faz:** desliga e remove os containers. O `-v` apaga também os arquivos do MinIO. Na próxima aula, será preciso rodar o `sql/hospital.sql` de novo.

---

## Problemas comuns

| O que aparece | O que quer dizer | Como resolver |
|---|---|---|
| `Connection refused` no `curl` | O Connect ainda está ligando | Espere 1 minuto e tente de novo |
| O conector aparece como `FAILED` | Algo deu errado; o motivo está no campo `trace` do `status` | Leia o `trace`. Os casos mais comuns estão abaixo |
| Erro de *replication slot* | Dois conectores com o mesmo `slot.name`, ou um marcador antigo | Confira o `slot.name` de cada arquivo. Apague marcadores antigos (veja a Limpeza) |
| Os tópicos `cdc.prontosocorro.*` não aparecem | O banco do pronto-socorro não foi criado | Rode o `sql/hospital.sql` no pgAdmin **antes** de criar os conectores |
| `relation ... already exists` ao rodar o SQL | O script já foi executado | Normal: o banco já está pronto |
| `violates check constraint` | Valor fora da lista, como uma cor que não existe | Use só as cores e os status da tabela |
| `violates foreign key constraint` | O `paciente_id` ou `medico_id` não existe | Use um `id` que exista (`SELECT * FROM prontosocorro.pacientes;`) |
| O Sink fica com a task `FAILED` e `Non-existent S3 bucket: bronze` | O bucket `bronze` não foi criado | Em http://localhost:9001 (`admin` / `minioadmin`): **Buckets → Create Bucket**, nome `bronze`. Depois reinicie a task: `curl -X POST http://localhost:8083/connectors/connector-minio-bronze/tasks/0/restart` |
| O arquivo não aparece no MinIO | Ainda não juntou 3 mensagens | Cadastre mais atendimentos |
| `container name ... already in use` | Outro laboratório está ligado | `docker compose down` na pasta do outro laboratório |
