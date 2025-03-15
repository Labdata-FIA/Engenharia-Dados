from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Uma DAG representa um workflow, um conjunto de task
with DAG(
        dag_id="ola_mundo_data_backfill",  # nome da DAG
        start_date=datetime(2024, 9, 1),  # A data em que o DAG deve começar a funcionar pela primeira vez
        end_date=datetime(2024, 9, 6),  # A data em que o DAG deve encerrar o funcionamento
        schedule_interval="@daily",  # timedelta oferece a capacidade de usar programações baseadas em frequência.
        catchup=False  # habilitar o backfill, True = será executado o passado nao execudado
) as dag:
    # As Tasks são representadas por operadores
    hello = BashOperator(task_id="exibir_mensagem", bash_command="echo 'olá mundo'")

    def airflow_com_data(data):
        print(f"[arg data]={data}, airflow!!!")


    airflow = PythonOperator(
        task_id="airflow_com_data",
        python_callable=airflow_com_data,
        op_kwargs={
            "data": "{{ ds }}"
        }
    )
    hello >> airflow
