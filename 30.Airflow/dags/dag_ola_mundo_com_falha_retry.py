from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowSkipException

# Uma DAG representa um workflow, um conjunto de tasks
with DAG(
        dag_id="ola_mundo_com_falha_retry",  # nome da DAG
        start_date=days_ago(1),  # A data em que o DAG deve começar a funcionar pela primeira vez
        schedule="0 0 * * *"  # definição de quando a DAG será executada
) as dag:
    # As Tasks são representadas por operadores
    hello = BashOperator(
        task_id="exibir_mensagem",
        bash_command="echo 'olá mundo'",
        retries=3,  # número de tentativas
        retry_delay=timedelta(seconds=10),  # intervalo entre tentativas
        execution_timeout=timedelta(seconds=10)  # tempo limite de execução
    )

    @task(retries=3, retry_delay=timedelta(seconds=10), execution_timeout=timedelta(seconds=10))
    def airflow(**context):
        if context['ti'].try_number == 3:
            print("olá mundo!!!")
        else:
            a = 2 / 0

    # Definindo a dependência entre tasks
    hello >> airflow()
