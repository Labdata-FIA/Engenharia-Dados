# Laboratório Airflow

Este repositório contém uma configuração do Apache Airflow utilizando Docker e Docker Compose, com integração ao MySQL para armazenamento de dados. O projeto inclui DAGs de exemplo para ingestão de dados a partir de uma API pública e armazenamento no banco de dados MySQL.

## Requisitos Mínimos

- Docker (versão 20.10 ou superior)
- Docker Compose (versão 1.29 ou superior)
- Python (versão 3.9 ou superior, se desejar executar scripts localmente)
- Acesso à internet para baixar imagens e dependências

## Estrutura do Projeto

```
30.Airflow/
├── dags/
│   └── __init__.py
├───── aula_airflow/
│      └── __init__.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env
├── poetry.lock
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Inicializar o Ambiente

Para inicializar o serviço, utilize o comando:

```shell
docker compose up mysql_airflow postgres_airflow webserver scheduler
```

> *Caso não funcione o comando acima*, utilize `docker-compose` no lugar de `docker compose`

Usar `Ctrl+C` para parar a execução do ambiente

## Parar remover os containers do Ambiente

Para parar todos os contêineres do ambiente, utilize o comando:
```shell
docker compose down mysql_airflow postgres_airflow webserver scheduler
```

## Criar o Usuário para Fazer Login no Airflow

Após inicializar o serviço, crie um usuário admin para acessar a interface do Airflow:

- Executar o comando abaixo no terminal

```shell
docker compose exec webserver airflow users create \
    --username admin \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email admin@example.com \
    --password admin
```

## Configurar a Conexão MySQL no Airflow

### Utilizando interface gráfica

1. Acesse a interface do Airflow em [http://localhost:8080](http://localhost:8080) e faça login com as credenciais criadas.
2. Vá para `Admin` -> `Connections`.
3. Clique em `+` para adicionar uma nova conexão e configure os campos conforme abaixo:

- **Conn Id**: `mysql_default`
- **Conn Type**: `MySQL`
- **Host**: `mysql_airflow`
- **Schema**: `airflow`
- **Login**: `airflow`
- **Password**: `airflow`
- **Port**: `3306`

### Utilizando linha de comando

```shell
docker compose exec webserver \
    airflow connections delete 'mysql_default'

docker compose exec webserver \
    airflow connections add 'mysql_default' --conn-uri 'mysql://airflow:airflow@mysql_airflow:3306/airflow'
```

## Monitoramento de Logs

Certifique-se de que a configuração acima esteja correta para evitar problemas de acesso aos logs.


