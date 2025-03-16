import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
        dag_id="example_jinja",
        start_date=airflow.utils.dates.days_ago(1),
        schedule_interval="@hourly",
) as dag:
    BashOperator(
        task_id="get_data",
        bash_command=(
            "curl -o /tmp/wikipageviews.gz "
            "https://dumps.wikimedia.org/other/pageviews/"
            "{{ dag_run.logical_date.year }}/"
            "{{ dag_run.logical_date.year }}-"
            "{{ '{:02}'.format(dag_run.logical_date.month) }}/"
            "pageviews-{{ dag_run.logical_date.year }}"
            "{{ '{:02}'.format(dag_run.logical_date.month) }}"
            "{{ '{:02}'.format(dag_run.logical_date.day) }}-"
            "{{ '{:02}'.format(dag_run.logical_date.hour) }}0000.gz"
        )
    )
