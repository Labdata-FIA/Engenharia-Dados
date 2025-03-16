from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.jdbc.operators.jdbc import JdbcOperator
from airflow.utils.dates import days_ago
from aula_airflow.utils3 import fetch_data, filter_data, insert_data

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
    return filter_data(todos)


def generate_insert_sql(ti):
    todos = ti.xcom_pull(task_ids='transform')
    values = ", ".join([f"('{todo}')" for todo in todos])
    return f"INSERT INTO tb_todos (title) VALUES {values};"


# Criando o DAG
with DAG(
        'exemplo_ingestao_dados3',
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

    create_table_task = JdbcOperator(
        task_id='create_table',
        jdbc_conn_id='mysql_default',
        sql="""
        CREATE TABLE IF NOT EXISTS tb_todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255)
        );
    """)

    generate_insert_sql_task = PythonOperator(
        task_id='generate_insert_sql',
        python_callable=generate_insert_sql
    )

    insert_data_task = JdbcOperator(
        task_id='insert_data',
        jdbc_conn_id='mysql_default',
        sql="""
        {{ task_instance.xcom_pull(task_ids='generate_insert_sql') }}
    """)

extract_task >> transform_task >> create_table_task >> generate_insert_sql_task >> insert_data_task
