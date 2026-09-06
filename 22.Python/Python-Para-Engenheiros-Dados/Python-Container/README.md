# Lendo um arquivo CSV com Python no Docker

Você vai organizar o Python em uma função `main()`, instalar dependências com `requirements.txt` e usar `docker compose` para subir tudo com um comando só.

## Antes de começar

```sh
docker --version
docker compose version
```

Os dois comandos precisam responder com um número de versão.


**O que o código faz:**

| Parte | O que faz |
|---|---|
| `import csv` | módulo da biblioteca padrão do Python para ler e escrever CSV |
| `from tabulate import tabulate` | biblioteca **externa** — precisa ser instalada, e por isso vai no `requirements.txt` |
| `CAMINHO_ARQUIVO` | constante com o caminho do arquivo — se mudar de arquivo, muda em um lugar só |
| `def carregar_clientes(caminho)` | função que só lê o arquivo e devolve os dados |
| `with open(...) as f` | abre o arquivo e **fecha sozinho** no final, mesmo se der erro |
| `encoding='utf-8'` | garante que acentos (`São Paulo`, `João`) sejam lidos corretamente |
| `csv.DictReader(f)` | usa o cabeçalho do CSV como chave: cada linha vira um dicionário |
| `def mostrar_tabela(registros)` | função que só exibe os dados, usando o `tabulate` |
| `headers='keys'` | usa as chaves do dicionário como cabeçalho da tabela |
| `disable_numparse=True` | mostra os valores exatamente como estão no CSV, sem converter para número |
| `def main()` | função principal: organiza o que o programa faz, na ordem |
| `if not registros: return` | se o arquivo estiver vazio, avisa e encerra sem quebrar no `registros[0]` |

### Por que `if __name__ == '__main__':`?

```python
if __name__ == '__main__':
    main()
```

Todo arquivo Python tem uma variável embutida chamada `__name__`. O valor dela depende de **como o arquivo foi acionado**:

| Situação | Valor de `__name__` | O bloco roda? |
|---|---|---|
| Você executa `python main.py` | `'__main__'` | sim |
| Outro arquivo faz `import main` | `'main'` | não |

Ou seja: essa linha é um **interruptor**. Ela diz "só execute a `main()` se este arquivo for o programa que está sendo rodado".

Sem ela, na hora que alguém importasse o seu arquivo para reaproveitar a função `carregar_clientes()`, o programa inteiro rodaria junto e imprimiria tudo na tela sem ninguém ter pedido.

Definir uma função `main()` e chamá-la nesse bloco é a convenção padrão do Python. Traz três ganhos:

- **Ordem** — dá para ler a `main()` e entender o programa inteiro em 5 linhas.
- **Reúso** — a `carregar_clientes()` pode ser importada por outro script.
- **Teste** — dá para testar cada função separada, sem executar o programa todo.

## Arquivo `requirements.txt`

É nele que se lista tudo que o projeto precisa instalar.

```
tabulate==0.9.0
```

Uma linha, uma biblioteca. O `==0.9.0` **trava a versão**: todo mundo que rodar este projeto — você, seu colega, o servidor — vai instalar exatamente a mesma versão e ver o mesmo resultado. Sem isso, daqui a seis meses o `pip` instalaria a versão mais nova e o código poderia quebrar sem ninguém ter tocado nele.

**Toda linha aqui corresponde a um `import` do seu código.** Repare no que *não* está listado: o `csv`. Ele já vem junto com o Python, não precisa ser instalado. Só entram no `requirements.txt` as bibliotecas externas, as que você instalaria com `pip install`.

Se quiser testar na sua máquina antes de dockerizar:


## `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copia e instala as dependências primeiro (aproveita o cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY main.py .

CMD ["python", "main.py"]
```

**O que cada linha faz:**

| Linha | O que faz |
|---|---|
| `FROM python:3.12-slim` | parte de uma imagem que já tem o Python instalado |
| `WORKDIR /app` | cria e entra na pasta `/app` dentro da imagem |
| `COPY requirements.txt .` | copia **só** a lista de dependências |
| `RUN pip install ...` | instala as dependências dentro da imagem |
| `COPY main.py .` | copia o código |
| `CMD ["python", "main.py"]` | o comando que roda quando o container inicia |

**Por que copiar o `requirements.txt` antes do código?** O Docker guarda em cache o resultado de cada linha. Se você mudar só o `main.py`, ele reaproveita a instalação já feita e o build fica bem mais rápido. Se copiasse tudo de uma vez, qualquer alteração no código obrigaria a reinstalar tudo de novo.

**Repare no que não foi copiado:** a pasta `dados/`. Ela vem no próximo passo.

## Arquivo `docker-compose.yml`

```yaml
services:
  clientes:
    build: .
    image: meu-python
    container_name: meu-python
    volumes:
      # pasta local dados/  ->  /app/dados dentro do container (somente leitura)
      - ./dados:/app/dados:ro
```

**O que cada linha faz:**

| Linha | O que faz |
|---|---|
| `services:` | a lista de containers do projeto |
| `clientes:` | o nome do nosso serviço (você escolhe) |
| `build: .` | constrói a imagem usando o `Dockerfile` da pasta atual |
| `image: meu-python` | o nome que a imagem construída vai receber |
| `container_name: meu-python` | o nome do container, para aparecer bonito no `docker ps` |
| `volumes:` | o mapeamento de pastas entre a sua máquina e o container |
| `./dados:/app/dados:ro` | a pasta `dados` daqui aparece dentro do container em `/app/dados` |

O `:ro` no final significa *read only*: o container consegue **ler** o arquivo, mas não consegue alterar nem apagar nada seu.


##  Subir o container

```sh
docker compose up -d clientes

docker logs meu-python
```


Na primeira vez o Docker baixa a imagem do Python e instala o `tabulate` — você vai ver o `pip` trabalhando na tela. Nas próximas vezes ele reaproveita o cache e nem passa por essa etapa.

**Resultado esperado:**

```
Total de registros: 10
Chaves disponíveis: ['id', 'nome', 'email', 'cidade', 'estado', 'valor_compra']

| id   | nome            | email                     | cidade         | estado   | valor_compra   |
|------|-----------------|---------------------------|----------------|----------|----------------|
| 1    | Ana Souza       | ana.souza@email.com       | São Paulo      | SP       | 1250.90        |
| 2    | Bruno Lima      | bruno.lima@email.com      | Campinas       | SP       | 340.00         |
| 3    | Carla Mendes    | carla.mendes@email.com    | Rio de Janeiro | RJ       | 890.50         |
| 4    | Diego Ferreira  | diego.ferreira@email.com  | Belo Horizonte | MG       | 2100.00        |
| 5    | Elisa Nogueira  | elisa.nogueira@email.com  | Curitiba       | PR       | 75.25          |
| 6    | Felipe Ramos    | felipe.ramos@email.com    | Porto Alegre   | RS       | 1580.40        |
| 7    | Gabriela Costa  | gabriela.costa@email.com  | Salvador       | BA       | 430.00         |
| 8    | Henrique Alves  | henrique.alves@email.com  | Recife         | PE       | 999.99         |
| 9    | Isabela Martins | isabela.martins@email.com | Fortaleza      | CE       | 260.70         |
| 10   | João Pereira    | joao.pereira@email.com    | Santos         | SP       | 1875.00        |
```

Repare que **todo valor foi lido como texto**, inclusive o `id` e o `valor_compra`. O módulo `csv` não adivinha tipos: se você quiser somar os valores, vai precisar converter com `float()`.

Para limpar o container depois que ele termina:

```sh
docker compose down
```


## Rodar o script manualmente


### Entrar no container e rodar por dentro

```sh
docker compose exec clientes bash
```

O prompt muda para algo como `root@a1b2c3d4:/app#`. Você está **dentro** do container, na pasta `/app`. Explore:

```sh
ls                       # veja o que existe aqui: main.py e requirements.txt
cat dados/clientes.csv   # o arquivo que veio da sua máquina pelo volume
python main.py           # roda o script
exit                     # sai do container, sem derrubá-lo
```

Repare que o `Dockerfile` e o `docker-compose.yml` **não estão lá**. Só foi copiado o que o `COPY` mandou copiar.

### Rodar sem entrar no container

```sh
docker compose exec clientes python main.py
```

Para experimentar interativamente, o interpretador também está lá dentro:

```sh
docker compose exec clientes python
>>> from main import carregar_clientes
>>> dados = carregar_clientes('dados/clientes.csv')
>>> len(dados)
```
