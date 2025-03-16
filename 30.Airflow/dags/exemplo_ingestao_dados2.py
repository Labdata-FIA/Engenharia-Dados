from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from aula_airflow.utils2 import fetch_data, filter_data, insert_data

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
def extract():
    return fetch_data()

def transform(ti):
    todos = ti.xcom_pull(task_ids='extract')
    titles = filter_data(todos)
    return titles

def load(ti):
    titles = ti.xcom_pull(task_ids='transform')
    insert_data(titles, 'mysql_default')


# Criando o DAG
with DAG(
    'exemplo_ingestao_dados2',
    default_args=default_args,
    description='Uma DAG de exemplo para ingestão de dados',
    schedule_interval='@daily',
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load
    )

    extract_task >> transform_task >> load_task
