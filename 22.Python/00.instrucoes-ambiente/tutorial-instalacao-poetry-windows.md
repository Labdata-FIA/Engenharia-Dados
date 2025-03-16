### Passo a Passo: Criando um Projeto com Poetry no Windows

#### 1. Instalando o Poetry

##### a. Via Instalador Oficial

Abra o **PowerShell** como Administrador e execute o seguinte comando:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

##### b. Adicionando o Poetry ao PATH

Se o instalador do Poetry não adicionar automaticamente o Poetry ao seu PATH, você pode fazer isso manualmente:

1. **Abra o PowerShell ou Prompt de Comando como Administrador**.
2. **Verifique onde o Poetry foi instalado**. Geralmente, é na pasta do usuário: `C:\Users\<seu_usuario>\AppData\Roaming\Python\Scripts`.

Para adicionar esse caminho ao PATH, execute o seguinte comando no PowerShell:

```powershell
$env:Path += ";C:\Users\<seu_usuario>\AppData\Roaming\Python\Scripts"
```

Ou adicione manualmente o caminho no painel de Controle do Windows:
- Vá para **Painel de Controle > Sistema e Segurança > Sistema > Configurações avançadas do sistema > Variáveis de ambiente**.
- Na seção **Variáveis do sistema**, selecione a variável **Path** e clique em **Editar**.
- Adicione `C:\Users\<seu_usuario>\AppData\Roaming\Python\Scripts` ao final da lista.

#### 2. Criando um Novo Projeto com Poetry

##### a. Navegue até o Diretório Desejado

Abra o PowerShell ou o Prompt de Comando e navegue até o diretório onde deseja criar seu projeto:

```powershell
cd C:\caminho\do\diretorio
```

##### b. Inicialize um Novo Projeto

Execute o comando abaixo para criar um novo projeto com o Poetry:

```powershell
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

```powershell
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

```powershell
poetry add nome_da_dependencia
```

##### b. Dependências de Desenvolvimento

Para adicionar uma dependência de desenvolvimento, use o comando `poetry add` com a flag `--dev`:

```powershell
poetry add --dev nome_da_dependencia
```

#### 6. Instalando Dependências

Para instalar todas as dependências listadas no `pyproject.toml`, use o comando `poetry install`:

```powershell
poetry install
```

#### 7. Usando Ambientes Virtuais

O Poetry cria e gerencia automaticamente um ambiente virtual para seu projeto. Para ativar o ambiente virtual, use o comando `poetry shell`:

```powershell
poetry shell
```

#### 8. Executando Scripts

Você pode executar scripts Python no contexto do ambiente virtual gerenciado pelo Poetry. Por exemplo, para executar um script `main.py`, use o comando:

```powershell
poetry run python nome_do_projeto\main.py
```

#### 9. Configurando Scripts no `pyproject.toml`

Você pode configurar scripts personalizados no `pyproject.toml` para facilitar a execução de tarefas comuns. Adicione uma seção `[tool.poetry.scripts]`:

```toml
[tool.poetry.scripts]
start = "nome_do_projeto.main:main"
```

Agora, você pode executar o script configurado com o comando:

```powershell
poetry run start
```

### Resumo dos Comandos Poetry

- **Instalar Poetry:**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

- **Criar um Novo Projeto:**
```powershell
poetry new nome_do_projeto
```

- **Adicionar Dependências:**
```powershell
poetry add nome_da_dependencia
```

- **Adicionar Dependências de Desenvolvimento:**
```powershell
poetry add --dev nome_da_dependencia
```

- **Instalar Dependências:**
```powershell
poetry install
```

- **Ativar o Ambiente Virtual:**
```powershell
poetry shell
```

- **Executar um Script:**
```powershell
poetry run python script.py
```
