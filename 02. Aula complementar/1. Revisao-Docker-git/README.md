# FIAShop — Git, Docker e Docker Compose (resumo)

**O case:** a FIAShop recebe pedidos o dia inteiro, e eles se perdem em planilhas atualizadas à mão. A missão do time de dados é guardar **todo pedido, do jeito que chegou**, num lugar central e confiável: a **camada bronze** do data lake.

**O que vamos construir:** uma API (FastAPI) recebe o pedido, e um script Python grava esse pedido como JSON no MinIO, o nosso "S3 local".

```
POST /pedidos  →  main.py (FastAPI)  →  ingestao.py  →  MinIO: bronze/pedidos/data_ingestao=AAAA-MM-DD/pedido_1_143005.json
```

**A ordem da aula:**

1. [Git](#1-git): versionar e compartilhar o código
2. [Docker: comandos básicos](#2-docker-comandos-básicos): rodar e investigar containers
3. [Docker Compose](#3-docker-compose): subir vários containers com um arquivo
4. [A aplicação na prática](#4-a-aplicação-na-prática): a pipeline funcionando

> Este é o resumo. A versão com cada passo detalhado está no [GUIA-COMPLETO.md](GUIA-COMPLETO.md).

**Pré-requisitos:** Docker Desktop (ou Docker Engine no Linux) aberto, Git, VS Code e uma conta no GitHub. No Windows, use o **PowerShell**.

---

## Antes de começar: entrar na pasta da aula

Abra o terminal (PowerShell no Windows, Terminal no Mac/Linux), vá até a pasta onde você clonou o repositório do curso e entre na pasta desta aula, um comando por vez:

```bash
cd "engenharia-dados"
cd "02. Aula complementar"
cd "1. Revisao-Docker-git"
```

> As aspas são necessárias porque os nomes das pastas têm espaços.

Confira se você está no lugar certo:

```bash
ls
```

Devem aparecer o `docker-compose.yml` e a pasta `api`. Os comandos `docker compose` desta aula precisam ser rodados **dentro desta pasta**.

---

## 1. Git

**Git** guarda o histórico do projeto na sua máquina. **GitHub** guarda uma cópia na nuvem para o time.

```
Pasta de trabalho  --add-->  Área de preparação  --commit-->  Histórico local  --push-->  GitHub
                                                              Histórico local  <--pull--  GitHub
```

### 1.1 Configurar (uma vez por computador)

```bash
git config --global user.name "Seu Nome"
git config --global user.email "email-da-conta@github.com"
git config --global init.defaultBranch main
```

| Comando | O que faz | Por que é importante |
|---|---|---|
| `user.name` / `user.email` | Grava quem é o autor dos commits | Sem isso, o Git não deixa commitar. O e-mail liga os commits ao seu perfil do GitHub |
| `init.defaultBranch main` | Usa `main` como branch principal | É o padrão do GitHub |

Ajuste também as quebras de linha, para o Git não achar que um arquivo inteiro mudou só porque passou entre Windows e Mac/Linux:

- **Windows:** `git config --global core.autocrlf true`
- **Mac / Linux:** `git config --global core.autocrlf input`

**Login no GitHub:**

- **Windows:** no primeiro `git push`, abre uma janela do navegador para você entrar.
- **Mac / Linux:** rode `gh auth login` e escolha GitHub.com → HTTPS → Yes → Login with a web browser.

### 1.2 Clonar o repositório

Crie no GitHub um repositório `fiashop`, marcando **Add a README file**. Depois:

```bash
git clone https://github.com/SEU-USUARIO/fiashop.git
cd fiashop
code .
```

| Comando | O que faz | Por que é importante |
|---|---|---|
| `git clone <url>` | Baixa o repositório com todo o histórico | É como você começa em qualquer projeto que já existe |
| `cd fiashop` | Entra na pasta do projeto | Os comandos `git` e `docker compose` só funcionam dentro da pasta do projeto |
| `code .` | Abre a pasta no VS Code | O `.` significa "esta pasta" |

### 1.3 O ciclo do dia a dia

Crie o `.gitignore`, a lista do que **nunca** vai para o GitHub:

```
.env
__pycache__/
*.py[cod]
.venv/
venv/
.DS_Store
.vscode/
.idea/
```

| Linha | Por que ignorar |
|---|---|
| `.env` | Guarda as **senhas**. É o mais importante da lista |
| `__pycache__/`, `*.py[cod]` | Arquivos que o Python gera sozinho ao rodar |
| `.venv/`, `venv/` | Bibliotecas instaladas localmente; podem ter centenas de MB |
| `.DS_Store`, `.vscode/`, `.idea/` | Arquivos do sistema e do editor, pessoais de cada um |

Agora o ciclo:

```bash
git status
git add .gitignore
git commit -m "Adiciona .gitignore"
git push
git log --oneline
```

| Comando | O que faz | Por que é importante |
|---|---|---|
| `git status` | Mostra o que mudou e o que está preparado | **Rode antes de tudo**, para saber exatamente o que vai entrar no commit |
| `git add <arquivo>` | Coloca o arquivo na área de preparação | Você escolhe o que entra no commit |
| `git commit -m "..."` | Salva uma versão no histórico local | Cria um ponto ao qual você pode voltar, com uma mensagem explicando a mudança |
| `git push` | Envia os commits para o GitHub | Sem push, o trabalho existe só no seu computador |
| `git pull` | Traz o que mudou no GitHub | Mantém você atualizado com o time. **Comece o dia com ele** |
| `git log --oneline` | Mostra o histórico, um commit por linha | Mostra quem mudou o quê e em que ordem |

### 1.4 Branches: trabalhar sem mexer na `main`

A `main` é a versão que **funciona**, e é dela que o time parte. Algo novo é feito numa **branch**, uma linha paralela do histórico.

```
main     ●───────●──────────────────●   ← continua estável
                  \                /
feature/api        ●─────●────────●     ← você trabalha aqui
```

```bash
git switch -c feature/api-pedidos
git push -u origin feature/api-pedidos
git switch main
git merge feature/api-pedidos
```

| Comando | O que faz | Por que é importante |
|---|---|---|
| `git branch` | Lista as branches; o `*` marca onde você está | Confirma onde você está antes de trabalhar |
| `git switch -c <nome>` | Cria uma branch e entra nela | Todo commit a partir daqui fica na branch, não na `main` |
| `git switch <nome>` | Troca de branch | Os arquivos da pasta mudam para a versão daquela branch |
| `git push -u origin <nome>` | Envia a branch ao GitHub (o `-u` só no primeiro push) | O trabalho fica salvo e visível para o time |
| `git merge <nome>` | Traz os commits de `<nome>` para a branch atual | É quando a feature testada entra na `main` |

> **"Estou trabalhando em uma pipeline nova. Como faço isso sem mexer na `main`?"**
> `git switch main` → `git pull` → `git switch -c feature/nova-pipeline` → commits na branch → `git push -u origin feature/nova-pipeline` → Pull Request no GitHub (ou `git switch main` + `git merge`).

No time, o merge costuma ser feito por **Pull Request** no GitHub: um colega revisa antes de o código entrar na `main`.

---

## 2. Docker: comandos básicos

Docker empacota um programa **com tudo de que ele precisa**, para rodar igual em qualquer computador. Acaba o "na minha máquina funciona".

| Conceito | O que é | Analogia: curso de MBA |
|---|---|---|
| **Imagem** | O pacote pronto, somente leitura. É o molde | A ementa da disciplina |
| **Container** | Uma imagem em execução | Cada turma em andamento |
| **Porta** | Liga uma porta da sua máquina à do container (`HOST:CONTAINER`) | O número da sala |
| **Volume** | Pasta fora do container; os dados sobrevivem a ele | A secretaria: a turma acaba, as notas ficam |
| **Network** | Rede onde os containers se acham pelo nome | O grupo dos professores: um chama o outro pelo nome |

**Imagem ≠ container:** uma imagem gera vários containers, e apagar um container não apaga a imagem.

### 2.1 Na prática, com o nginx

O **nginx** é um servidor web. Aqui ele só serve de container de teste: a imagem é leve, sobe na hora e mostra uma página no navegador.

```bash
docker pull nginx
docker images
docker run -d --name site1 -p 8080:80 nginx
docker run -d --name site2 -p 8081:80 nginx
docker ps
```

Abra `localhost:8080` e `localhost:8081`: são dois containers da **mesma** imagem.

| Comando | O que faz | Por que é importante |
|---|---|---|
| `docker pull <imagem>` | Baixa uma imagem | É como se obtém qualquer software pronto: bancos, MinIO, Kafka |
| `docker images` | Lista as imagens baixadas | Mostra que a imagem existe, mas ainda não roda |
| `docker run -d --name site1 -p 8080:80 nginx` | Cria e inicia um container | `-d`: em segundo plano. `--name`: dá um nome. `-p 8080:80`: a 8080 da máquina leva à 80 do container |
| `docker ps` | Lista os containers rodando | Primeira pergunta de qualquer investigação: "está de pé?" |

### 2.2 Os comandos que dão autonomia

```bash
docker logs site1
docker exec -it site1 /bin/bash      # entra no container; "exit" para sair
docker stop site1
docker ps -a
docker rm site1
```

| Comando | O que faz | Por que é importante |
|---|---|---|
| `docker logs <c>` | Mostra o que o container escreveu (`-f` acompanha ao vivo) | **É onde aparecem os erros** |
| `docker exec -it <c> /bin/bash` | Abre um terminal dentro do container | Para conferir arquivos e variáveis por dentro |
| `docker stop <c>` | Para o container | Libera memória e a porta; o container ainda existe |
| `docker ps -a` | Lista **todos**, inclusive os parados | É onde você encontra um container que **caiu** |
| `docker rm <c>` | Remove o container parado | Libera o nome. A imagem continua |

> **Parado não é removido:** um container parado ainda ocupa o nome. Rodar de novo `docker run --name site1` dá o erro *"name is already in use"*, e a solução é `docker rm`.

> **Windows:** no Git Bash, o `docker exec -it` costuma falhar; use o PowerShell. **Linux:** se der `permission denied`, rode `sudo usermod -aG docker $USER` e entre de novo na sessão.

Limpe o teste:

```bash
docker stop site2
docker rm site2
docker images          # o nginx continua: imagem ≠ container
```

---

## 3. Docker Compose

Com vários containers, o `docker run` vira uma linha enorme para cada um. O **Compose** descreve todos num arquivo, o `docker-compose.yml`, e um comando sobe tudo. O arquivo vai para o Git, então o time inteiro sobe o mesmo ambiente.

### 3.1 As chaves do `docker-compose.yml`

Exemplo com o MinIO, baseado no compose do curso (sem as variáveis do Kafka, que não usamos aqui):

```yaml
services:
  minio:
    image: cgr.dev/chainguard/minio:latest
    container_name: minio
    user: root
    ports:
      - "9000:9000"   # API S3, usada pelos programas
      - "9001:9001"   # console web, usado no navegador
    volumes:
      - minio_storage:/data
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    command: server --console-address ":9001" /data
    networks:
      rede_fia:

networks:
  rede_fia:
    driver: bridge

volumes:
  minio_storage: {}
```

| Chave | O que faz | Por que é importante |
|---|---|---|
| `image` | Imagem e versão a usar | Com a versão fixa, todos rodam exatamente o mesmo |
| `build` | Constrói a imagem a partir de um Dockerfile | É como o **seu** código vira imagem (aparece na API, seção 4) |
| `container_name` | Nome fixo do container | Permite `docker logs minio` |
| `ports` | `HOST:CONTAINER` | Sem portas publicadas, o navegador não alcança o container |
| `volumes` | Guarda dados fora do container | Sem volume, os dados **somem** quando o container é removido |
| `environment` | Variáveis passadas ao programa | É como se configura um container sem mudar a imagem |
| `command` | Comando executado ao iniciar | Substitui o padrão da imagem |
| `depends_on` | Ordem de subida | Um serviço sobe depois daquele de que precisa |
| `networks` | Rede do container | Na mesma rede, os containers se acham **pelo nome do serviço** |

Os blocos `networks:` e `volumes:` no fim do arquivo **criam** a rede e o volume; dentro do serviço, eles só **usam**.

> **Por que não a imagem do compose do curso:** o compose do curso usa `quay.io/minio/minio`. Essa imagem e a `minio/minio` do Docker Hub deixaram de ser distribuídas publicamente, e o download agora falha com `401 UNAUTHORIZED`. Por isso usamos a imagem do MinIO mantida pela Chainguard (`cgr.dev/chainguard/minio`). O `user: root` evita erro de permissão ao gravar no volume.
>
> Na versão gratuita, essa imagem só tem a tag `latest`. É uma exceção à regra de fixar a versão, que continua valendo para o resto do projeto.

> **YAML:** indentação é sintaxe. Use 2 espaços, nunca TAB.

### 3.2 Variáveis de ambiente e o `.env`

A senha **não** fica no `docker-compose.yml`, que vai para o GitHub. Ele só tem os nomes (`${MINIO_ROOT_PASSWORD}`), e o Compose busca os valores no arquivo `.env`, que está no `.gitignore`.

| Arquivo | Vai para o GitHub? | Para que serve |
|---|---|---|
| `.env` | **Não** | Valores reais (senhas) da sua máquina |
| `.env.example` | **Sim** | Modelo que mostra ao time quais variáveis criar |

### 3.3 Comandos do Compose

```bash
docker compose up -d        # sobe tudo
docker compose ps           # confere
docker compose logs -f      # acompanha
docker compose down         # derruba tudo
```

| Comando | O que faz | Quando usar |
|---|---|---|
| `docker compose config` | Valida o arquivo e mostra as variáveis já substituídas | Antes de subir, para achar erro de indentação ou `.env` faltando |
| `docker compose up -d` | Cria rede, volumes e containers e sobe tudo em segundo plano | O jeito normal de subir o projeto |
| `docker compose up -d --build` | Igual, mas reconstrói as imagens com `build:` | Quando o código, o Dockerfile ou o `requirements.txt` mudou |
| `docker compose ps` / `ps -a` | Estado dos serviços / incluindo os encerrados | Sempre depois de subir |
| `docker compose logs -f <serviço>` | Logs ao vivo de um serviço | Para investigar erros |
| `docker compose exec <serviço> <comando>` | Roda um comando dentro do serviço | Para testar ou investigar por dentro |
| `docker compose restart <serviço>` | Reinicia sem reler o YAML | Quando travou sem você mudar configuração |
| `docker compose down` | Remove containers e rede; **os volumes ficam** | Para encerrar o trabalho |
| `docker compose down -v` | Remove também os volumes | ⚠️ Apaga os dados. Só para começar do zero |

---

## 4. A aplicação na prática

### 4.1 A arquitetura

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

| Container | O que faz |
|---|---|
| `minio` | Armazenamento compatível com S3: o nosso data lake |
| `fiashop-api` | Recebe o pedido, valida e grava na bronze. Na primeira gravação, cria o bucket `bronze` se ele não existir |

> **Regra de ouro:** de **fora** do Docker, use `localhost` + a porta publicada. De **dentro** (um container falando com outro), use o **nome do serviço**: `http://minio:9000`. Dentro de um container, `localhost` é o próprio container.

### 4.2 Os arquivos do projeto

```
fiashop/
├── docker-compose.yml   ← os 2 serviços: minio e fiashop-api
├── .env.example         ← modelo das variáveis
├── .gitignore
└── api/
    ├── Dockerfile       ← receita da imagem da API
    ├── requirements.txt ← fastapi, uvicorn, boto3
    ├── main.py          ← FastAPI: recebe e valida o pedido
    └── ingestao.py      ← grava o pedido na bronze
```

**`api/main.py`: a porta de entrada.**

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

O `Pedido` é o contrato: se faltar um campo ou vier texto onde era número, a FastAPI recusa com **erro 422**, antes de o dado chegar à bronze.

**`api/ingestao.py`: a gravação.**

```python
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")   # não é segredo: pode ter valor padrão
MINIO_USER = os.environ["MINIO_ROOT_USER"]                           # segredo: sem valor padrão no código
MINIO_PASSWORD = os.environ["MINIO_ROOT_PASSWORD"]

def garantir_bucket():
    nomes = [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]
    if BUCKET_BRONZE not in nomes:
        s3.create_bucket(Bucket=BUCKET_BRONZE)       # cria o bucket só na primeira vez

def salvar_na_bronze(pedido):
    garantir_bucket()
    agora = datetime.now()
    pedido["recebido_em"] = agora.strftime("%Y-%m-%dT%H:%M:%S")
    caminho = f"pedidos/data_ingestao={agora:%Y-%m-%d}/pedido_{pedido['id_pedido']}_{agora:%H%M%S}.json"
    s3.put_object(Bucket="bronze", Key=caminho, Body=json.dumps(pedido, ensure_ascii=False).encode("utf-8"))
```

É a mesma lógica da Aula 6 de Python (`json` para a pasta `bronze/`), trocando o destino para o MinIO com o `boto3`. A pasta `data_ingestao=` segue o particionamento da Aula 7.

O `garantir_bucket()` cria o bucket `bronze` se ele ainda não existir, então ninguém precisa criá-lo à mão antes do primeiro pedido.

**Onde fica a senha:** só no `.env` da raiz. O caminho até o código é `.env` → `environment:` do `docker-compose.yml` → container → `os.environ`. Não existe um segundo `.env` dentro de `api/`, para a senha ficar num lugar só.

| Forma | Quando usar | Por quê |
|---|---|---|
| `os.getenv("NOME", "padrão")` | Configurações que **não são segredo** (endereço, nome do bucket) | Se a variável faltar, o código segue com um valor razoável |
| `os.environ["NOME"]` | **Segredos** (usuário, senha, tokens) | Se a variável faltar, o código para com `KeyError` na hora, em vez de rodar com uma senha escrita no código |

**`api/Dockerfile`: a receita da imagem.**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py ingestao.py ./
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

O `requirements.txt` é copiado **antes** do código para aproveitar o cache: se só o código muda, o Docker não reinstala as bibliotecas.

**O serviço da API no `docker-compose.yml`:**

```yaml
  fiashop-api:
    build: ./api                          # constrói com o Dockerfile da pasta api
    container_name: fiashop-api
    ports:
      - "8000:8000"
    environment:
      MINIO_ENDPOINT: http://minio:9000   # nome do serviço, não localhost
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    volumes:
      - ./api:/app                        # edita no VS Code, o container vê na hora
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    depends_on:
      - minio                             # sobe depois do MinIO
    networks:
      rede_fia:
```

### 4.3 Subir

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
docker compose up -d --build
```

**Mac / Linux:**

```bash
cp .env.example .env
docker compose up -d --build
```

Depois, em qualquer sistema:

```bash
docker compose ps
docker compose logs -f fiashop-api
```

| Comando | O que faz | O que você deve ver |
|---|---|---|
| `cp` / `Copy-Item` | Cria o seu `.env` a partir do modelo | Um arquivo `.env` na pasta (troque a senha) |
| `docker compose up -d --build` | Baixa a imagem do MinIO, constrói a imagem da API e sobe os 2 serviços | Imagem do MinIO baixada, a da API construída |
| `docker compose ps` | Serviços rodando | `minio` e `fiashop-api` como `running` |
| `docker compose logs -f fiashop-api` | Logs da API ao vivo | `Uvicorn running on http://0.0.0.0:8000` |

O bucket `bronze` só aparece no console depois do primeiro pedido, porque é a API que o cria.

### 4.4 Testar

1. `http://localhost:8000` → mensagem *FIAShop API no ar*.
2. `http://localhost:8000/docs` → **POST /pedidos** → **Try it out** → cole o pedido abaixo → **Execute**.

```json
{
  "id_pedido": 1,
  "cliente": "Ana Souza",
  "produto": "Camiseta FIA",
  "quantidade": 2,
  "valor_unitario": 79.9
}
```

3. A resposta é **201**, com o caminho do arquivo gravado.
4. `http://localhost:9001` (usuário e senha do `.env`) → **bronze → pedidos → data_ingestao=...** → abra o JSON.
5. Envie um pedido com `"id_pedido": "abc"` → **422**: a validação barrou o dado.

Pelo terminal:

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

### 4.5 Investigar

```bash
docker compose exec fiashop-api python ingestao.py
docker exec -it fiashop-api /bin/bash
    env | grep MINIO
    exit
```

| Comando | O que faz | Por que é importante |
|---|---|---|
| `docker compose exec fiashop-api python ingestao.py` | Roda só o script de ingestão (grava o pedido 999) | Separa "o problema é na API" de "o problema é na gravação" |
| `docker exec -it fiashop-api /bin/bash` | Entra no container da API | Para investigar por dentro |
| `env \| grep MINIO` | (Dentro) mostra as variáveis do MinIO | Confirma que o compose entregou endereço e credenciais |

**Experimente o erro mais comum:** troque `MINIO_ENDPOINT` para `http://localhost:9000`, rode `docker compose up -d` e envie um pedido. O log mostra *Could not connect*, porque dentro do container `localhost` é o próprio container. Volte para `http://minio:9000`.

### 4.6 Versionar com branch

```bash
git switch -c feature/api-pedidos
git add api docker-compose.yml .env.example
git commit -m "Adiciona API de pedidos e ingestão na bronze"
git push -u origin feature/api-pedidos
git switch main
git merge feature/api-pedidos
git push
```

O `.env` não aparece no `git status`: o `.gitignore` está protegendo as senhas.

---

## Bronze, Silver e Gold

| Camada | O que guarda | Na FIAShop |
|---|---|---|
| **Bronze** | O dado como chegou, mais a data de chegada | Um JSON por pedido (**feito hoje**) |
| **Silver** | Dado limpo e tipado, em formato analítico | Os pedidos do dia num Parquet, com `valor_total` |
| **Gold** | Dado agregado para o negócio | Faturamento por produto por dia |

**Desafio:** numa branch `feature/silver`, crie o `silver.py`, que lê a bronze do dia, calcula `valor_total = quantidade * valor_unitario` e grava um Parquet no bucket `silver`. Depois, abra um Pull Request.

---

## Problemas comuns

| Sintoma | Como resolver |
|---|---|
| `container name "/minio" is already in use` | `docker stop minio` e `docker rm minio` (sobrou do lab do curso) |
| `port is already allocated` | `docker ps` para achar quem usa a porta, ou troque o lado esquerdo: `"9010:9000"` |
| `Cannot connect to the Docker daemon` | Abra o Docker Desktop. No Linux: `sudo systemctl start docker` |
| `variable is not set` | Falta o `.env` na pasta do `docker-compose.yml` |
| API não sobe e o log mostra `KeyError: 'MINIO_ROOT_USER'` | A variável não chegou ao container. Confira o `.env` na raiz e o `environment:` do serviço `fiashop-api`, e rode `docker compose up -d` |
| `401 UNAUTHORIZED` ao baixar `quay.io/minio/minio` | A imagem oficial deixou de ser pública. Use `cgr.dev/chainguard/minio:latest`, como no `docker-compose.yml` deste projeto |
| MinIO cai com `permission denied` em `/data` | Confira se o serviço `minio` tem `user: root` |
| POST devolve 500 logo depois de subir | O MinIO ainda estava iniciando. Espere alguns segundos e envie de novo |
| POST devolve 500 com `Could not connect` | `MINIO_ENDPOINT` deve ser `http://minio:9000` |
| `git push` recusa a senha | Login pelo navegador (Windows) ou `gh auth login` |
| `git push` com `rejected (fetch first)` | `git pull` e depois `git push` |

Mais casos, separados por sistema operacional, estão no [GUIA-COMPLETO.md](GUIA-COMPLETO.md#8-problemas-comuns).
