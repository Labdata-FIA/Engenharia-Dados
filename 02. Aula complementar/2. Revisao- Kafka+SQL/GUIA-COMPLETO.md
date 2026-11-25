# Guia Completo: Docker Compose, Kafka e Kafka Connect

Este guia é para **consulta**. O `README.md` é o passo a passo da aula. Aqui você encontra a explicação de cada peça e uma "cola" de comandos para usar depois.

Use como um dicionário: não precisa ler de uma vez. Procure o assunto no índice.

## Índice

1. [O mapa geral](#1-o-mapa-geral)
2. [Docker em 5 minutos](#2-docker-em-5-minutos)
3. [O docker-compose.yaml, linha por linha](#3-o-docker-composeyaml-linha-por-linha)
4. [As imagens usadas](#4-as-imagens-usadas)
5. [Comandos do Docker e do Compose](#5-comandos-do-docker-e-do-compose)
6. [Kafka: conceitos](#6-kafka-conceitos)
7. [Kafka: comandos básicos](#7-kafka-comandos-básicos)
8. [Kafka Connect: conceitos](#8-kafka-connect-conceitos)
9. [Kafka Connect: comandos da API](#9-kafka-connect-comandos-da-api)
10. [Debezium e o PostgreSQL por dentro](#10-debezium-e-o-postgresql-por-dentro)
11. [O Sink do MinIO por dentro](#11-o-sink-do-minio-por-dentro)
12. [Diagnóstico: quando algo dá errado](#12-diagnóstico-quando-algo-dá-errado)
13. [Glossário](#13-glossário)

---

## 1. O mapa geral

```
                         rede_fia (rede interna do Docker)
 ┌───────────────────────────────────────────────────────────────────────────┐
 │                                                                           │
 │  pgadmin ──► postgres ──WAL──► connect (Debezium) ──► kafka-broker        │
 │  (tela)      (banco)           (lê o diário)          (esteiras)          │
 │                                                            │              │
 │                                connect (S3 Sink) ◄─────────┘              │
 │                                       │                                   │
 │                                       ▼                                   │
 │                                     minio ◄── mc (cria o bucket e desliga)│
 │                                  (data lake)                              │
 │                                                                           │
 │  zookeeper ◄── kafka-broker (o Kafka usa o ZooKeeper para se organizar)   │
 └───────────────────────────────────────────────────────────────────────────┘
       ▲ portas abertas para o seu computador:
       5433 pgAdmin · 5432 Postgres · 9092 Kafka · 8083 Connect · 9000/9001 MinIO
```

| Peça | Papel em uma frase | Analogia |
|---|---|---|
| **PostgreSQL** | Banco onde o sistema do hospital grava os atendimentos | O livro-caixa da loja |
| **pgAdmin** | Tela no navegador para mexer no banco | A caneta para escrever no livro |
| **Kafka** | Guarda mensagens em fila, na ordem, para quem quiser ler | Esteiras de uma fábrica |
| **ZooKeeper** | Organiza o Kafka (quem está vivo, quem manda) | O gerente de turno da fábrica |
| **Kafka Connect** | Liga outros sistemas ao Kafka só com configuração | Uma tomada universal |
| **Debezium** | Plugin do Connect que lê as mudanças do banco | Um estagiário lendo o livro-caixa e avisando cada lançamento |
| **S3 Sink** | Plugin do Connect que grava mensagens em arquivos | O arquivista que guarda as cópias |
| **MinIO** | Armazenamento de arquivos compatível com o Amazon S3 | O arquivo morto da empresa |
| **mc** | Programa de linha de comando do MinIO | O ajudante que monta as pastas antes do expediente |

---

## 2. Docker em 5 minutos

### 2.1 Imagem x container

| Conceito | O que é | Analogia |
|---|---|---|
| **Imagem** | Um pacote pronto, só leitura, com o programa e tudo que ele precisa | A **receita** (ou a planta da casa) |
| **Container** | Uma imagem **rodando**. Dá para ter vários containers da mesma imagem | O **bolo** feito com a receita (a casa construída) |
| **Registry** | O "site" de onde as imagens são baixadas | O supermercado das receitas |
| **Tag** | A versão da imagem, depois dos `:` | A edição do livro de receitas |

Exemplo: `confluentinc/cp-kafka:7.6.1`

| Parte | Significado |
|---|---|
| `confluentinc` | Quem publicou (a empresa Confluent) |
| `cp-kafka` | O nome da imagem |
| `7.6.1` | A tag (versão) |
| *(sem endereço na frente)* | Vem do **Docker Hub**, o registry padrão |

Quando a imagem tem um endereço na frente, ela vem de outro registry:

| Imagem | Registry |
|---|---|
| `quay.io/debezium/example-postgres` | Quay.io (da Red Hat) |
| `cgr.dev/chainguard/minio` | Chainguard |
| `dpage/pgadmin4` | Docker Hub |

> **Por que fixar a versão (tag)?** Sem tag, o Docker usa `latest`, que muda com o tempo. A aula que funcionou hoje pode quebrar daqui a um mês. Com a tag fixa, todos os alunos rodam exatamente a mesma coisa.

### 2.2 Porta (`ports`)

Cada container é como um apartamento isolado. A porta é a **campainha** que liga o seu computador a ele.

```
"5433:80"
  │    └── porta DENTRO do container (onde o programa escuta)
  └─────── porta no SEU computador (onde você acessa)
```

`5433:80` no pgAdmin: o pgAdmin escuta na porta 80 dentro do container, e você acessa por `http://localhost:5433`.

### 2.3 Volume (`volumes`)

Por padrão, tudo que um container grava **some** quando ele é apagado. O volume é um **HD externo** plugado no container.

| Tipo | Exemplo neste projeto | O que faz |
|---|---|---|
| **Volume nomeado** | `minio_storage:/data` | O Docker cria e cuida de um espaço chamado `minio_storage`. Os arquivos do MinIO sobrevivem a um `docker compose down` |
| **Bind mount** (pasta do seu PC) | `./conectores:/conectores` | A pasta `conectores` do seu computador aparece dentro do container. Se você editar o JSON no seu editor, o container vê na hora |

### 2.4 Rede (`networks`)

Containers na mesma rede se encontram **pelo nome do serviço**, como ramais de telefone dentro de uma empresa.

| Quem chama | Endereço usado | Por quê |
|---|---|---|
| Connect → Kafka | `kafka-broker:29092` | Estão na mesma rede `rede_fia`; o nome vira o endereço |
| Connect → Postgres | `postgres:5432` | Idem |
| Você (navegador) → pgAdmin | `localhost:5433` | Você está **fora** da rede; entra pela porta aberta |

> ⚠️ **A pegadinha do `localhost`:** dentro de um container, `localhost` é **o próprio container**, não o seu computador. Por isso, no pgAdmin, o servidor é `postgres`, e não `localhost`.

### 2.5 Variáveis de ambiente (`environment`) e o arquivo `.env`

São configurações passadas para o programa na hora em que ele liga, como um bilhete deixado na mesa: "a senha é postgres".

O arquivo `.env` guarda valores que o **Compose** substitui no `docker-compose.yaml` antes de subir tudo:

```
# .env
POSTGRES_DEBEZIUM=3.0
PAGADMIN_VERSION=9.0
CONFLUENT_VERSION=7.6.1
```

```yaml
image: confluentinc/cp-kafka:${CONFLUENT_VERSION}   # vira cp-kafka:7.6.1
```

Para ver o arquivo final, já com as variáveis trocadas:

```bash
docker compose config
```

---

## 3. O docker-compose.yaml, linha por linha

### 3.1 As chaves que aparecem em todo serviço

| Chave | O que faz | Exemplo |
|---|---|---|
| `services:` | Começa a lista de containers | — |
| `postgres:` (nome do serviço) | Nome do serviço. **Vira o endereço** dele na rede | `postgres` |
| `image:` | Qual imagem usar | `confluentinc/cp-kafka:${CONFLUENT_VERSION}` |
| `container_name:` | Nome fixo do container (usado em `docker exec`, `docker logs`) | `kafkaConect` |
| `ports:` | Portas abertas para o seu computador | `- "9092:9092"` |
| `environment:` | Configurações do programa | `POSTGRES_PASSWORD=postgres` |
| `volumes:` | "HDs" ligados ao container | `./conectores:/conectores` |
| `depends_on:` | Ordem de **início**: liga este serviço depois daqueles | `- kafka-broker` |
| `networks:` | Em qual rede o container entra | `rede_fia:` |
| `restart:` | O que fazer se o container cair | `on-failure` |
| `command:` | O comando que o container executa ao ligar | `/opt/kafka/kafka_connect_run.sh` |

> ⚠️ **`depends_on` não espera o serviço ficar pronto.** Ele só garante que o container do Kafka **começou a ligar** antes do Connect. O Kafka pode levar alguns segundos para aceitar conexões. Por isso o Connect tem `restart: on-failure`: se ele cair por não achar o Kafka, o Docker liga de novo.

> 💡 **Duas formas de escrever `environment`:** as duas funcionam e aparecem neste arquivo.
> ```yaml
> environment:              # forma de lista
>   - POSTGRES_USER=postgres
> environment:              # forma de dicionário
>   POSTGRES_USER: postgres
> ```

### 3.2 `postgres`

```yaml
postgres:
  image: quay.io/debezium/example-postgres:${POSTGRES_DEBEZIUM}
  container_name: postgres
  ports:
   - 5432:5432
  environment:
   - POSTGRES_USER=postgres
   - POSTGRES_PASSWORD=postgres
  networks:
    rede_fia:
```

| Linha | O que significa |
|---|---|
| `image: quay.io/debezium/example-postgres:3.0` | Um PostgreSQL preparado pelo time do Debezium: já vem com `wal_level=logical` e os plugins de leitura do diário instalados |
| `ports: 5432:5432` | Abre o banco para o seu computador (para ferramentas como DBeaver). O pgAdmin **não** usa esta porta: ele fala pela rede interna |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` | Usuário e senha do banco. O Debezium usa os mesmos |

> Este container **não tem volume**. Se você rodar `docker compose down`, o banco volta ao zero e o `sql/hospital.sql` precisa ser executado de novo.

### 3.3 `pgadmin`

| Linha | O que significa |
|---|---|
| `image: dpage/pgadmin4:9.0` | A tela web oficial do PostgreSQL |
| `PGADMIN_DEFAULT_EMAIL` / `PGADMIN_DEFAULT_PASSWORD` | Login da **tela** do pgAdmin (não é a senha do banco) |
| `ports: "5433:80"` | Acesse em `http://localhost:5433` |
| `depends_on: postgres` | Liga depois do banco |

### 3.4 `zookeeper`

| Linha | O que significa |
|---|---|
| `image: confluentinc/cp-zookeeper:7.6.1` | O ZooKeeper empacotado pela Confluent |
| `ZOOKEEPER_CLIENT_PORT: 2181` | Porta em que o Kafka conversa com o ZooKeeper |
| `ZOOKEEPER_TICK_TIME: 2000` | A "batida do relógio" interna, em milissegundos |
| `ZOOKEEPER_INIT_LIMIT` / `SYNC_LIMIT` | Quantas batidas esperar antes de considerar um nó atrasado. Só importa com vários ZooKeepers |
| `ZOOKEEPER_4LW_COMMANDS_WHITELIST: "*"` | Libera comandos de diagnóstico de 4 letras (como `ruok`, "você está bem?") |
| `ulimits: nofile: 65536` | Permite abrir muitos arquivos ao mesmo tempo. Kafka e ZooKeeper abrem milhares |

> **ZooKeeper está saindo de cena.** Versões novas do Kafka (4.0 em diante) usam o modo **KRaft**, em que o próprio Kafka se organiza, sem ZooKeeper. Usamos ZooKeeper porque é o formato das aulas do curso.

### 3.5 `kafka-broker`

```yaml
KAFKA_BROKER_ID: 101
KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-broker:29092,PLAINTEXT_HOST://localhost:9092
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
CONFLUENT_METRICS_ENABLE: 'false'
```

| Linha | O que significa |
|---|---|
| `KAFKA_BROKER_ID: 101` | O "crachá" deste servidor Kafka. Precisa ser único se houver vários |
| `KAFKA_ZOOKEEPER_CONNECT` | Onde está o ZooKeeper |
| `KAFKA_ADVERTISED_LISTENERS` | **Os dois endereços** que o Kafka divulga (veja abaixo) |
| `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP` | Os dois endereços usam texto simples, sem criptografia (ok para laboratório) |
| `KAFKA_INTER_BROKER_LISTENER_NAME` | Qual endereço os brokers usam entre si |
| `..._REPLICATION_FACTOR: 1` e `MIN_ISR: 1` | Quantas cópias dos tópicos internos guardar. Temos **1 broker só**, então só cabe 1 cópia. Em produção, normalmente 3 |
| `CONFLUENT_METRICS_ENABLE: 'false'` | Desliga as métricas extras da Confluent (não usamos) |

**Por que dois endereços?**

O Kafka entrega ao cliente um endereço para ele voltar a se conectar. Esse endereço precisa funcionar **de onde o cliente está**:

| Quem conecta | Usa | Por quê |
|---|---|---|
| Containers (Connect) | `kafka-broker:29092` | Dentro da rede, o nome `kafka-broker` existe |
| Seu computador | `localhost:9092` | Fora da rede, o nome `kafka-broker` não existe; `localhost:9092` cai na porta aberta |
| Comandos **dentro** do container do Kafka | `localhost:9092` | Lá dentro, `localhost` é o próprio Kafka |

Analogia: a empresa tem um **ramal interno** (29092) para quem está no prédio e um **telefone externo** (9092) para quem está na rua.

### 3.6 `connect`

```yaml
connect:
  image: fernandos/kafka-connet-debezium-lab:v215
  container_name: kafkaConect
  ports:
  - 8083:8083
  depends_on:
   - kafka-broker
  restart: on-failure
  volumes:
    - "./conectores:/conectores"
  environment:
  - KAFKA_LOG4J_OPTS=-Dlog4j.configuration=file:/opt/kafka/config/connect-log4j.properties
  - KAFKA_CONNECT_BOOTSTRAP_SERVERS=kafka-broker:29092
  - |
      KAFKA_CONNECT_CONFIGURATION=
      key.converter=org.apache.kafka.connect.json.JsonConverter
      value.converter=org.apache.kafka.connect.json.JsonConverter
      key.converter.schemas.enable=false
      value.converter.schemas.enable=false
      group.id=connect
      offset.storage.topic=connect-offsets
      offset.storage.replication.factor=1
      config.storage.topic=connect-configs
      config.storage.replication.factor=1
      status.storage.topic=connect-status
      status.storage.replication.factor=1
  command: /opt/kafka/kafka_connect_run.sh
```

| Linha | O que significa |
|---|---|
| `image: fernandos/kafka-connet-debezium-lab:v215` | Imagem do curso: Kafka Connect + plugins Debezium e S3 Sink já instalados (o "connet" sem "c" é o nome real da imagem) |
| `container_name: kafkaConect` | Nome usado em `docker exec -it kafkaConect bash` |
| `ports: 8083:8083` | A **API REST** do Connect: é por aqui que você dá ordens |
| `restart: on-failure` | Se cair (por exemplo, o Kafka ainda não estava pronto), liga de novo |
| `./conectores:/conectores` | Os arquivos JSON dos conectores aparecem dentro do container em `/conectores` |
| `KAFKA_LOG4J_OPTS` | Onde está a configuração dos logs (o que aparece em `docker logs`) |
| `KAFKA_CONNECT_BOOTSTRAP_SERVERS` | Onde está o Kafka (endereço **interno**) |
| `- \|` | No YAML, o `\|` significa "o texto a seguir tem várias linhas, mantenha as quebras" |
| `KAFKA_CONNECT_CONFIGURATION=` | Bloco de configuração do Connect (explicado abaixo) |
| `command: /opt/kafka/kafka_connect_run.sh` | O script que liga o Connect, lendo as variáveis acima |

**O bloco `KAFKA_CONNECT_CONFIGURATION`:**

| Linha | O que significa | Analogia |
|---|---|---|
| `key.converter=...JsonConverter` | A **chave** das mensagens será gravada no Kafka como JSON | A língua em que a etiqueta da caixa é escrita |
| `value.converter=...JsonConverter` | O **conteúdo** das mensagens será JSON | A língua da carta dentro da caixa |
| `key/value.converter.schemas.enable=false` | **Não** colocar a descrição dos campos (o "schema") dentro de cada mensagem. A mensagem fica bem menor e mais fácil de ler | Mandar só a carta, sem o manual de como ler a carta |
| `group.id=connect` | Nome do "time" de Connects. Vários containers com o mesmo `group.id` dividem o trabalho | O nome da equipe |
| `offset.storage.topic=connect-offsets` | Tópico onde o Connect anota **até onde já leu** | O marcador de página |
| `config.storage.topic=connect-configs` | Tópico onde ficam salvos os conectores que você criou | A pasta de contratos |
| `status.storage.topic=connect-status` | Tópico com o estado de cada conector (RUNNING, FAILED...) | O quadro de avisos |
| `*.replication.factor=1` | 1 cópia de cada tópico interno (só temos 1 broker) | — |

> 💡 **Por isso o Connect "lembra" dos conectores** depois de reiniciar: tudo fica guardado em tópicos do próprio Kafka, não no container.

### 3.7 `minio`

| Linha | O que significa |
|---|---|
| `image: cgr.dev/chainguard/minio:latest` | O MinIO empacotado pela Chainguard (veja a seção 4) |
| `user: root` | Roda como administrador dentro do container. A imagem normalmente roda com um usuário limitado, que não tem permissão de gravar no volume novo |
| `ports: 9000` | A **API S3**: é por aqui que programas (o Sink, o `mc`) gravam e leem arquivos |
| `ports: 9001` | O **console**: a tela web, em `http://localhost:9001` |
| `minio_storage:/data` | Volume onde os arquivos ficam guardados |
| `MINIO_ROOT_USER` / `PASSWORD` | Login de administrador (`admin` / `minioadmin`) |
| `MINIO_NOTIFY_KAFKA_*` | Configura o MinIO para **avisar o Kafka** quando um arquivo chega. Vem da aula original; esta revisão não usa, mas não atrapalha |
| `command: server --console-address ":9001" /data` | "Ligue o servidor, coloque o console na porta 9001 e guarde tudo em `/data`" |

### 3.8 `mc`

```yaml
mc:
  image: cgr.dev/chainguard/minio-client:latest
  container_name: mc
  depends_on:
    - minio
  environment:
    MC_HOST_myminio: http://admin:minioadmin@minio:9000
  command: ["mb", "--ignore-existing", "myminio/bronze"]
  restart: on-failure
```

| Linha | O que significa |
|---|---|
| `image: ...minio-client` | O `mc`, programa de linha de comando do MinIO |
| `MC_HOST_myminio: http://admin:minioadmin@minio:9000` | Cria o apelido `myminio` apontando para o MinIO, com usuário e senha. O formato é `MC_HOST_<apelido>` |
| `command: ["mb", "--ignore-existing", "myminio/bronze"]` | Executa `mc mb` (*make bucket*, "crie o bucket") `bronze`. `--ignore-existing` evita erro se ele já existir |
| `restart: on-failure` | Se o MinIO ainda estiver ligando, o comando falha e o Docker tenta de novo, até dar certo |

Depois de criar o bucket, o `mc` termina e o container **desliga**. É normal ele não aparecer em `docker ps`.

> **`command` x `entrypoint`:** o `entrypoint` é o **programa** que o container executa; o `command` são os **argumentos** passados a ele. Nesta imagem, o `entrypoint` já é o `mc`, então o `command` só completa: `mc` + `mb --ignore-existing myminio/bronze`.

### 3.9 Final do arquivo

```yaml
networks:
  rede_fia:
    driver: bridge

volumes:
  minio_storage: {}
```

| Linha | O que significa |
|---|---|
| `networks: rede_fia: driver: bridge` | Cria a rede interna `rede_fia`. `bridge` é o tipo padrão: uma rede privada dentro do seu computador |
| `volumes: minio_storage: {}` | Declara o volume nomeado. O `{}` quer dizer "configurações padrão" |

---

## 4. As imagens usadas

| Serviço | Imagem | Quem publica | O que tem dentro | Por que esta |
|---|---|---|---|---|
| postgres | `quay.io/debezium/example-postgres:3.0` | Projeto Debezium | PostgreSQL com `wal_level=logical` e plugins de decodificação | Pronto para CDC sem configurar nada |
| pgadmin | `dpage/pgadmin4:9.0` | Projeto pgAdmin | Tela web do Postgres | Padrão do mercado |
| zookeeper | `confluentinc/cp-zookeeper:7.6.1` | Confluent | ZooKeeper | Mesmo pacote do Kafka |
| kafka-broker | `confluentinc/cp-kafka:7.6.1` | Confluent | Apache Kafka 3.6 + comandos `kafka-*` | Igual às aulas de Kafka do curso |
| connect | `fernandos/kafka-connet-debezium-lab:v215` | Professor do curso | Kafka Connect (base Strimzi) + Debezium PostgreSQL + Confluent S3 Sink | Plugins já instalados; é a imagem da aula 21 do curso |
| minio | `cgr.dev/chainguard/minio:latest` | Chainguard | Servidor MinIO | As imagens oficiais do MinIO deixaram de ser distribuídas publicamente (dão erro 401) |
| mc | `cgr.dev/chainguard/minio-client:latest` | Chainguard | Comando `mc` | Mesmo motivo |

### 4.1 Como uma imagem de Connect "ganha" plugins

O Kafka Connect, sozinho, não sabe falar com Postgres nem com S3. Os **plugins** (arquivos `.jar`) ensinam isso. A imagem do curso foi construída mais ou menos assim (um `Dockerfile`):

```dockerfile
FROM quay.io/strimzi/kafka:<versão>          # 1. parte de uma imagem com Kafka Connect
USER root
RUN mkdir -p /opt/kafka/plugins/debezium     # 2. cria a pasta de plugins
# 3. baixa e descompacta os plugins (Debezium Postgres, S3 Sink) nessa pasta
USER 1001
```

| Conceito | Explicação |
|---|---|
| `FROM` | "Comece a partir desta imagem". Toda imagem é feita em camadas sobre outra |
| Pasta de plugins | O Connect procura plugins numa pasta (`plugin.path`). Tudo que estiver lá vira um conector disponível |
| Resultado | Uma imagem nova, publicada no Docker Hub, que qualquer aluno baixa já pronta |

Para ver os plugins que vieram na imagem:

```bash
curl -s http://localhost:8083/connector-plugins
```

### 4.2 Arquitetura do processador

A imagem do Connect foi feita para processadores **Intel/AMD (amd64)**. Em Macs com chip Apple (M1, M2...), o Docker a roda **emulada**: funciona, mas fica mais lenta para ligar.

---

## 5. Comandos do Docker e do Compose

> Rode estes comandos na pasta onde está o `docker-compose.yaml`. Eles são iguais em Windows (PowerShell), Linux e Mac.

### 5.1 Subir, parar, apagar

| Comando | O que faz | Quando usar |
|---|---|---|
| `docker compose up -d` | Baixa as imagens que faltam e liga tudo. `-d` = em segundo plano, devolvendo o terminal | Início da aula |
| `docker compose up -d mc` | Liga (ou religa) **só** o serviço `mc` | Refazer um serviço específico |
| `docker compose ps` | Lista os containers do projeto e o estado de cada um | Conferir se tudo subiu |
| `docker compose stop` | **Pausa** os containers (nada é apagado) | Fim do dia, para continuar depois |
| `docker compose start` | Religa os containers pausados | Retomar |
| `docker compose restart connect` | Reinicia um serviço | Ele travou |
| `docker compose down` | **Apaga** os containers e a rede. Volumes ficam | Recomeçar do zero, mas mantendo os arquivos do MinIO |
| `docker compose down -v` | Apaga containers, rede **e volumes** | Limpeza total |
| `docker compose config` | Mostra o compose final, com as variáveis do `.env` trocadas | Conferir se o `.env` foi lido |
| `docker compose pull` | Baixa (atualiza) as imagens sem ligar nada | Antes da aula, com internet boa |

### 5.2 Olhar e entrar

| Comando | O que faz | Quando usar |
|---|---|---|
| `docker ps` | Lista os containers **ligados** (de qualquer projeto) | Ver o que está rodando |
| `docker ps -a` | Lista **todos**, inclusive os desligados | Ver se o `mc` terminou ou deu erro |
| `docker logs kafkaConect` | Mostra o que o container escreveu na tela | Investigar um erro |
| `docker logs -f kafkaConect` | Igual, mas **acompanha ao vivo** (`Ctrl+C` para sair) | Ver o Connect ligando |
| `docker logs --tail 50 kafkaConect` | Só as últimas 50 linhas | Logs muito grandes |
| `docker exec -it kafka-broker bash` | **Entra** no container e abre um terminal lá dentro | Usar os comandos do Kafka |
| `exit` | Sai do container (ele continua ligado) | — |
| `docker stats` | Uso de CPU e memória de cada container, ao vivo | Computador lento |
| `docker images` | Lista as imagens baixadas | — |
| `docker volume ls` | Lista os volumes | Achar o `minio_storage` |

**`docker exec -it kafka-broker bash`, parte por parte:**

| Parte | Significado |
|---|---|
| `docker exec` | Executa um comando em um container que **já está ligado** |
| `-i` | Interativo: mantém a entrada do teclado aberta |
| `-t` | Cria um terminal "de verdade" (com cores, prompt) |
| `kafka-broker` | Em qual container |
| `bash` | Qual programa abrir: o terminal |

> 💡 Você percebe que está **dentro** de um container porque o começo da linha muda, por exemplo para `[appuser@a1b2c3d4 ~]$` ou `[kafka@c8553c7d5c6d kafka]$`.

---

## 6. Kafka: conceitos

### 6.1 As palavras principais

| Conceito | O que é | Analogia |
|---|---|---|
| **Broker** | Um servidor Kafka. Aqui temos um: `kafka-broker` | Um galpão da fábrica |
| **Tópico** | Uma fila de mensagens com nome. Ex.: `hospital.prontosocorro.atendimentos` | Uma esteira com etiqueta |
| **Mensagem** (ou evento, registro) | Um item na fila. Tem **chave**, **valor** e data/hora | Uma caixa na esteira |
| **Chave** (*key*) | Identifica do que a mensagem fala. Ex.: `{"id": 3}` | A etiqueta da caixa |
| **Valor** (*value*) | O conteúdo. Ex.: o atendimento inteiro em JSON | O que tem dentro da caixa |
| **Partição** | Um tópico pode ser dividido em várias filas paralelas. Mensagens com a **mesma chave** vão sempre para a **mesma partição**, e por isso ficam em ordem | Várias faixas da mesma esteira |
| **Offset** | O número da posição da mensagem dentro da partição: 0, 1, 2... | O número da senha na fila do banco |
| **Producer** | Quem **escreve** mensagens. Aqui: o Debezium | Quem coloca caixas na esteira |
| **Consumer** | Quem **lê** mensagens. Aqui: o S3 Sink e o `kafka-console-consumer` | Quem retira caixas da esteira |
| **Consumer group** | Um time de consumidores. O Kafka anota até onde **cada time** já leu | Cada departamento tem seu marcador de página |
| **Retenção** | Por quanto tempo as mensagens ficam guardadas (padrão: 7 dias) | Por quanto tempo as caixas ficam no depósito |

### 6.2 A diferença para uma fila comum

Numa fila comum, quem lê a mensagem a **remove**. No Kafka, ler **não apaga**:

- Vários consumidores leem o mesmo tópico, cada um no seu ritmo.
- Um consumidor novo pode começar do início (`--from-beginning`) e reler tudo.
- Se o Sink ficar desligado por uma hora, ao voltar ele continua de onde parou, porque seu offset está anotado.

### 6.3 Como os tópicos desta aula são nomeados

O Debezium cria um tópico por tabela, no formato `<prefixo>.<schema>.<tabela>`:

| Tópico | Prefixo (`topic.prefix`) | Schema | Tabela |
|---|---|---|---|
| `cdc.prontosocorro.atendimentos` | `cdc` | `prontosocorro` | `atendimentos` |
| `hospital.prontosocorro.pacientes` | `hospital` | `prontosocorro` | `pacientes` |

Tópicos que começam com `connect-` ou `__` (como `__consumer_offsets`) são **internos**: do Connect e do próprio Kafka. Não mexa neles.

---

## 7. Kafka: comandos básicos

Primeiro, entre no container do Kafka:

```bash
docker exec -it kafka-broker bash
```

Todos os comandos abaixo rodam **lá dentro** e usam `--bootstrap-server localhost:9092`, que significa *"o Kafka está aqui mesmo, na porta 9092"*.

### 7.1 Tópicos (`kafka-topics`)

| Comando | O que faz |
|---|---|
| `kafka-topics --bootstrap-server localhost:9092 --list` | Lista todos os tópicos |
| `kafka-topics --bootstrap-server localhost:9092 --describe --topic hospital.prontosocorro.atendimentos` | Detalhes: partições, réplicas, líder |
| `kafka-topics --bootstrap-server localhost:9092 --create --topic teste --partitions 3 --replication-factor 1` | Cria o tópico `teste` com 3 partições |
| `kafka-topics --bootstrap-server localhost:9092 --delete --topic teste` | Apaga o tópico `teste` |

| Opção | Significado |
|---|---|
| `--partitions 3` | Quantas filas paralelas o tópico terá |
| `--replication-factor 1` | Quantas cópias de cada partição. Não pode ser maior que o número de brokers (aqui, 1) |

> Na aula **não precisamos criar tópicos à mão**: o Kafka os cria sozinho na primeira mensagem (`auto.create.topics.enable`, ligado por padrão nesta imagem).

### 7.2 Escrever mensagens (`kafka-console-producer`)

```bash
kafka-console-producer --bootstrap-server localhost:9092 --topic teste
```

O cursor fica esperando. Cada linha que você digitar e der **Enter** vira uma mensagem. `Ctrl+C` para sair.

Com chave (separada do valor por `:`):

```bash
kafka-console-producer --bootstrap-server localhost:9092 --topic teste --property parse.key=true --property key.separator=:
```

Digite, por exemplo: `paciente1:{"nome":"Maria"}`

### 7.3 Ler mensagens (`kafka-console-consumer`)

```bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic hospital.prontosocorro.atendimentos --from-beginning --property print.key=true
```

| Opção | O que faz |
|---|---|
| `--topic ...` | Qual tópico ler |
| `--from-beginning` | Começa da **primeira** mensagem guardada. Sem isso, mostra só as que chegarem **daqui pra frente** |
| `--property print.key=true` | Mostra a chave antes do valor |
| `--property print.timestamp=true` | Mostra a data/hora de cada mensagem |
| `--property print.partition=true` | Mostra em qual partição a mensagem está |
| `--max-messages 1` | Para depois de 1 mensagem (útil para ver só um exemplo) |
| `--group meu-time` | Lê como parte de um consumer group, que guarda a posição |

O consumer fica **esperando novas mensagens** até você apertar `Ctrl+C`. Isso é normal: é o "tempo real".

> 💡 **Exercício clássico:** abra dois terminais. Num, deixe o consumer rodando. No outro (ou no pgAdmin), faça um `INSERT`. A mensagem aparece no consumer em segundos.

### 7.4 Consumer groups (`kafka-consumer-groups`)

| Comando | O que faz |
|---|---|
| `kafka-consumer-groups --bootstrap-server localhost:9092 --list` | Lista os times de consumidores |
| `kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group connect-connector-minio-bronze` | Mostra até onde o Sink já leu |

A saída do `--describe` tem estas colunas importantes:

| Coluna | Significado |
|---|---|
| `CURRENT-OFFSET` | Até onde o time já leu |
| `LOG-END-OFFSET` | Quantas mensagens existem no tópico |
| `LAG` | **Quantas faltam ler** (`LOG-END - CURRENT`). Se o `LAG` não diminui, o consumidor está parado |

> Todo **conector Sink** vira um consumer group chamado `connect-<nome-do-conector>`.

---

## 8. Kafka Connect: conceitos

### 8.1 Por que existe

Sem o Connect, para levar dados do Postgres para o Kafka você escreveria um programa: conectar no banco, descobrir o que mudou, transformar em mensagem, enviar, tratar erros, lembrar onde parou... O Connect já faz tudo isso. Você só **descreve** o que quer num arquivo JSON.

| Sem Connect | Com Connect |
|---|---|
| Escrever, testar e manter código | Escrever um JSON de configuração |
| Cada equipe faz do seu jeito | Todos usam os mesmos plugins, testados por milhares de empresas |
| Se o programa cai, você precisa saber onde parou | O Connect anota o progresso sozinho (`connect-offsets`) |

### 8.2 As palavras principais

| Conceito | O que é | Neste projeto |
|---|---|---|
| **Worker** | O processo (container) do Kafka Connect | `kafkaConect` |
| **Plugin** | O "driver" que sabe falar com um sistema | Debezium PostgreSQL, S3 Sink |
| **Conector** | Uma **configuração** de um plugin, com nome. Um plugin pode ter vários conectores | `connector-hospital-cdc`, `connector-hospital`, `connector-minio-bronze` |
| **Task** | O "trabalhador" que de fato move os dados. Um conector tem 1 ou mais tasks (`tasks.max`) | `tasks[0]` |
| **Source** | Conector que **traz** dados de fora **para o Kafka** | Debezium |
| **Sink** | Conector que **leva** dados **do Kafka** para fora | S3 Sink |
| **Converter** | Define o formato das mensagens no Kafka (JSON, Avro...) | `JsonConverter` |
| **SMT** (*Single Message Transform*) | Uma pequena transformação aplicada em cada mensagem no caminho | `unwrap`, `extractKey` |

```
 SOURCE                                           SINK
 Postgres ──► [plugin Debezium] ──► converter ──► Kafka ──► converter ──► [plugin S3] ──► MinIO
                    │                                                         │
                  SMTs (opcional)                                          SMTs (opcional)
```

### 8.3 Os estados de um conector

| Estado | Significado | O que fazer |
|---|---|---|
| `RUNNING` | Funcionando | Nada |
| `PAUSED` | Pausado por você | `resume` quando quiser |
| `FAILED` | Deu erro | Leia o campo `trace` no `status` |
| `UNASSIGNED` | Ainda não foi entregue a um worker | Espere alguns segundos |

> ⚠️ **O conector e a task têm estados separados.** É comum o conector estar `RUNNING` e a **task** estar `FAILED`. Sempre olhe os dois no `status`.

---

## 9. Kafka Connect: comandos da API

O Connect não tem tela. Você conversa com ele mandando mensagens HTTP para a porta **8083**, com o comando `curl`.

### 9.1 O `curl` em 1 minuto

| Parte | Significado | Analogia |
|---|---|---|
| `curl` | Programa que envia uma mensagem HTTP | O carteiro |
| `-s` | Silencioso: sem barra de progresso | — |
| `-X GET` / `PUT` / `POST` / `DELETE` | O **tipo** do pedido. Sem `-X`, é `GET` | "Quero ver" / "Quero gravar" / "Quero que faça" / "Quero apagar" |
| `-H 'Content-Type: application/json'` | Avisa que o conteúdo é JSON | Escrever "carta em português" no envelope |
| `-d @arquivo.json` | Envia o conteúdo do arquivo. O `@` quer dizer "leia deste arquivo" | O conteúdo da carta |
| `http://localhost:8083/...` | Para onde mandar | O endereço |

### 9.2 De onde rodar

| Onde você está | Endereço | Caminho do JSON |
|---|---|---|
| **Dentro** do Connect (`docker exec -it kafkaConect bash`) | `http://localhost:8083` | `@/conectores/arquivo.json` |
| No **seu computador** (Linux, Mac, Git Bash) | `http://localhost:8083` | `@conectores/arquivo.json` |
| No **PowerShell** (Windows) | `http://localhost:8083` | Use `curl.exe` (e não `curl`, que no PowerShell é outro comando) |

### 9.3 Consultar

| Comando | O que mostra |
|---|---|
| `curl -s http://localhost:8083/` | Versão do Connect. Se responde, ele está no ar |
| `curl -s http://localhost:8083/connector-plugins` | Plugins instalados |
| `curl -s http://localhost:8083/connectors` | Nomes dos conectores criados |
| `curl -s "http://localhost:8083/connectors?expand=status"` | Todos os conectores com seus estados, de uma vez |
| `curl -s http://localhost:8083/connectors/connector-hospital/status` | Estado do conector e das tasks (e o erro, se houver) |
| `curl -s http://localhost:8083/connectors/connector-hospital/config` | A configuração atual |
| `curl -s http://localhost:8083/connectors/connector-hospital/topics` | Quais tópicos o conector já usou |

### 9.4 Criar e alterar

```bash
curl -s -X PUT -H 'Content-Type: application/json' -d @/conectores/connector-hospital.json http://localhost:8083/connectors/connector-hospital/config
```

| Parte | Significado |
|---|---|
| `-X PUT` | "Grave esta configuração". Se o conector não existe, **cria**; se existe, **atualiza** |
| `/connectors/connector-hospital/config` | O nome do conector vai **no endereço** |
| `-d @/conectores/connector-hospital.json` | O arquivo só tem a configuração, sem o nome |

> 💡 Por isso usamos `PUT .../config` e não `POST /connectors`: o mesmo comando serve para criar **e** para corrigir. Mudou o JSON? Rode de novo.

### 9.5 Controlar

| Comando | O que faz | Quando usar |
|---|---|---|
| `curl -s -X PUT http://localhost:8083/connectors/connector-hospital/pause` | Pausa. As mudanças continuam guardadas na origem | Manutenção |
| `curl -s -X PUT http://localhost:8083/connectors/connector-hospital/resume` | Retoma de onde parou | Depois da pausa |
| `curl -s -X POST http://localhost:8083/connectors/connector-hospital/restart` | Reinicia o conector | Mudou algo fora (ex.: senha do banco) |
| `curl -s -X POST http://localhost:8083/connectors/connector-minio-bronze/tasks/0/restart` | Reinicia **só a task 0** | A task está `FAILED` e você já corrigiu a causa |
| `curl -s -X DELETE http://localhost:8083/connectors/connector-hospital` | Apaga o conector | Limpeza |

> ⚠️ **Apagar um conector Debezium não apaga o *replication slot* no Postgres** (seção 10.3). O slot continua segurando o diário do banco. Remova-o na limpeza.

---

## 10. Debezium e o PostgreSQL por dentro

### 10.1 Como o Debezium lê o banco

1. Ao ser criado, o conector tira uma **foto** (*snapshot*) das tabelas: cada linha existente vira uma mensagem com `"op": "r"` (*read*).
2. Depois, ele passa a ler o **WAL**, o diário em que o Postgres anota cada mudança antes de aplicá-la.
3. Cada `INSERT`, `UPDATE` ou `DELETE` vira uma mensagem no Kafka.

Ele **não faz consultas** nas tabelas para descobrir o que mudou. Por isso pesa pouco no banco.

### 10.2 Os requisitos no Postgres

| Requisito | Para que serve | Como conferir |
|---|---|---|
| `wal_level = logical` | O diário precisa descrever as mudanças linha por linha | `SHOW wal_level;` |
| Usuário com permissão de replicação | O Debezium se conecta como um "leitor do diário" | Aqui usamos o `postgres`, que pode tudo |
| `REPLICA IDENTITY FULL` (opcional) | Faz o `before` vir completo no `UPDATE` e no `DELETE` | Está no `hospital.sql` |

### 10.3 Replication slot e publication

| Conceito | O que é | Analogia |
|---|---|---|
| **Replication slot** | Um "marcador" no Postgres que lembra até onde o Debezium já leu o diário. O Postgres **guarda o diário** até o slot avançar | O marcador de página que impede o livro de ser jogado fora |
| **Publication** | A lista de tabelas cujas mudanças o Postgres publica | A lista de assinantes do jornal |

Cada conector Debezium precisa do **seu próprio slot** (`slot.name`). Por isso temos `debezium_cdc` e `debezium_hospital`.

Para ver no pgAdmin:

```sql
SELECT slot_name, active FROM pg_replication_slots;
SELECT * FROM pg_publication;
```

Para remover um slot que sobrou (o conector precisa estar apagado antes):

```sql
SELECT pg_drop_replication_slot('debezium_cdc');
```

> ⚠️ **Por que isso importa:** um slot esquecido faz o Postgres guardar o diário **para sempre**, esperando um leitor que não volta. Em produção, isso enche o disco do banco.

### 10.4 O "envelope" da mensagem (sem SMT)

```json
{
  "before": null,
  "after":  { "id": 4, "paciente_id": 5, "classificacao_risco": "VERMELHO", "...": "..." },
  "source": { "table": "atendimentos", "ts_ms": 1760000000000, "...": "..." },
  "op": "c",
  "ts_ms": 1760000000123
}
```

| Campo | Significado |
|---|---|
| `before` | Como a linha **era** (vazio num `INSERT`) |
| `after` | Como a linha **ficou** (vazio num `DELETE`) |
| `source` | De onde veio: banco, schema, tabela, hora |
| `op` | O tipo de operação |

| `op` | Significado |
|---|---|
| `r` | *read*: linha lida na foto inicial |
| `c` | *create*: `INSERT` |
| `u` | *update*: `UPDATE` |
| `d` | *delete*: `DELETE` |

Depois de um `DELETE`, o Debezium manda também uma mensagem com valor **vazio** (*tombstone*, "lápide"). Ela avisa ao Kafka que aquela chave pode ser esquecida.

> **Datas:** uma coluna `DATE` chega como **número de dias desde 01/01/1970**. Ex.: `-4313` = 1958-03-12. Não é erro; é o formato padrão do Debezium.

### 10.5 Os SMTs desta aula

| SMT | Configuração | O que faz |
|---|---|---|
| `unwrap` | `ExtractNewRecordState` | Joga fora o envelope e deixa só o `after`, a linha como ficou |
| `unwrap.add.fields` | `op,source.ts_ms` | Acrescenta `__op` e `__source_ts_ms` na mensagem limpa, para não perder o tipo e a hora |
| `unwrap.delete.tombstone.handling.mode` | `tombstone` | Num `DELETE`, manda só a lápide |
| `extractKey` | `ExtractField$Key`, campo `id` | A chave deixa de ser `{"id": 3}` e vira só `3` |

---

## 11. O Sink do MinIO por dentro

### 11.1 A configuração

| Campo | Valor | Significado |
|---|---|---|
| `connector.class` | `io.confluent.connect.s3.S3SinkConnector` | O plugin de gravar em S3 |
| `topics` | `hospital.prontosocorro.atendimentos` | De qual tópico ler |
| `s3.bucket.name` | `bronze` | Em qual bucket gravar. **Precisa existir antes** |
| `store.url` | `http://minio:9000` | Onde está o "S3". Sem isso, o plugin tentaria a Amazon de verdade |
| `s3.region` | `us-east-1` | Obrigatório pelo protocolo S3; o MinIO aceita qualquer um |
| `aws.access.key.id` / `secret` | `admin` / `minioadmin` | Login no MinIO |
| `flush.size` | `3` | Grava um arquivo **a cada 3 mensagens** |
| `format.class` | `JsonFormat` | Os arquivos serão JSON |
| `storage.class` | `S3Storage` | Grava em armazenamento compatível com S3 |
| `behavior.on.null.values` | `ignore` | Ignora as lápides (mensagens vazias) em vez de falhar |

### 11.2 Onde os arquivos aparecem

```
bronze/
└── topics/
    └── hospital.prontosocorro.atendimentos/
        └── partition=0/
            ├── hospital.prontosocorro.atendimentos+0+0000000000.json
            └── hospital.prontosocorro.atendimentos+0+0000000003.json
```

| Parte do nome | Significado |
|---|---|
| `topics/` | Pasta padrão do Sink |
| `partition=0` | Partição do tópico de onde as mensagens vieram |
| `+0+0000000000` | Partição 0, começando no offset 0 (o arquivo tem os offsets 0, 1, 2) |

Cada arquivo tem **uma mensagem JSON por linha**.

> **Por que não aparece arquivo?** Com `flush.size = 3`, o Sink só grava quando junta 3 mensagens. Se o tópico tem 4, você verá 1 arquivo; a 4ª espera mais 2. Em produção, usa-se também `rotate.interval.ms` para gravar por tempo.

---

## 12. Diagnóstico: quando algo dá errado

### 12.1 O roteiro

Siga nesta ordem, do mais básico para o mais específico:

| # | Pergunta | Comando |
|---|---|---|
| 1 | Os containers estão ligados? | `docker compose ps` |
| 2 | Algum caiu? Por quê? | `docker logs --tail 50 <container>` |
| 3 | O Connect responde? | `curl -s http://localhost:8083/` |
| 4 | Os plugins estão lá? | `curl -s http://localhost:8083/connector-plugins` |
| 5 | O conector e a task estão `RUNNING`? | `curl -s http://localhost:8083/connectors/<nome>/status` |
| 6 | O tópico existe e tem mensagens? | `kafka-topics --list` e `kafka-console-consumer ... --from-beginning` |
| 7 | O Sink está lendo? | `kafka-consumer-groups --describe --group connect-<nome>` (olhe o `LAG`) |
| 8 | O arquivo chegou? | Console do MinIO em `http://localhost:9001` |

### 12.2 Erros comuns

| Mensagem | Causa | Solução |
|---|---|---|
| `Connection refused` no `curl` | O Connect ainda está ligando | Espere 1 a 2 minutos. Acompanhe com `docker logs -f kafkaConect` |
| `schema "prontosocorro" does not exist` | Rodou só parte do `hospital.sql` | Rode o script **inteiro** (Ctrl+A, F5) |
| `relation "prontosocorro.pacientes" does not exist` | O `hospital.sql` não foi executado | Rode o script no pgAdmin |
| `Non-existent S3 bucket: bronze` | O bucket não foi criado | Crie no console do MinIO e reinicie a task (seção 9.5) |
| `replication slot "..." already exists` | Dois conectores com o mesmo `slot.name`, ou um slot que sobrou | Use outro `slot.name` ou remova o slot antigo (seção 10.3) |
| `wal_level must be logical` | Postgres sem CDC habilitado | Use a imagem `debezium/example-postgres` ou configure `wal_level` |
| `Connector ... not found` (404) | Nome digitado errado | `curl -s http://localhost:8083/connectors` para ver os nomes |
| Tópico não aparece | O conector falhou ou a tabela não está no `schema.include.list` | Veja o `status` do conector |
| Computador muito lento | Pouca memória para o Docker | Dê ao menos 4 GB ao Docker Desktop (Settings → Resources) |
| `port is already allocated` | Outro programa usa a mesma porta | Feche o programa ou mude a porta da esquerda em `ports` |

---

## 13. Glossário

| Termo | Significado |
|---|---|
| **API REST** | Jeito de um programa receber ordens por mensagens HTTP (GET, PUT, POST, DELETE) |
| **Bind mount** | Pasta do seu computador que aparece dentro do container |
| **Bootstrap server** | O endereço "de entrada" do Kafka |
| **Broker** | Um servidor Kafka |
| **Bucket** | A "pasta principal" de um armazenamento S3/MinIO |
| **CDC** (*Change Data Capture*) | Capturar cada mudança de um banco, no momento em que acontece |
| **Consumer group** | Time de consumidores que divide a leitura e guarda a posição |
| **Container** | Uma imagem rodando |
| **Converter** | Define o formato das mensagens no Kafka |
| **Data lake** | Armazenamento barato de arquivos brutos, para análise depois |
| **Docker Compose** | Ferramenta que sobe vários containers a partir de um arquivo YAML |
| **Envelope** | A mensagem completa do Debezium (`before`, `after`, `source`, `op`) |
| **Imagem** | Pacote pronto com o programa e suas dependências |
| **JSON** | Formato de texto com pares `"campo": valor` |
| **KRaft** | Modo novo do Kafka, sem ZooKeeper |
| **Lag** | Quantas mensagens um consumidor ainda não leu |
| **Offset** | Posição de uma mensagem dentro da partição |
| **Partição** | Divisão de um tópico em filas paralelas |
| **Plugin** | "Driver" que ensina o Connect a falar com um sistema |
| **Registry** | Repositório de imagens (Docker Hub, Quay.io, cgr.dev) |
| **Replication slot** | Marcador no Postgres de até onde o leitor do diário chegou |
| **S3** | Padrão de armazenamento de arquivos da Amazon, que o MinIO imita |
| **Sink** | Conector que leva dados do Kafka para fora |
| **SMT** | Transformação simples aplicada em cada mensagem |
| **Snapshot** | A "foto" inicial das tabelas que o Debezium tira ao começar |
| **Source** | Conector que traz dados para o Kafka |
| **Tag** | Versão de uma imagem |
| **Task** | O "trabalhador" de um conector |
| **Tombstone** | Mensagem com valor vazio, que marca uma chave como apagada |
| **Tópico** | Fila de mensagens com nome |
| **Volume** | "HD externo" de um container, para os dados não sumirem |
| **WAL** (*Write-Ahead Log*) | O diário onde o Postgres anota cada mudança antes de aplicá-la |
| **YAML** | Formato de texto com indentação, usado no `docker-compose.yaml` |
