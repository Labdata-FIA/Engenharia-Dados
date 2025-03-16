from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

# Definindo os argumentos padrão para as tarefas do DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Criando o DAG
dag = DAG(
    'exemplo_muitosimples',
    default_args=default_args,
    description='Exemplo muito simples DAG',
    schedule_interval='@daily',
)

# Definindo tarefas
start = EmptyOperator(
    task_id='start',
    dag=dag,
)

end = EmptyOperator(
    task_id='end',
    dag=dag,
)

# Definindo a ordem de execução das tarefas
start >> end
