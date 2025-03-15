from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from aula_airflow.utils import fetch_data, filter_data, insert_data

# Definindo os argumentos padrão para as tarefas do DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Função que combina todas as etapas do pipeline de ingestão de dados
def ingest_data():
    todos = fetch_data()
    titles = filter_data(todos)
    insert_data(titles)

# Criando o DAG
dag = DAG(
    'exemplo_ingestao_dados',
    default_args=default_args,
    description='Uma DAG de exemplo para ingestão de dados',
    schedule_interval='@daily',
)

# Definindo a tarefa
ingest_task = PythonOperator(
    task_id='ingest_data',
    python_callable=ingest_data,
    dag=dag,
)

# Definindo a ordem de execução das tarefas
ingest_task
