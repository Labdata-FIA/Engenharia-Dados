# FIAShop — Guia de consulta

Este guia é o material de **consulta** do projeto FIAShop. O [README.md](README.md) segue a ordem da aula, passo a passo. Aqui o conteúdo está organizado por assunto, para você voltar quando precisar lembrar:

- **o que é** cada conceito;
- **o que fizemos** no projeto e por quê;
- **o que cada comando faz, por que usar e quando usar.**

---

## Sumário

1. [Conceitos básicos](#1-conceitos-básicos)
   - [Git e GitHub](#11-git-e-github)
   - [Docker](#12-docker)
   - [Docker Compose](#13-docker-compose)
   - [API e FastAPI](#14-api-e-fastapi)
   - [Dados: MinIO, buckets e camadas](#15-dados-minio-buckets-e-camadas)
2. [O que construímos](#2-o-que-construímos)
3. [Comandos de Git](#3-comandos-de-git)
4. [Comandos de Docker](#4-comandos-de-docker)
5. [Comandos de Docker Compose](#5-comandos-de-docker-compose)
6. [Publicar uma imagem no Docker Hub](#6-publicar-uma-imagem-no-docker-hub)
7. [Referência do docker-compose.yml](#7-referência-do-docker-composeyml)
8. [Referência do Dockerfile](#8-referência-do-dockerfile)
9. [Comandos do sistema (Windows, Mac, Linux)](#9-comandos-do-sistema-windows-mac-linux)
10. [Problemas comuns](#10-problemas-comuns)

---

## 1. Conceitos básicos

### 1.1 Git e GitHub

| Conceito | O que é | Por que importa |
|---|---|---|
| **Git** | Programa que guarda o histórico de um projeto na sua máquina | Permite voltar versões, saber quem mudou o quê e trabalhar em equipe sem sobrescrever o trabalho dos outros |
| **GitHub** | Site que guarda uma cópia do repositório na nuvem | É onde o time compartilha o código, revisa mudanças e mantém um backup |
| **Repositório (repo)** | A pasta do projeto acompanhada pelo Git, com todo o histórico | É a "unidade" do projeto: tudo o que importa fica dentro dele |
| **Commit** | Uma "foto" do projeto num momento, com uma mensagem | Cria pontos para onde você pode voltar e documenta o que mudou |
| **Área de preparação (staging)** | Onde ficam as mudanças escolhidas para o próximo commit | Permite commitar só parte do que mudou, mantendo cada commit com um assunto só |
| **Branch** | Uma linha paralela do histórico | Permite trabalhar numa novidade sem mexer na versão estável |
| **`main`** | A branch principal, com a versão que funciona | É dela que o time e os processos automáticos partem. Nunca deve receber código pela metade |
| **Merge** | Juntar os commits de uma branch em outra | É como uma feature pronta entra na `main` |
| **Pull Request (PR)** | Um pedido, no GitHub, para fazer o merge de uma branch | Cria um momento de revisão: um colega olha o código antes de ele entrar na `main` |
| **Conflito** | Quando duas branches mudam a mesma linha | O Git não decide sozinho e pede que uma pessoa escolha qual versão fica |
| **`origin`** | O nome padrão do repositório remoto (o GitHub) | Aparece em comandos como `git push -u origin <branch>` |
| **`.gitignore`** | Lista de arquivos que o Git deve ignorar | Impede que senhas e arquivos gerados automaticamente vão para o GitHub |

O caminho de uma mudança:

```
Pasta de trabalho  --git add-->  Área de preparação  --git commit-->  Histórico local  --git push-->  GitHub
                                                                      Histórico local  <--git pull--  GitHub
```

### 1.2 Docker

**Por que Docker:** sem ele, cada pessoa instala Python, bibliotecas e serviços na própria máquina, cada um numa versão, e surge o "na minha máquina funciona". Com Docker, o programa vem empacotado com tudo de que precisa e roda igual em qualquer computador.

| Conceito | O que é | Analogia: curso de MBA |
|---|---|---|
| **Imagem** | Pacote somente leitura com sistema, bibliotecas e código. É o molde | A ementa da disciplina |
| **Container** | Uma imagem em execução. Nasce, roda, para e pode ser removido | Cada turma em andamento com aquela ementa |
| **Porta** | Liga uma porta da sua máquina a uma porta do container (`HOST:CONTAINER`) | O número da sala |
| **Volume** | Armazenamento fora do container; os dados sobrevivem a ele | A secretaria: a turma acaba, as notas ficam |
| **Network** | Rede privada onde os containers se encontram pelo nome do serviço | O grupo dos professores: um chama o outro pelo nome |

Outros termos:

| Conceito | O que é | Por que importa |
|---|---|---|
| **Imagem ≠ container** | Uma imagem gera vários containers; apagar um container não apaga a imagem | É a base para entender todo o resto |
| **Registry (registro)** | Servidor que guarda imagens para download: Docker Hub, `quay.io`, `cgr.dev` | É de onde vêm as imagens prontas. Se o dono parar de distribuir, o download quebra (foi o que aconteceu com o MinIO) |
| **Tag** | A versão de uma imagem, depois dos dois-pontos: `python:3.12-slim` | Com a tag fixa, todos rodam exatamente a mesma versão |
| **`latest`** | Tag que aponta para a versão mais recente | Prático, mas muda com o tempo. Evite em projetos que precisam ser reproduzíveis |
| **Dockerfile** | A receita para construir uma imagem | É como o **seu** código vira uma imagem |
| **Volume nomeado** | Volume criado e gerenciado pelo Docker (`minio_storage:/data`) | Padrão para **dados** que precisam sobreviver |
| **Bind mount** | Uma pasta da sua máquina montada no container (`./api:/app`) | Padrão para **código** em desenvolvimento: você edita e o container vê na hora |
| **Entrypoint** | O programa principal de uma imagem | O `command:` do compose vira os argumentos desse programa |
| **`localhost`** | "Esta máquina" | **Dentro de um container, `localhost` é o próprio container**, e não a sua máquina |

### 1.3 Docker Compose

| Conceito | O que é | Por que importa |
|---|---|---|
| **Docker Compose** | Ferramenta que sobe vários containers a partir de um arquivo | Substitui vários `docker run` longos por um único `docker compose up -d` |
| **`docker-compose.yml`** | O arquivo que descreve os serviços, portas, volumes e redes | Vai para o Git: o time inteiro sobe o mesmo ambiente |
| **Serviço** | Cada item dentro de `services:`; vira um container | Cada parte da aplicação (MinIO, API) é um serviço |
| **Nome do serviço** | A chave do serviço no YAML (`minio`, `fiashop-api`) | Dentro da rede, é o endereço que os outros containers usam: `http://minio:9000` |
| **Projeto** | O conjunto de serviços de um `docker-compose.yml` | O Docker usa o nome da pasta como prefixo: o volume `minio_storage` vira `fiashop_minio_storage` |
| **`.env`** | Arquivo com os valores das variáveis (`MINIO_ROOT_PASSWORD=...`) | Tira as senhas do `docker-compose.yml`. **Nunca vai para o GitHub** |
| **`.env.example`** | Modelo do `.env`, sem os valores reais | Vai para o GitHub e mostra ao time quais variáveis criar |
| **`${VARIAVEL}`** | Marcação no YAML que o Compose troca pelo valor do `.env` | É assim que o compose usa uma senha sem escrevê-la |

### 1.4 API e FastAPI

| Conceito | O que é | Por que importa |
|---|---|---|
| **API** | Um programa que recebe pedidos pela rede e responde | É a porta de entrada dos dados: sistemas enviam pedidos para ela |
| **Endpoint (rota)** | Um endereço da API, como `/pedidos` | Cada rota faz uma coisa |
| **GET / POST** | Métodos HTTP: GET busca dados, POST envia dados | O pedido da FIAShop chega por POST |
| **FastAPI** | Framework Python para criar APIs | Valida os dados automaticamente e gera a documentação sozinho |
| **Pydantic / `BaseModel`** | A forma de definir o "contrato" dos dados (campos e tipos) | Recusa dados fora do formato antes de chegarem à bronze |
| **Uvicorn** | O servidor que mantém a API rodando e escutando numa porta | A FastAPI define as rotas; o Uvicorn as coloca no ar |
| **Swagger (`/docs`)** | Página de testes gerada automaticamente pela FastAPI | Permite testar a API pelo navegador, igual em qualquer sistema |
| **Status 201** | "Criado": o pedido foi recebido e gravado | Resposta de sucesso do `POST /pedidos` |
| **Status 422** | "Dados inválidos": falta campo ou o tipo está errado | A validação funcionando |
| **Status 500** | "Erro no servidor": algo quebrou dentro da API | Hora de olhar os logs (`docker compose logs fiashop-api`) |

### 1.5 Dados: MinIO, buckets e camadas

| Conceito | O que é | Por que importa |
|---|---|---|
| **S3** | O serviço de armazenamento de arquivos da AWS | É o padrão de mercado para data lakes |
| **MinIO** | Armazenamento compatível com S3 que roda localmente | Permite praticar com S3 sem conta na AWS. O mesmo código funciona nos dois |
| **Bucket** | A "pasta principal" do S3/MinIO | Cada camada do data lake costuma ser um bucket: `bronze`, `silver`, `gold` |
| **Objeto / Key** | Um arquivo dentro do bucket e o caminho dele | `pedidos/data_ingestao=2026-10-08/pedido_1_143005.json` é a key |
| **`boto3`** | A biblioteca Python oficial da AWS para S3 | Trocando o `endpoint_url`, fala com o MinIO ou com o S3 de verdade |
| **Ingestão** | Trazer o dado da fonte para o data lake | É o que o `ingestao.py` faz |
| **Particionamento** | Separar os arquivos em pastas por um valor, no formato `coluna=valor` | Ferramentas como Spark, DuckDB e Athena leem só a pasta de interesse, por exemplo um dia |

**Arquitetura medalhão:**

| Camada | O que guarda | Na FIAShop |
|---|---|---|
| **Bronze** | O dado como chegou, sem tratamento, mais a data de chegada | Um JSON por pedido (**feito no projeto**) |
| **Silver** | Dado limpo, tipado, sem duplicatas, em formato analítico (Parquet) | Os pedidos do dia num Parquet, com `valor_total` |
| **Gold** | Dado agregado, pronto para o negócio | Faturamento por produto por dia |

**Por que separar em camadas:** se a regra da Silver estiver errada, você corrige e reprocessa a partir da Bronze, que guarda o dado original.

---

## 2. O que construímos

### 2.1 O case

A FIAShop recebe pedidos o dia inteiro, e eles se perdiam em planilhas atualizadas à mão. A missão foi garantir que **todo pedido seja guardado, do jeito que chegou, num lugar central e confiável**: a camada bronze.

### 2.2 A arquitetura

```
 SUA MÁQUINA                         REDE rede_fia (dentro do Docker)
┌──────────────────┐               ┌───────────────────────────────────────────────────────┐
│ Navegador        │  porta 8000   │  ┌─────────────────────┐  minio:9000  ┌─────────────┐ │
│ curl / Swagger   │──────────────►│  │ fiashop-api         │─────────────►│ minio       │ │
│                  │               │  │ main.py  (recebe)   │              │ bucket      │ │
│                  │               │  │ ingestao.py (grava) │              │ bronze      │ │
│                  │               │  └─────────────────────┘              └─────────────┘ │
│                  │  porta 9001   │                                              ▲        │
│                  │──────────────────────── console do MinIO ───────────────────┘        │
└──────────────────┘               └───────────────────────────────────────────────────────┘
```

O caminho de um pedido:

```
POST /pedidos  →  main.py valida  →  ingestao.py grava  →  MinIO: bronze/pedidos/data_ingestao=AAAA-MM-DD/pedido_<id>_<hora>.json
```

**Regra de ouro:** de fora do Docker, use `localhost` + a porta publicada. De dentro (um container falando com outro), use o nome do serviço: `http://minio:9000`.

### 2.3 Os arquivos e o papel de cada um

| Arquivo | Para que serve | Vai para o Git? |
|---|---|---|
| `docker-compose.yml` | Descreve os serviços `minio` e `fiashop-api`, a rede e o volume | Sim |
| `.env` | Usuário e senha do MinIO | **Não** (está no `.gitignore`) |
| `.env.example` | Modelo do `.env`, sem a senha real | Sim |
| `.gitignore` | Lista do que o Git ignora | Sim |
| `README.md` | Roteiro da aula | Sim |
| `GUIA-COMPLETO.md` | Este guia de consulta | Sim |
| `api/Dockerfile` | Receita da imagem da API | Sim |
| `api/requirements.txt` | Bibliotecas Python com versão fixa: `fastapi`, `uvicorn`, `boto3` | Sim |
| `api/main.py` | A API: recebe, valida e repassa o pedido | Sim |
| `api/ingestao.py` | Cria o bucket se precisar e grava o pedido na bronze | Sim |

### 2.4 O `.gitignore`, linha por linha

| Linha | De onde vem esse arquivo | Por que ignorar |
|---|---|---|
| `.env` | Você cria a partir do `.env.example` | Guarda as **senhas**. É o mais importante da lista |
| `__pycache__/`, `*.py[cod]` | O Python cria sozinho ao rodar o código | É recriado toda vez e só gera conflito |
| `.venv/`, `venv/` | O comando `python -m venv`, se alguém rodar Python fora do Docker | Pode ter centenas de MB e só funciona naquele computador |
| `.DS_Store` | O Finder do Mac | Não tem relação com o projeto |
| `.vscode/`, `.idea/` | O VS Code e o PyCharm | Preferências pessoais do editor |

> Crie o `.gitignore` **antes** do primeiro commit com arquivos sensíveis. Ele não protege o que já foi commitado.

### 2.5 As decisões do projeto e o porquê

| Decisão | Por quê |
|---|---|
| **Imagem `cgr.dev/chainguard/minio:latest`** em vez de `quay.io/minio/minio` | As imagens oficiais do MinIO deixaram de ser públicas, e o download passou a falhar com `401 UNAUTHORIZED`. A Chainguard publica o MinIO compilado a partir do código aberto. Na versão gratuita, só existe a tag `latest` |
| **`user: root` no MinIO** | A imagem da Chainguard roda com um usuário sem privilégios, que não consegue gravar no volume novo. O `root` evita o erro de permissão |
| **Sem o serviço `mc`** | A imagem do `mc` também ficou indisponível. O bucket passou a ser criado pelo próprio `ingestao.py`, na função `garantir_bucket()` |
| **Senha só no `.env` da raiz** | Um lugar só para cada segredo. O caminho até o código é `.env` → `environment:` do compose → container → `os.environ` |
| **`os.environ[...]` para senhas e `os.getenv(..., padrão)` para o resto** | Senha sem valor padrão: se faltar, a API para com `KeyError` em vez de rodar com uma senha escrita no código |
| **Validação com `BaseModel`** | Dado fora do formato é recusado com erro 422 antes de chegar à bronze |
| **Pasta `data_ingestao=AAAA-MM-DD`** | Particionamento por dia, o mesmo padrão `coluna=valor` da Aula 7 de Python |
| **Bind mount `./api:/app` + `--reload`** | Durante o desenvolvimento, você edita no VS Code e a API recarrega sozinha |
| **Versões fixas no `requirements.txt`** | Todos instalam exatamente as mesmas bibliotecas, hoje e daqui a meses |

### 2.6 O código, em resumo

**`api/main.py`:**

```python
class Pedido(BaseModel):
    id_pedido: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: float

@app.post("/pedidos", status_code=201)
def receber_pedido(pedido: Pedido):
    caminho = salvar_na_bronze(pedido.model_dump())
    return {"status": "pedido recebido", "arquivo_na_bronze": caminho}
```

| Trecho | O que faz |
|---|---|
| `class Pedido(BaseModel)` | Define o contrato do pedido; a FastAPI recusa o que estiver fora dele (422) |
| `@app.post("/pedidos", status_code=201)` | Cria a rota que recebe os pedidos e responde "criado" |
| `pedido.model_dump()` | Converte o pedido num dicionário Python comum |
| `salvar_na_bronze(...)` | Delega a gravação para o `ingestao.py` |

**`api/ingestao.py`:**

```python
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")   # não é segredo
BUCKET_BRONZE = os.getenv("BUCKET_BRONZE", "bronze")
MINIO_USER = os.environ["MINIO_ROOT_USER"]                           # segredo: sem valor padrão
MINIO_PASSWORD = os.environ["MINIO_ROOT_PASSWORD"]

def garantir_bucket():
    nomes = [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]
    if BUCKET_BRONZE not in nomes:
        s3.create_bucket(Bucket=BUCKET_BRONZE)

def salvar_na_bronze(pedido):
    garantir_bucket()
    agora = datetime.now()
    pedido["recebido_em"] = agora.strftime("%Y-%m-%dT%H:%M:%S")
    caminho = f"pedidos/data_ingestao={agora:%Y-%m-%d}/pedido_{pedido['id_pedido']}_{agora:%H%M%S}.json"
    s3.put_object(Bucket=BUCKET_BRONZE, Key=caminho, Body=json.dumps(pedido, ensure_ascii=False, indent=2).encode("utf-8"))
```

| Trecho | O que faz |
|---|---|
| `os.getenv("NOME", "padrão")` | Lê uma configuração que não é segredo, com valor padrão |
| `os.environ["NOME"]` | Lê um segredo; se não existir, para com `KeyError` |
| `boto3.client("s3", endpoint_url=...)` | Cria o cliente S3 apontando para o MinIO |
| `garantir_bucket()` | Cria o bucket `bronze` só se ele ainda não existir |
| `pedido["recebido_em"]` | Registra quando o pedido chegou |
| `json.dumps(...)` | Converte o pedido em texto JSON (mesmo `json` da Aula 6) |
| `s3.put_object(...)` | Grava o arquivo no bucket |
| `if __name__ == "__main__":` | Permite rodar o script sozinho para teste (grava o pedido 999) |

---

## 3. Comandos de Git

### 3.1 Configuração (uma vez por computador)

| Comando | O que faz | Por que usar | Quando usar |
|---|---|---|---|
| `git config --global user.name "Nome"` | Grava o nome do autor dos commits | Sem isso, o Git não deixa commitar | Na primeira vez que usa Git no computador |
| `git config --global user.email "email"` | Grava o e-mail do autor | O GitHub liga os commits ao seu perfil pelo e-mail | Idem |
| `git config --global init.defaultBranch main` | Define `main` como branch inicial de repositórios novos | É o padrão do GitHub | Idem |
| `git config --global core.autocrlf true` | (Windows) Converte as quebras de linha ao commitar e ao baixar | Evita que arquivos apareçam "todo modificados" entre Windows e Mac/Linux | Idem, no Windows |
| `git config --global core.autocrlf input` | (Mac/Linux) Converte as quebras de linha só ao commitar | Idem | Idem, no Mac e no Linux |
| `git config --list` | Mostra as configurações gravadas | Para conferir nome, e-mail e ajustes | Depois de configurar, ou quando algo parece errado |
| `gh auth login` | Faz login no GitHub pelo navegador | O GitHub não aceita mais a senha da conta no terminal | Antes do primeiro `git push` (Mac/Linux; no Windows, opcional) |
| `gh auth status` | Mostra se você está logado e com qual conta | Confirma o login | Quando o `push` for recusado |

### 3.2 Dia a dia

| Comando | O que faz | Por que usar | Quando usar |
|---|---|---|---|
| `git clone <url>` | Baixa um repositório do GitHub, com todo o histórico | É como você começa a trabalhar num projeto que já existe | Uma vez, no início |
| `git status` | Mostra o que mudou e o que está preparado | Evita commitar algo sem querer | **Antes de qualquer `add` ou `commit`** |
| `git diff` | Mostra linha a linha o que mudou | Para revisar o que você fez | Antes do `add` |
| `git add <arquivo>` | Coloca o arquivo na área de preparação | Você escolhe o que entra no commit | Depois de revisar com `status` |
| `git add .` | Prepara tudo o que mudou na pasta | Prático quando todas as mudanças são do mesmo assunto | Com cuidado: confira o `status` antes |
| `git commit -m "mensagem"` | Salva uma versão no histórico local | Cria um ponto de retorno documentado | Quando uma parte do trabalho está pronta |
| `git push` | Envia os commits para o GitHub | Sem push, o trabalho existe só na sua máquina | Depois de commitar |
| `git pull` | Traz para a sua máquina o que mudou no GitHub | Mantém você atualizado e evita conflitos | **No começo do dia** e antes de criar uma branch |
| `git log --oneline` | Mostra o histórico, um commit por linha | Para ver o que foi feito e em que ordem | Sempre que quiser se localizar |
| `git log --oneline --graph --all` | Mostra o histórico com as branches desenhadas | Para visualizar branches e merges | Depois de um merge |

**Mensagem de commit:** curta, no imperativo, dizendo o que o commit faz. Bom: `Adiciona serviço do MinIO`. Ruim: `ajustes`, `teste`.

### 3.3 Branches e merge

| Comando | O que faz | Por que usar | Quando usar |
|---|---|---|---|
| `git branch` | Lista as branches; o `*` marca a atual | Confirma onde você está | Antes de começar a trabalhar |
| `git switch -c <nome>` | Cria uma branch e entra nela | Isola o trabalho novo da `main` | Ao começar uma feature ou correção |
| `git switch <nome>` | Troca para uma branch existente | Os arquivos da pasta mudam para a versão daquela branch | Para voltar à `main` ou a outra branch |
| `git push -u origin <nome>` | Envia a branch ao GitHub e liga a local à remota | O trabalho fica salvo e visível para o time | No **primeiro** push de uma branch; depois, só `git push` |
| `git merge <nome>` | Traz os commits de `<nome>` para a branch atual | É como a feature entra na `main` | Com a feature testada, estando na `main` |
| `git branch -d <nome>` | Apaga a branch local | Mantém a lista limpa. Recusa apagar o que não foi integrado | Depois do merge |
| `git push origin --delete <nome>` | Apaga a branch no GitHub | Mantém o repositório organizado | Depois do merge |

**Convenção de nomes:** `feature/...` para algo novo, `fix/...` para correção.

**Fluxo para uma pipeline nova sem mexer na `main`:**

1. `git switch main` e `git pull`
2. `git switch -c feature/nova-pipeline`
3. Trabalhe e faça commits na branch
4. `git push -u origin feature/nova-pipeline`
5. Pull Request no GitHub (ou `git switch main` + `git merge feature/nova-pipeline` + `git push`)

**Conflito no merge:** o Git marca o trecho com `<<<<<<<`, `=======` e `>>>>>>>`. Escolha o que fica, apague as marcações e rode `git add` + `git commit`.

---

## 4. Comandos de Docker

| Comando | O que faz | Por que usar | Quando usar |
|---|---|---|---|
| `docker --version` | Mostra a versão do Docker | Confirma que está instalado | Na preparação do ambiente |
| `docker pull <imagem>` | Baixa uma imagem de um registry | Traz software pronto (bancos, MinIO, nginx) | Antes de usar uma imagem nova (o `run` também baixa sozinho) |
| `docker images` | Lista as imagens na máquina | Mostra o que já foi baixado ou construído | Para conferir imagens e liberar espaço |
| `docker build -t <nome> <pasta>` | Constrói uma imagem a partir de um Dockerfile | Transforma o seu código numa imagem | Quando a imagem é sua (o compose faz isso com `build:`) |
| `docker run -d --name <nome> -p <host>:<container> <imagem>` | Cria e inicia um container | Coloca uma imagem para rodar | Para testes rápidos, fora do compose |
| `docker ps` | Lista os containers **rodando** | Primeira pergunta de qualquer investigação: "está de pé?" | Sempre que algo não responder |
| `docker ps -a` | Lista **todos** os containers, inclusive os parados | Mostra os que caíram e o código de saída | Quando um container "sumiu" |
| `docker logs <container>` | Mostra o que o container escreveu | **É onde aparecem os erros** | Quando algo falhar |
| `docker logs -f <container>` | Acompanha os logs ao vivo | Para ver o que acontece enquanto você testa | Durante testes |
| `docker exec -it <container> /bin/bash` | Abre um terminal dentro do container | Para olhar arquivos e variáveis por dentro | Para investigar (imagens mínimas: `/bin/sh`; a do MinIO não tem shell) |
| `docker stop <container>` | Para o container | Libera memória e a porta, sem apagar o container | Para pausar |
| `docker start <container>` | Liga de novo um container parado | Retoma sem recriar | Depois de um `stop` |
| `docker rm <container>` | Remove um container parado | Libera o nome. A imagem continua | Ao ver o erro *"name is already in use"* |
| `docker rmi <imagem>` | Remove uma imagem | Libera espaço em disco | Para limpar imagens que não usa mais |
| `docker volume ls` | Lista os volumes | Para ver onde estão os dados | Para conferir se o volume existe |
| `docker volume inspect <volume>` | Mostra detalhes do volume, inclusive o `Mountpoint` | Para saber onde o volume fica no disco | Por curiosidade ou investigação |

**Opções do `docker run`:**

| Opção | O que faz |
|---|---|
| `-d` | Roda em segundo plano e devolve o terminal |
| `--name` | Dá um nome ao container |
| `-p 8080:80` | Liga a porta 8080 da máquina à 80 do container |

**Exemplo de prática, com o nginx** (um servidor web usado só como container de teste):

```bash
docker pull nginx
docker run -d --name site1 -p 8080:80 nginx
docker run -d --name site2 -p 8081:80 nginx
docker ps
```

Dois containers da mesma imagem, em `localhost:8080` e `localhost:8081`. Depois, `docker stop` e `docker rm` nos dois: a imagem continua no `docker images`.

---

## 5. Comandos de Docker Compose

Todos os comandos rodam **dentro da pasta do projeto**, onde está o `docker-compose.yml`.

| Comando | O que faz | Por que usar | Quando usar |
|---|---|---|---|
| `docker compose config` | Valida o arquivo e mostra a versão "por extenso", com as variáveis substituídas | Pega erro de indentação, chave errada e `.env` faltando sem subir nada | **Antes do `up`**, sempre que mudar o YAML ou o `.env` |
| `docker compose up -d` | Cria rede, volumes e containers e sobe tudo em segundo plano | O jeito normal de subir o projeto | No início do trabalho, ou depois de mudar o YAML ou o `.env` |
| `docker compose up -d --build` | Igual, mas reconstrói as imagens com `build:` | Garante que a imagem da API tenha o Dockerfile e o `requirements.txt` atuais | Quando o Dockerfile ou o `requirements.txt` mudou |
| `docker compose up -d <serviço>` | Sobe só um serviço | Para usar só parte do projeto | Ex.: subir só o `minio` |
| `docker compose up` | Sobe preso ao terminal, mostrando todos os logs | Para acompanhar tudo ao vivo; `Ctrl+C` derruba | Durante testes |
| `docker compose ps` | Lista os serviços do projeto e o estado | Confirma que tudo está `running` | Logo depois de subir |
| `docker compose ps -a` | Inclui os serviços encerrados | Mostra quem caiu e o código de saída | Quando um serviço sumiu |
| `docker compose logs <serviço>` | Mostra os logs de um serviço | Para investigar erros | Quando algo falhar |
| `docker compose logs -f <serviço>` | Acompanha os logs ao vivo | Para ver o que acontece enquanto testa | Durante testes |
| `docker compose exec <serviço> <comando>` | Roda um comando dentro de um serviço | Para testar ou investigar por dentro | Ex.: `docker compose exec fiashop-api python ingestao.py` |
| `docker compose restart <serviço>` | Reinicia o serviço **sem reler o YAML** | Quando travou sem mudança de configuração | Ex.: o `--reload` não pegou a mudança |
| `docker compose build` | Só reconstrói as imagens com `build:` | Para construir sem subir | Raramente; o `up --build` já faz isso |
| `docker compose pull` | Baixa as versões mais novas das imagens | Para atualizar imagens com `latest` ou tags novas | Quando quiser atualizar o MinIO, por exemplo |
| `docker compose down` | Para e remove containers e rede. **Os volumes ficam** | Encerra o projeto sem perder dados | No fim do trabalho |
| `docker compose down -v` | Remove também os volumes | Começa do zero | ⚠️ **Apaga os dados do MinIO.** Use só de propósito |

**O ciclo do dia a dia:**

```bash
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
```

> **`restart` × `up -d`:** depois de mudar o `docker-compose.yml` ou o `.env`, use `docker compose up -d`, que recria o que mudou. O `restart` não lê as mudanças.

> **`docker compose exec` × `docker exec`:** fazem a mesma coisa. O primeiro usa o **nome do serviço**; o segundo, o **nome do container**. Neste projeto, os dois nomes são iguais.

---

## 6. Publicar uma imagem no Docker Hub

Publicar a imagem da API "congela" uma versão: qualquer máquina baixa a mesma imagem, sem precisar do código nem do build.

| Comando | O que faz | Por que usar | Quando usar |
|---|---|---|---|
| `docker login` | Entra na sua conta do Docker Hub | Sem login, o envio é recusado | Antes do primeiro `push` |
| `docker tag fiashop-api SEU-USUARIO/fiashop-api:1.0` | Dá à imagem o nome no formato `usuário/nome:versão` | O Docker Hub exige esse formato; a tag marca a versão | Antes de cada envio |
| `docker push SEU-USUARIO/fiashop-api:1.0` | Envia a imagem para o Docker Hub | Torna a imagem disponível para qualquer máquina | Quando uma versão está pronta |
| `docker buildx build --platform linux/amd64,linux/arm64 -t SEU-USUARIO/fiashop-api:1.0 --push ./api` | Constrói para Intel/AMD e para chips Apple, e envia | A imagem roda bem no Windows, no Linux e nos Macs com chip M | Quando a turma usa sistemas variados |

Depois de publicar, o serviço no compose usa `image: SEU-USUARIO/fiashop-api:1.0` no lugar do `build: ./api`, e saem o bind mount e o `--reload`, que são coisas de desenvolvimento.

**Cuidados:**

- **Versione** (`1.0`, `1.1`...), em vez de usar só `latest`.
- **Nunca coloque senha dentro da imagem.** Neste projeto, o Dockerfile copia só o código, e as senhas chegam pelo `environment`.
- **O repositório no Docker Hub nasce público.**

---

## 7. Referência do docker-compose.yml

O arquivo do projeto:

```yaml
services:

  minio:
    image: cgr.dev/chainguard/minio:latest
    container_name: minio
    user: root
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_storage:/data
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    command: server --console-address ":9001" /data
    networks:
      rede_fia:

  fiashop-api:
    build: ./api
    image: fiashop-api
    container_name: fiashop-api
    ports:
      - "8000:8000"
    environment:
      MINIO_ENDPOINT: http://minio:9000
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
      BUCKET_BRONZE: bronze
    volumes:
      - ./api:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    depends_on:
      - minio
    networks:
      rede_fia:

networks:
  rede_fia:
    driver: bridge

volumes:
  minio_storage: {}
```

| Chave | O que faz | Por que usar | Quando usar |
|---|---|---|---|
| `services:` | Abre a lista de containers | Cada item vira um container | Sempre |
| `image` | Define a imagem e a versão | Com a tag fixa, todos rodam o mesmo | Para imagens prontas, ou para dar nome a uma imagem construída |
| `build` | Constrói a imagem com o Dockerfile da pasta indicada | É como o seu código vira imagem | Para imagens suas, como a API |
| `container_name` | Dá um nome fixo ao container | Facilita `docker logs minio` | Quase sempre, em projetos pequenos |
| `user` | Define com qual usuário o container roda | Resolve problemas de permissão | Quando a imagem roda sem privilégios e precisa gravar no volume |
| `ports` | Publica portas no formato `HOST:CONTAINER` | Sem isso, o navegador não alcança o container | Para serviços que você acessa de fora do Docker |
| `volumes` | Monta volumes nomeados ou bind mounts | Dados sobrevivem ao container; código editável em tempo real | Volume nomeado para dados; bind mount para código em desenvolvimento |
| `environment` | Passa variáveis para o programa | Configura o container sem mudar a imagem | Para endereços, nomes e credenciais |
| `command` | Substitui o comando padrão da imagem | Ajusta como o programa inicia | Quando o padrão da imagem não serve |
| `depends_on` | Define a ordem de subida | Um serviço sobe depois daquele de que precisa | Quando há dependência. **Não espera o serviço ficar pronto**, só iniciar |
| `networks` | Coloca o container numa rede | Na mesma rede, os containers se acham pelo nome | Sempre que um serviço fala com outro |
| `networks:` (no fim) | **Cria** a rede | O serviço só usa o que foi criado aqui | Para cada rede usada |
| `volumes:` (no fim) | **Cria** o volume nomeado | Idem | Para cada volume nomeado usado |

**Os pares que precisam combinar:**

| Se trocar... | Troque também... | Por quê |
|---|---|---|
| A pasta de dentro (`/data`) em `volumes` | O `/data` no `command` do MinIO | O MinIO precisa gravar na pasta onde o volume está montado |
| O nome do volume (`minio_storage`) | O bloco `volumes:` do fim | O bloco do fim cria o volume; o serviço o usa pelo nome |
| A porta do console no `--console-address` | A porta da direita do `ports` | O `ports` precisa apontar para a porta onde o console está |

**O `command` do MinIO, por partes:** a imagem já roda o programa `minio`, e o `command` vira os argumentos dele. O resultado é `minio server --console-address ":9001" /data`:

- `server` liga o modo servidor;
- `--console-address ":9001"` fixa o console web na porta 9001 (sem isso, a porta seria aleatória);
- `/data` é a pasta onde o MinIO grava, a mesma montada no volume. O nome `/data` segue a documentação do MinIO.

**Onde o volume fica de verdade:** dentro do container, em `/data`. No Docker, no volume `fiashop_minio_storage` (o prefixo é o nome da pasta do projeto). No disco, em `/var/lib/docker/volumes/...` no Linux, ou dentro da máquina virtual do Docker Desktop no Windows e no Mac. O MinIO grava num formato interno, então use o console ou o `boto3` para ver os arquivos.

**Como conferir:** `docker compose config` mostra o arquivo por extenso. Se aparecer erro ou o aviso `variable is not set`, há algo a corrigir. A saída mostra a senha em texto puro, então não compartilhe essa saída.

---

## 8. Referência do Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py ingestao.py ./
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| Instrução | O que faz | Por que usar |
|---|---|---|
| `FROM` | Define a imagem base | Reaproveita uma imagem oficial; o `slim` é menor |
| `WORKDIR` | Cria e entra numa pasta dentro da imagem | Os comandos seguintes acontecem nela |
| `COPY` | Copia arquivos da sua máquina para a imagem | Leva o código e as dependências para dentro |
| `RUN` | Executa um comando durante o build | Instala as bibliotecas na imagem |
| `EXPOSE` | Documenta a porta usada | É só documentação; quem publica é o `ports:` do compose |
| `CMD` | Define o comando padrão ao iniciar o container | Liga a API. O `command:` do compose pode substituí-lo |

**Por que o `requirements.txt` é copiado antes do código:** o Docker guarda cada passo em cache. Se só o código muda, ele reaproveita a instalação das bibliotecas, e o build fica muito mais rápido.

**`--host 0.0.0.0`:** faz a API aceitar conexões de fora do container. Sem isso, o navegador não a alcança.

**Dockerfile × docker-compose.yml:** o Dockerfile diz **como construir uma imagem**; o compose diz **como rodar vários containers juntos**.

---

## 9. Comandos do sistema (Windows, Mac, Linux)

Os comandos `git` e `docker` são iguais nos três sistemas. O que muda são os comandos do próprio sistema.

| Tarefa | Windows (PowerShell) | Windows (CMD) | Mac / Linux |
|---|---|---|---|
| Copiar o `.env` | `Copy-Item .env.example .env` | `copy .env.example .env` | `cp .env.example .env` |
| Criar um arquivo vazio | `New-Item .env -ItemType File` | `type nul > .env` | `touch .env` |
| Listar arquivos (com ocultos) | `Get-ChildItem -Force` | `dir /a` | `ls -a` |
| Ver o conteúdo de um arquivo | `Get-Content .env` | `type .env` | `cat .env` |
| Pasta atual | `pwd` | `cd` | `pwd` |
| Continuar o comando na linha de baixo | `` ` `` (crase) | `^` | `\` |
| Enviar um POST | `Invoke-RestMethod` ou `curl.exe` | `curl` com `\"` | `curl` |
| Interromper um comando | `Ctrl+C` | `Ctrl+C` | `Ctrl+C` (também no Mac) |

**Terminal recomendado:** no Windows, o PowerShell (o Git Bash atrapalha alguns comandos do Docker). No Mac, o Terminal. No Linux, o terminal padrão.

**Enviar um pedido pelo terminal:**

**Mac / Linux:**

```bash
curl -X POST http://localhost:8000/pedidos -H "Content-Type: application/json" \
  -d '{"id_pedido": 2, "cliente": "Bruno Lima", "produto": "Moletom FIA", "quantidade": 1, "valor_unitario": 189.9}'
```

**Windows (PowerShell):**

```powershell
$pedido = @{ id_pedido = 2; cliente = "Bruno Lima"; produto = "Moletom FIA"; quantidade = 1; valor_unitario = 189.9 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8000/pedidos -ContentType "application/json" -Body $pedido
```

Na dúvida, use o Swagger em `http://localhost:8000/docs`, igual em qualquer sistema.

---

## 10. Problemas comuns

**Roteiro de investigação**, que resolve a maioria dos casos:

1. `docker compose ps -a`: o container está de pé ou caiu?
2. `docker compose logs <serviço>`: qual erro ele escreveu?
3. `docker compose config`: o compose e o `.env` estão certos?
4. `docker exec -it fiashop-api /bin/bash` e depois `env | grep MINIO`: as variáveis chegaram?

### Todos os sistemas

| Sintoma | Causa provável | Como resolver |
|---|---|---|
| `401 UNAUTHORIZED` ao baixar `quay.io/minio/minio` | A imagem oficial do MinIO deixou de ser pública | Use `cgr.dev/chainguard/minio:latest`, como no compose deste projeto |
| MinIO cai com `permission denied` em `/data` | A imagem roda sem privilégios | Confira o `user: root` no serviço `minio` |
| `container name "/minio" is already in use` | Sobrou um container `minio` do lab do curso | `docker stop minio` e `docker rm minio` |
| `port is already allocated` | Outro container ou programa usa a porta | `docker ps` para achar quem usa, ou troque o lado esquerdo: `"9010:9000"` |
| `Cannot connect to the Docker daemon` | O Docker não está rodando | Abra o Docker Desktop |
| Erro de YAML (`mapping values are not allowed`...) | Indentação errada ou TAB | `docker compose config` aponta a linha |
| `variable is not set` | Falta o `.env`, ou ele está em outra pasta | Crie o `.env` na pasta do `docker-compose.yml` |
| API não sobe e o log mostra `KeyError: 'MINIO_ROOT_USER'` | A variável não chegou ao container | Confira o `.env` e o `environment:` da `fiashop-api`, e rode `docker compose up -d` |
| MinIO não sobe e o log fala de senha | Senha com menos de 8 caracteres | Use uma senha maior no `.env` |
| POST devolve 500 logo depois de subir | O MinIO ainda estava iniciando | Espere alguns segundos e envie de novo |
| POST devolve 500 com `Could not connect` | `MINIO_ENDPOINT` com `localhost` | Use `http://minio:9000` |
| POST devolve 422 | O pedido está fora do formato | Confira os campos e os tipos. É a validação funcionando |
| O bucket `bronze` não aparece no console | Nenhum pedido foi enviado ainda | A API cria o bucket no primeiro pedido |
| A mudança no código não aparece | O `--reload` não detectou | `docker compose restart fiashop-api` |
| `git push` recusa a senha | O GitHub não aceita a senha da conta | Login pelo navegador (Windows) ou `gh auth login` |
| `git push` diz `rejected (fetch first)` | O GitHub tem commits que você não tem | `git pull` e depois `git push` |
| `git status` mostra todos os arquivos modificados sem você ter mexido | Quebras de linha diferentes entre sistemas | `git config --global core.autocrlf true` (Windows) ou `input` (Mac/Linux) |

### Só no Windows

| Sintoma | Como resolver |
|---|---|
| Docker Desktop fala de **WSL** | PowerShell como administrador: `wsl --install` e `wsl --update`. Reinicie |
| Docker Desktop fala de **virtualização** | Ative "Virtualization Technology" (Intel VT-x / AMD-V) na BIOS |
| `the input device is not a TTY` no `docker exec` | Use o PowerShell, ou `winpty docker exec -it <c> //bin/bash` no Git Bash |
| `docker exec` tenta abrir `C:/Program Files/Git/...` | Use o PowerShell, ou escreva `//bin/bash` |
| `cp` ou `touch` não funcionam | Você está no CMD. Use o PowerShell, ou `copy` no CMD |
| `curl` com JSON dá erro de aspas | Use `curl.exe`, o `Invoke-RestMethod` ou o Swagger |

### Só no Mac

| Sintoma | Como resolver |
|---|---|
| `Cannot connect to the Docker daemon` | Abra o Docker Desktop e espere o ícone parar de animar |
| `zsh: command not found: code` | No VS Code: `Cmd+Shift+P` → **Shell Command: Install 'code' command in PATH** |
| `xcrun: error: invalid active developer path` | `xcode-select --install` |
| `git push` pede usuário e senha | `gh auth login` |

### Só no Linux

| Sintoma | Como resolver |
|---|---|
| `permission denied ... docker.sock` | `sudo usermod -aG docker $USER`, depois saia da sessão e entre de novo |
| `Cannot connect to the Docker daemon` | `sudo systemctl start docker` |
| `docker: 'compose' is not a docker command` | `sudo apt install docker-compose-plugin` |
| Não consigo apagar `api/__pycache__` | `sudo rm -rf api/__pycache__` (o container criou como `root`) |
