### Passo a Passo: Criando um Projeto com Poetry

#### 1. Instalando o Poetry

Antes de começar, você precisa instalar o Poetry. Se ainda não o tem instalado, siga os passos abaixo:

##### a. Via Instalador Oficial

Abra um terminal e execute o seguinte comando:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

##### b. Adicionando o Poetry ao PATH

Depois da instalação, você pode adicionar o Poetry ao seu PATH, caso ele não tenha sido adicionado automaticamente. Adicione a linha abaixo ao seu arquivo de configuração do
shell (`.bashrc`, `.zshrc`, etc.):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

#### 2. Criando um Novo Projeto com Poetry

##### a. Navegue até o Diretório Desejado

Abra um terminal e navegue até o diretório onde deseja criar seu projeto:

```bash
cd /caminho/do/diretorio
```

##### b. Inicialize um Novo Projeto

Execute o comando abaixo para criar um novo projeto com o Poetry:

```bash
poetry new nome_do_projeto
```

Este comando criará uma estrutura de diretórios semelhante a esta:

```plaintext
nome_do_projeto/
├── pyproject.toml
├── README.rst
├── nome_do_projeto
│   └── __init__.py
└── tests
    └── __init__.py
```

#### 3. Navegando pelo Projeto

Entre no diretório do projeto:

```bash
cd nome_do_projeto
```

#### 4. Estrutura do Arquivo `pyproject.toml`

O arquivo `pyproject.toml` é o coração do seu projeto Poetry. Ele contém informações sobre seu projeto e suas dependências.

##### a. Exemplo de `pyproject.toml`

Aqui está um exemplo básico do que você pode encontrar no seu `pyproject.toml`:

```toml
[tool.poetry]
name = "nome_do_projeto"
version = "0.1.0"
description = ""
authors = ["Seu Nome <seu.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.dev-dependencies]
pytest = "^6.2.4"
```

#### 5. Adicionando Dependências

##### a. Dependências de Produção

Para adicionar uma dependência de produção, use o comando `poetry add`:

```bash
poetry add nome_da_dependencia
```

##### b. Dependências de Desenvolvimento

Para adicionar uma dependência de desenvolvimento, use o comando `poetry add` com a flag `--dev`:

```bash
poetry add --dev nome_da_dependencia
```

#### 6. Instalando Dependências

Para instalar todas as dependências listadas no `pyproject.toml`, use o comando `poetry install`:

```bash
poetry install
```

#### 7. Usando Ambientes Virtuais

O Poetry cria e gerencia automaticamente um ambiente virtual para seu projeto. Para ativar o ambiente virtual, use o comando `poetry shell`:

```bash
poetry shell
```

#### 8. Executando Scripts

Você pode executar scripts Python no contexto do ambiente virtual gerenciado pelo Poetry. Por exemplo, para executar um script `main.py`, use o comando:

```bash
poetry run python nome_do_projeto/main.py
```

#### 9. Configurando Scripts no `pyproject.toml`

Você pode configurar scripts personalizados no `pyproject.toml` para facilitar a execução de tarefas comuns. Adicione uma seção `[tool.poetry.scripts]`:

```toml
[tool.poetry.scripts]
start = "nome_do_projeto.main:main"
```

Agora, você pode executar o script configurado com o comando:

```bash
poetry run start
```

### Resumo dos Comandos Poetry

- **Instalar Poetry:**
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

- **Criar um Novo Projeto:**
  ```bash
  poetry new nome_do_projeto
  ```

- **Adicionar Dependências:**
  ```bash
  poetry add nome_da_dependencia
  ```

- **Adicionar Dependências de Desenvolvimento:**
  ```bash
  poetry add --dev nome_da_dependencia
  ```

- **Instalar Dependências:**
  ```bash
  poetry install
  ```

- **Ativar o Ambiente Virtual:**
  ```bash
  poetry shell
  ```

- **Executar um Script:**
  ```bash
  poetry run python script.py
  ```

