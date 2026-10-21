# Hands-on: Data Ingestion com Airbyte

> **Advanced MBA | Pós-Graduação · Engenharia e Arquitetura de Dados - Big Data**
> Prof. Felipe Yoshimoto · LABDATA-FIA · FIA Business School
> Tema: *Airbyte: Data Ingestion na Modern Data Stack* · Versão: outubro de 2026

Guia passo a passo: do CSV ao Snowflake, passando por Postgres na cloud e Airbyte Cloud.

```mermaid
flowchart LR
    A[CSV-AdventureWorks] --> B[DBeaver-cliente SQL]
    B --> C[(Postgres-Render free tier)]
    C --> D[Airbyte Cloud-Source + Destination]
    D --> E[(Snowflake-strial)]
```

| Etapa | Componentes |
|---|---|
| Preparação da source | CSV → DBeaver → Postgres (Render) |
| Extract + Load | Airbyte Cloud |
| Destination | Snowflake |
| Transform | Próximas aulas |

---

## Sumário

- [Visão geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [1. Signup no Render](#1-signup-no-render)
- [2. Criar um banco Postgres](#2-criar-um-banco-postgres)
- [3. Copiar a connection string](#3-copiar-a-connection-string)
- [4. Conectar com o DBeaver](#4-conectar-com-o-dbeaver)
- [5. Criar o schema adventureworks](#5-criar-o-schema-adventureworks)
- [6. Importar os arquivos CSV](#6-importar-os-arquivos-csv)
- [7. Signup no Airbyte Cloud](#7-signup-no-airbyte-cloud)
- [8. Signup no Snowflake Trial](#8-signup-no-snowflake-trial)
- [9. Adicionar a Source Postgres](#9-adicionar-a-source-postgres)
- [10. Setup SQL no Snowflake](#10-setup-sql-no-snowflake)
- [11. Destination Snowflake e nova Connection](#11-destination-snowflake-e-nova-connection)
- [12. Testar o sync com uma tabela](#12-testar-o-sync-com-uma-tabela)
- [Próximos passos](#próximos-passos)
- [Troubleshooting](#troubleshooting)
- [Apêndice A: Snowflake com Key Pair Authentication](#apêndice-a-snowflake-com-key-pair-authentication)
- [Apêndice B: IPs do Airbyte Cloud (allowlist)](#apêndice-b-ips-do-airbyte-cloud-allowlist)
- [Apêndice C: Limpeza ao final do curso](#apêndice-c-limpeza-ao-final-do-curso)
- [Referências](#referências)

---

## Visão geral

Neste hands-on você vai montar, do zero, um pipeline de Data Ingestion real na Modern Data Stack. Os dados do **AdventureWorks** (empresa fictícia de bicicletas da Microsoft) serão carregados em um banco Postgres na cloud e replicados pelo **Airbyte Cloud** para o data warehouse **Snowflake**.

> **Por que a ordem dos passos 10 e 11?**
> Para configurar o Destination no Airbyte você precisa de warehouse, usuário e senha que ainda não existem. Por isso o setup SQL no Snowflake (passo 10) vem antes de Destination + Connection (passo 11).

> [!NOTE]
> As telas das plataformas mudam com frequência. Se algum botão estiver com outro nome, procure a opção equivalente; os conceitos e os valores dos campos continuam os mesmos.

## Pré-requisitos

- Um e-mail válido (de preferência o mesmo nas três plataformas)
- Navegador atualizado (Chrome, Edge ou Firefox)
- [DBeaver Community](https://dbeaver.io/download/) instalado
- Arquivos CSV do AdventureWorks (disponibilizados pelo professor)
- Cerca de 90 minutos

> [!CAUTION]
> **Nunca versione credenciais.** Guarde host, usuário, senha e Account Identifier em um bloco de notas seguro ou em um arquivo `.env` listado no `.gitignore`.
>
> | Item | Onde anotar |
> |---|---|
> | Postgres Host | local seguro |
> | Postgres Database / User | local seguro |
> | Postgres Password | local seguro |
> | Snowflake Account Identifier | local seguro |
> | Snowflake User / Password | local seguro |

---

## 1. Signup no Render

📍 `dashboard.render.com/register`

**Objetivo:** criar uma conta gratuita na plataforma de cloud que vai hospedar o nosso banco Postgres (a source do pipeline).

1. Acesse [dashboard.render.com/register](https://dashboard.render.com/register).
2. Crie a conta com GitHub, GitLab, Bitbucket ou Google **(1)**, ou com e-mail e senha **(2)**.
3. Clique em **Create Account (3)** e confirme o e-mail recebido.
4. Se pedido, responda ao questionário inicial e crie o workspace (ex.: `Seu Nome's workspace`).

<p align="center">
  <img src="img/01-render-signup.png" alt="Tela de cadastro do Render" width="800">
  <br><sub><b>Figura 1:</b> Tela de cadastro do Render.</sub>
</p>

## 2. Criar um banco Postgres

📍 Render Dashboard → **+ New** → **Postgres**

**Objetivo:** provisionar um Postgres gerenciado, acessível pela internet, para receber os dados do AdventureWorks.

1. No dashboard, clique em **+ New (1)** e escolha **Postgres (2)**.
2. Preencha o formulário conforme a tabela abaixo e clique em **Create Database**.
3. Aguarde o status mudar de *Creating* para **Available** (1 a 3 minutos).

<p align="center">
  <img src="img/02-render-new-postgres.png" alt="Menu + New → Postgres no Render Dashboard" width="800">
  <br><sub><b>Figura 2:</b> Menu + New → Postgres no Render Dashboard.</sub>
</p>

| Campo | Valor sugerido | Observação |
|---|---|---|
| **Name** | `adventureworks` | Nome do serviço no Render. |
| **Database** | `adventureworks` | O Render pode adicionar um sufixo (ex.: `adventureworks_gan8`). |
| **User** | `adventureworks_user` | Também pode receber sufixo. |
| **Region** | `Oregon (US West)` | Qualquer região funciona; os IPs do Airbyte Cloud ficam nos EUA. |
| **PostgreSQL Version** | padrão (mais recente) | Não altere. |
| **Instance Type / Plan** | `Free` | 1 GB de storage: suficiente para o AdventureWorks. |

> [!WARNING]
> **Limites do plano Free**
> - O banco gratuito **expira 30 dias após a criação**. Depois disso há 14 dias de carência para upgrade e, então, o banco e os dados são apagados.
> - Apenas **um** Postgres Free ativo por workspace, sem backups.

> [!TIP]
> **Acesso externo (Inbound IP Rules):** na página do banco, verifique em **Networking / Access Control** se conexões externas estão liberadas (padrão: `0.0.0.0/0`, qualquer IP). Para uma configuração mais segura, restrinja aos IPs do Airbyte Cloud e ao seu IP (lista no [Apêndice B](#apêndice-b-ips-do-airbyte-cloud-allowlist)).

## 3. Copiar a connection string

📍 Render → seu banco → **Info** → **Connections**

**Objetivo:** obter as credenciais que o DBeaver e o Airbyte vão usar para se conectar ao Postgres.

1. Abra o banco criado e role até a seção **Connections**.
2. Em **External Database URL**, clique no ícone de copiar **(1)**.
3. Cole o valor em um local seguro (veja o aviso em [Pré-requisitos](#pré-requisitos)).

<p align="center">
  <img src="img/03-render-external-url.png" alt="External Database URL no Render" width="800">
  <br><sub><b>Figura 3:</b> External Database URL. A senha foi ocultada neste material.</sub>
</p>

### Anatomia da connection string

```text
postgresql://USUARIO:SENHA@HOST:5432/DATABASE

-- exemplo (valores fictícios)
postgresql://adventureworks_gan8_user:Abc123xyz@dpg-xxxxxxxx-a.oregon-postgres.render.com:5432/adventureworks_gan8
```

| Parte | Exemplo | Usado em |
|---|---|---|
| **Host** | `dpg-xxxxxxxx-a.oregon-postgres.render.com` | DBeaver e Airbyte (campo Host) |
| **Port** | `5432` | Se não aparecer na URL, use 5432 |
| **Database** | `adventureworks_gan8` | Depois da última `/` |
| **Username** | `adventureworks_gan8_user` | Entre `//` e `:` |
| **Password** | (entre `:` e `@`) | Nunca publique ou envie por chat |

> [!IMPORTANT]
> **Internal vs. External Database URL:** a **Internal URL** só funciona entre serviços dentro do Render. Para DBeaver e Airbyte Cloud use sempre a **External Database URL**, que exige SSL (`sslmode=require`).

## 4. Conectar com o DBeaver

📍 DBeaver → **Database** → **New Database Connection**

**Objetivo:** acessar o Postgres a partir do seu computador para criar estruturas e carregar dados.

1. No DBeaver, clique em **Database → New Database Connection** (ou no ícone de tomada com +).
2. Selecione **PostgreSQL** e clique em **Next**.
3. Na aba **Main**, mantenha **Connect by: Host** e preencha os campos abaixo.
4. Na aba **SSL**, marque **Use SSL** e escolha **SSL mode: require**.
5. Clique em **Test Connection…**. Se o DBeaver pedir para baixar o driver, aceite (**Download**).
6. Com o teste OK, clique em **Finish**.

| Campo (aba Main) | Valor | Observação |
|---|---|---|
| Host | `dpg-xxxxxxxx-a.oregon-postgres.render.com` | Sem `postgresql://` e sem porta |
| Port | `5432` | |
| Database | `adventureworks_xxxx` | |
| Authentication | Database Native | |
| Username / Password | `adventureworks_xxxx_user` / `••••` | Marque *Save password* se for um computador pessoal |

> [!TIP]
> **Atalho:** em vez de preencher campo a campo, mude **Connect by** para **URL** e use
> `jdbc:postgresql://HOST:5432/DATABASE?sslmode=require`, informando usuário e senha nos campos próprios.

## 5. Criar o schema adventureworks

📍 DBeaver → **SQL Editor**

**Objetivo:** organizar as tabelas do AdventureWorks em um schema próprio, separado do `public`.

1. Clique com o botão direito na conexão → **SQL Editor → Open SQL script** (ou `Ctrl` + `]`).
2. Execute o comando abaixo com `Ctrl` + `Enter`:

```sql
CREATE SCHEMA IF NOT EXISTS adventureworks;

-- conferindo
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name = 'adventureworks';
```

3. No **Database Navigator**, clique com o botão direito em **Schemas → Refresh** (`F5`) para ver o novo schema.

## 6. Importar os arquivos CSV

📍 DBeaver → schema `adventureworks` → **Import Data**

**Objetivo:** carregar todos os CSVs do AdventureWorks como tabelas no schema `adventureworks`.

1. Expanda `adventureworks`, clique com o botão direito em **Tables** (ou no próprio schema) → **Import Data**.
2. Em **Import source**, escolha **CSV** → **Next**.
3. Selecione todos os arquivos `.csv` de uma vez (`Ctrl` + `A` na janela de arquivos). Cada arquivo vira uma tabela.
4. Em **Importer settings**, confira:
   - **Encoding:** `UTF-8` (ou `UTF-16` / `Windows-1252` se os acentos aparecerem estranhos);
   - **Column delimiter:** o separador do arquivo (`,`, `;` ou `Tab`);
   - **Header position:** `top` (a primeira linha tem os nomes das colunas).
5. Em **Tables mapping**, confirme que cada arquivo aponta para uma tabela *new* no schema `adventureworks`. Clique em **Configure** para revisar os tipos das colunas, se necessário.
6. Em **Data load settings**, mantenha **Use transactions** marcado e clique em **Proceed**.
7. Ao final, faça **Refresh** no schema e confira as tabelas com a consulta abaixo.

```sql
-- tabelas importadas e quantidade aproximada de linhas
SELECT relname AS tabela, n_live_tup AS linhas
FROM pg_stat_user_tables
WHERE schemaname = 'adventureworks'
ORDER BY relname;

-- contagem exata de uma tabela (troque o nome)
SELECT COUNT(*) FROM adventureworks.nome_da_tabela;
```

> [!TIP]
> **Recomendado: defina primary keys.** Tabelas importadas de CSV não têm primary key. Sem ela, o Airbyte não oferece o sync mode **Incremental | Append + Deduped**. Para as tabelas principais, rode, por exemplo:
>
> ```sql
> ALTER TABLE adventureworks.nome_da_tabela ADD PRIMARY KEY (coluna_id);
> ```

## 7. Signup no Airbyte Cloud

📍 `cloud.airbyte.com`

**Objetivo:** criar o workspace onde vamos configurar Source, Destination e Connection.

1. Acesse [cloud.airbyte.com/signup](https://cloud.airbyte.com/signup).
2. Cadastre-se com Google, GitHub ou e-mail corporativo e confirme o e-mail.
3. Crie a organização/workspace (ex.: `LABDATA-Hands-on`). Mantenha a data residency padrão (**United States**).
4. Você cai na tela inicial com o menu lateral: **Connections**, **Sources**, **Destinations**.

> [!NOTE]
> **Conceito da aula:** o Airbyte Cloud é a versão gerenciada da plataforma: o Core (Web UI, API Server, Scheduler, Worker) já está rodando para você. Você só configura os **Connectors**. Em Self-Managed, você faria o deploy com Docker ou Kubernetes.

## 8. Signup no Snowflake Trial

📍 `signup.snowflake.com`

**Objetivo:** criar a conta do cloud data warehouse que será o destination do pipeline.

1. Acesse [signup.snowflake.com](https://signup.snowflake.com) e preencha nome, e-mail e empresa.
2. Escolha a edição **Enterprise** (ou Standard), o cloud provider **AWS** e uma região próxima (ex.: *South America (São Paulo)* ou *US East*).
3. Ative a conta pelo link recebido por e-mail e defina o usuário administrador e a senha.
4. Entre no **Snowsight** (interface web do Snowflake).
5. Descubra o **Account Identifier**: clique no seu nome (canto inferior esquerdo) → **Account → View account details**. Copie o *Account identifier* no formato `ORGNAME-ACCOUNTNAME` (ex.: `QHOOJHG-WB63749`).

> [!NOTE]
> **Por que a conta Trial facilita o lab:** o Snowflake está descontinuando o login só com senha (single-factor) para usuários comuns e de serviço. Contas Trial continuam aceitando usuário e senha, por isso podemos usar esse método aqui. Em contas de produção, use Key Pair ([Apêndice A](#apêndice-a-snowflake-com-key-pair-authentication)).

## 9. Adicionar a Source Postgres

📍 Airbyte → **Sources** → **+ New source** → **Postgres**

**Objetivo:** configurar o Source Connector que vai extrair os dados do Postgres no Render.

1. No menu lateral, clique em **Sources → + New source** e busque **Postgres**.
2. Preencha os campos conforme a tabela abaixo (destaques **(1)** a **(3)** na figura).
3. Clique em **Set up source**. O Airbyte testa a conexão; aguarde a mensagem *"All connection tests passed!"*.

<p align="center">
  <img src="img/09-airbyte-source-postgres.png" alt="Source Postgres no Airbyte Cloud" width="800">
  <br><sub><b>Figura 4:</b> Source Postgres no Airbyte Cloud. À direita, o Setup Guide do connector.</sub>
</p>

| Campo | Valor | Observação |
|---|---|---|
| **Source name** | `Postgres AdventureWorks` | Nome livre, para identificar a source. |
| **Host (1)** | `dpg-xxxxxxxx-a.oregon-postgres.render.com` | Somente o hostname: sem `postgresql://`, sem porta. |
| **Port (2)** | `5432` | |
| **Database Name (3)** | `adventureworks_xxxx` | Exatamente como na connection string. |
| **Schemas** | `adventureworks` | Case-sensitive. Remova `public` para listar só nossas tabelas. |
| **Username** | `adventureworks_xxxx_user` | Ou o usuário read-only (dica abaixo). |
| **Password** | `••••••••` | Fica armazenada de forma criptografada no Airbyte. |
| **SSL Mode** | `require` | O Render exige SSL nas conexões externas. |
| **SSH Tunnel Method** | `No Tunnel` | O banco já é acessível pela internet. |
| **Update Method** | `Standard (xmin)` | Pode aparecer como *Detect Changes with Xmin System Column*. CDC exige logical replication, que não usaremos. |
| **Opções avançadas** | padrão | JDBC URL Params, Checkpoint e Max Concurrent Queries: não altere. |

> [!TIP]
> **Boa prática: usuário read-only dedicado.** Em produção, o Airbyte deve ler a source com um usuário com o mínimo de privilégios. No DBeaver, conectado com o usuário principal:
>
> ```sql
> CREATE USER airbyte_reader PASSWORD 'UmaSenhaForte#2026';
> GRANT USAGE ON SCHEMA adventureworks TO airbyte_reader;
> GRANT SELECT ON ALL TABLES IN SCHEMA adventureworks TO airbyte_reader;
> ALTER DEFAULT PRIVILEGES IN SCHEMA adventureworks GRANT SELECT ON TABLES TO airbyte_reader;
> ```

> [!NOTE]
> **Como o xmin funciona:** todo registro no Postgres tem a coluna de sistema `xmin` (o ID da transação que o gravou). O Airbyte guarda o maior `xmin` lido no *state* e, no sync seguinte, busca só o que é mais novo: Incremental Data Loading sem precisar de uma coluna `updated_at`. **Limitação:** o `xmin` não captura deletes; para isso, use CDC.

## 10. Setup SQL no Snowflake

📍 Snowsight → **Projects** → **Workspaces / Worksheets** → **+ SQL File**

**Objetivo:** criar warehouse, database e um usuário com senha para o Airbyte, concedendo a role `ACCOUNTADMIN`.

1. No Snowsight, abra um novo SQL Worksheet.
2. Cole o script abaixo, **troque a senha** e execute tudo (**Run All**, ou `Ctrl` + `Shift` + `Enter`).
3. Confira o resultado do `SHOW USERS` no final.

```sql
USE ROLE ACCOUNTADMIN;

-- 1. Warehouse (compute): pequeno, desliga sozinho após 60s ocioso
CREATE WAREHOUSE IF NOT EXISTS AIRBYTE_WAREHOUSE
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

-- 2. Database de destino (o Airbyte cria os schemas dentro dele)
CREATE DATABASE IF NOT EXISTS AIRBYTE_DATABASE;

-- 3. Usuário do Airbyte com senha (troque por uma senha forte)
CREATE USER IF NOT EXISTS AIRBYTE_USER
  PASSWORD = 'TroqueEstaSenha#2026!'
  DEFAULT_ROLE = ACCOUNTADMIN
  DEFAULT_WAREHOUSE = AIRBYTE_WAREHOUSE
  MUST_CHANGE_PASSWORD = FALSE;

-- 4. Concede a role ACCOUNTADMIN ao novo usuário
GRANT ROLE ACCOUNTADMIN TO USER AIRBYTE_USER;

-- 5. Conferência
SHOW USERS LIKE 'AIRBYTE_USER';
SHOW GRANTS TO USER AIRBYTE_USER;
```

> [!WARNING]
> **ACCOUNTADMIN é só para o laboratório.** É a role mais poderosa da conta; usamos aqui para simplificar. Em produção, aplique **RBAC** e o princípio do menor privilégio: crie uma `AIRBYTE_ROLE` com `USAGE` no warehouse e `OWNERSHIP` / `CREATE SCHEMA` apenas no database de destino (é o script recomendado na documentação do Airbyte).

> [!TIP]
> **Senha:** use pelo menos 14 caracteres, com maiúsculas, minúsculas, números e caractere especial. Se o Snowflake recusar a senha, a mensagem informa a política exigida.

## 11. Destination Snowflake e nova Connection

📍 Airbyte → **Destinations** → **+ New destination** → **Snowflake**

**Objetivo:** configurar o **Destination Connector** e ligar Source → Destination em uma **Connection**.

### 11.1 Destination Snowflake

1. Clique em **Destinations → + New destination** e busque **Snowflake**.
2. Preencha os campos da tabela a seguir: Host **(1)** e Role **(2)** na figura.
3. Clique em **Set up destination** e aguarde os testes passarem.

<p align="center">
  <img src="img/11-airbyte-destination-snowflake.png" alt="Destination Snowflake no Airbyte Cloud" width="800">
  <br><sub><b>Figura 5:</b> Destination Snowflake. O destaque (3) mostra o aviso de descontinuidade do método Username and Password.</sub>
</p>

| Campo | Valor | Observação |
|---|---|---|
| **Destination name** | `Snowflake` | Nome livre. |
| **Host (1)** | `ORGNAME-ACCOUNTNAME.snowflakecomputing.com` | Account Identifier + `.snowflakecomputing.com`, sem `https://`. |
| **Role (2)** | `ACCOUNTADMIN` | Em maiúsculas, como no script. |
| **Warehouse** | `AIRBYTE_WAREHOUSE` | |
| **Database** | `AIRBYTE_DATABASE` | Precisa existir (criado no passo 10). |
| **Default Schema** | `ADVENTUREWORKS` | O Airbyte cria o schema se ele não existir. |
| **Username** | `AIRBYTE_USER` | |
| **Authorization Method** | `Username and Password` | Se não aparecer, use Key Pair Authentication ([Apêndice A](#apêndice-a-snowflake-com-key-pair-authentication)). |
| **Password** | `••••••••` | A senha definida no passo 10. |
| **Opções avançadas** | padrão | JDBC URL Params vazio; raw tables no schema `airbyte_internal`; Data Retention = 1 dia. |

> [!WARNING]
> **Username and Password está deprecated no connector.** Desde a versão 5.0.0 do Snowflake destination, esse método está deprecated e será removido em uma versão futura (destaque **3** na Figura 5). **Key Pair Authentication** ou **Programmatic Access Token** são os métodos recomendados. Se a sua tela não oferecer mais a opção de senha, siga o [Apêndice A](#apêndice-a-snowflake-com-key-pair-authentication).

### 11.2 Nova Connection

1. Clique em **Connections → + New connection**.
2. **Define source:** escolha a source existente *Postgres AdventureWorks*.
3. **Define destination:** escolha a destination existente *Snowflake*.
4. **Select streams:** o Airbyte lista as tabelas do schema `adventureworks`. Para o teste do passo 12, ative **apenas uma tabela** (de preferência uma pequena).
5. Escolha o sync mode do stream e clique em **Next**.
6. Em **Configure connection**, preencha a tabela abaixo e clique em **Finish & Sync** (ou **Set up connection**).

| Campo | Valor | Observação |
|---|---|---|
| **Sync mode** | `Full Refresh \| Overwrite` | Funciona sem primary key. Com PK definida (passo 6), prefira `Incremental \| Append + Deduped`. |
| **Connection name** | `Postgres → Snowflake (AdventureWorks)` | |
| **Schedule type** | `Manual` | Para o teste. Depois mude para *Scheduled* (ex.: a cada 24 horas) ou *Cron*. |
| **Destination Namespace** | `Destination default` | Usa o Default Schema (`ADVENTUREWORKS`). *Mirror source structure* também funciona com ACCOUNTADMIN. |
| **Stream prefix** | (vazio) | Opcional, ex.: `raw_`. |
| **Schema changes** | `Propagate field changes only` | Mantém o padrão: novas colunas da source chegam ao destination (Schema Management). |
| **Notifications** | Failed syncs: e-mail | Logging & Alerts: você é avisado antes do usuário de negócio. |

## 12. Testar o sync com uma tabela

📍 Airbyte → **Connections** → sua connection

**Objetivo:** executar o primeiro sync e validar que os dados chegaram íntegros ao Snowflake.

1. Na connection, clique em **Sync now**.
2. Acompanhe em **Timeline / Job history**: o status passa de *Running* para *Succeeded*.
3. Abra os logs do job e anote quantos registros foram *extracted* e *loaded*.
4. No Snowsight, valide os dados com o script abaixo, trocando `NOME_DA_TABELA`.
5. Compare o `COUNT(*)` do Snowflake com o do Postgres (passo 6). Os números devem ser iguais.

```sql
USE WAREHOUSE AIRBYTE_WAREHOUSE;
USE DATABASE AIRBYTE_DATABASE;

-- schemas criados pelo Airbyte: ADVENTUREWORKS (final) e AIRBYTE_INTERNAL (raw)
SHOW SCHEMAS IN DATABASE AIRBYTE_DATABASE;
SHOW TABLES IN SCHEMA AIRBYTE_DATABASE.ADVENTUREWORKS;

-- contagem e amostra (no Snowflake, os nomes ficam em MAIÚSCULAS)
SELECT COUNT(*) FROM ADVENTUREWORKS.NOME_DA_TABELA;
SELECT * FROM ADVENTUREWORKS.NOME_DA_TABELA LIMIT 10;

-- metadados de ingestão adicionados pelo Airbyte
SELECT _AIRBYTE_RAW_ID, _AIRBYTE_EXTRACTED_AT, _AIRBYTE_META
FROM ADVENTUREWORKS.NOME_DA_TABELA
LIMIT 5;
```

**O que observar**

- **Final table** (schema `ADVENTUREWORKS`): colunas tipadas, prontas para análise.
- **Raw table** (schema `AIRBYTE_INTERNAL`): o registro original em JSON, usado pelo Airbyte para typing e deduping.
- **`_AIRBYTE_EXTRACTED_AT`**: quando o dado foi extraído. Útil para auditoria e reliability.

---

## Próximos passos

- [ ] Volte à connection → **Schema** e ative os demais streams do AdventureWorks.
- [ ] Rode um novo sync e valide as contagens tabela a tabela.
- [ ] Insira ou altere uma linha no Postgres e rode o sync de novo: observe o comportamento do sync mode escolhido.
- [ ] Mude o Schedule type para *Scheduled* (a cada 24 horas).

### Checklist de boas práticas do lab

- **Incremental sempre que possível:** menos volume, mais consistência (State Management).
- **Alertas configurados** para failed syncs (Error Handling & Monitoring).
- **Credenciais seguras:** nunca em prints, chats ou repositórios; usuários dedicados e menor privilégio (Security).

## Troubleshooting

| Sintoma | Causa provável e solução |
|---|---|
| `Connection timed out` / `refused` | Uso da Internal URL ou IP bloqueado. Use o host da External URL e confira as Inbound IP Rules ([Apêndice B](#apêndice-b-ips-do-airbyte-cloud-allowlist)). |
| `SSL connection is required` | Defina **SSL Mode = require** no Airbyte e **Use SSL** no DBeaver. |
| `password authentication failed` | Senha copiada com espaço ou caractere a mais. Copie de novo da External URL. |
| Nenhum stream aparece na Connection | Campo **Schemas** da source sem `adventureworks` ou tabelas criadas em `public`. |
| Acentos estranhos nos dados | Encoding errado na importação. Reimporte com `UTF-8` ou `Windows-1252`. |
| Snowflake: `Incorrect username or password` | Usuário/senha em maiúsculas/minúsculas diferentes ou senha não trocada no script. Teste o login do `AIRBYTE_USER` no Snowsight. |
| Snowflake: `Insufficient privileges` / schema `PUBLIC` | Role errada. Confira `ACCOUNTADMIN` e use *Destination default* no namespace. |
| Sem opção *Append + Deduped* | A tabela não tem primary key. Crie a PK no Postgres (passo 6) e faça **Refresh source schema**. |
| Banco Render inacessível após semanas | O plano Free expira em 30 dias. Crie um novo banco ou faça upgrade. |

---

## Apêndice A: Snowflake com Key Pair Authentication

Use este caminho se o Airbyte não oferecer *Username and Password* ou em contas que não sejam Trial. Ele substitui a senha por um par de chaves RSA.

### A.1 Gerar as chaves (terminal: Linux, macOS ou Git Bash no Windows)

```bash
# chave privada (formato PKCS#8, sem passphrase, para o lab)
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt

# chave pública derivada da privada
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

### A.2 Registrar a chave pública no usuário (Snowsight)

```sql
-- cole o conteúdo de rsa_key.pub SEM as linhas BEGIN/END e sem quebras de linha
ALTER USER AIRBYTE_USER SET RSA_PUBLIC_KEY = 'MIIBIjANBgkqh...';

-- conferência: o campo RSA_PUBLIC_KEY_FP deve estar preenchido
DESC USER AIRBYTE_USER;
```

### A.3 No Destination Snowflake do Airbyte

- **Authorization Method:** Key Pair Authentication
- **Private Key:** todo o conteúdo de `rsa_key.p8`, incluindo as linhas `-----BEGIN PRIVATE KEY-----` e `-----END PRIVATE KEY-----`
- **Passphrase:** vazio (a chave foi gerada com `-nocrypt`)

> [!CAUTION]
> **Proteja a chave privada.** O arquivo `rsa_key.p8` é equivalente a uma senha. Não envie por chat, **não suba para o GitHub** (adicione `*.p8` e `*.pub` ao `.gitignore`) e apague-o ao final do curso. Em produção, gere a chave com passphrase (`-v2 aes-256-cbc` no lugar de `-nocrypt`).

## Apêndice B: IPs do Airbyte Cloud (allowlist)

Se você restringir as Inbound IP Rules do Render, libere os IPs de saída do Airbyte Cloud (workspaces nos EUA, região padrão) e também o seu IP, para o DBeaver continuar funcionando.

| Região (GCP) | Endereços |
|---|---|
| `us-west-3` | `34.106.109.131` · `34.106.196.165` · `34.106.60.246` · `34.106.229.69` · `34.106.127.139` · `34.106.218.58` · `34.106.115.240` · `34.106.225.141` |
| `us-central-1` | `34.33.7.0/29` |

> Fonte: [docs.airbyte.com/platform/operating-airbyte/ip-allowlist](https://docs.airbyte.com/platform/operating-airbyte/ip-allowlist) (consultado em outubro de 2026). A lista pode mudar; confira a página antes de aplicar regras em produção.

## Apêndice C: Limpeza ao final do curso

- [ ] **Airbyte:** pause ou apague a connection para evitar syncs agendados.
- [ ] **Snowflake:** `ALTER WAREHOUSE AIRBYTE_WAREHOUSE SUSPEND;` (o trial tem créditos limitados).
- [ ] **Snowflake:** `DROP USER AIRBYTE_USER;` quando não for mais usar.
- [ ] **Render:** apague o banco em **Settings → Delete Database** (ou deixe expirar).
- [ ] Apague arquivos locais com credenciais e chaves (`rsa_key.p8`).

## Referências

- Airbyte. [Postgres source connector](https://docs.airbyte.com/integrations/sources/postgres)
- Airbyte. [Snowflake destination connector](https://docs.airbyte.com/integrations/destinations/snowflake)
- Airbyte. [IP allow list for Cloud](https://docs.airbyte.com/platform/operating-airbyte/ip-allowlist)
- Render. [Deploy for Free (limites do Postgres Free)](https://render.com/docs/free)
- Render. [Inbound IP Rules](https://render.com/docs/inbound-ip-rules)
- Snowflake. [Planning for the deprecation of single-factor password sign-ins](https://docs.snowflake.com/en/user-guide/security-mfa-rollout)

---

<sub>© FIA LABDATA. Todos os direitos reservados. · Hands-on: Data Ingestion com Airbyte</sub>
