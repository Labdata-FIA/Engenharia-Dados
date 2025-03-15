import logging
import sys
import tempfile
import time
from pprint import pprint

import airflow.utils.dates
from airflow import DAG
from airflow.decorators import task

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable

BASE_DIR = tempfile.gettempdir()

@task(task_id="print_the_context")
def _print_context(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    pprint(kwargs)
    print(ds)
    return "Whatever you return gets printed in the logs"


with DAG(
        dag_id="debug_variables",
        start_date=airflow.utils.dates.days_ago(1),
        schedule_interval="@daily",
) as dag:
    run_this = _print_context()
