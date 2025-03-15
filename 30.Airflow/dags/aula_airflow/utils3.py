# airflow_project/aula_airflow/utils.py
import requests
from airflow.hooks.base import BaseHook
import mysql.connector
import logging

# Configurando o logging
# logging = logging.getlogging()
# logging.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logging.addHandler(handler)

def fetch_data():
    logging.info('Fetching data from https://jsonplaceholder.typicode.com/todos')
    response = requests.get('https://jsonplaceholder.typicode.com/todos')
    response.raise_for_status()
    data = response.json()
    logging.info('Fetched %d records', len(data))
    return data

def filter_data(todos):
    logging.info('Filtering data')
    filtered_todos = [todo['title'] for todo in todos if todo['completed']]
    logging.info('Filtered down to %d completed records', len(filtered_todos))
    return filtered_todos

def insert_data(titles, mysql_conn_id):
    logging.info('Inserting data into MySQL database')
    connection = BaseHook.get_connection(mysql_conn_id)
    conn = mysql.connector.connect(
        host=connection.host,
        database=connection.schema,
        user=connection.login,
        password=connection.password,
        port=connection.port
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255)
        )
    """)
    logging.info('Created table tb_todos if it did not exist')
    for title in titles:
        cursor.execute("INSERT INTO tb_todos (title) VALUES (%s)", (title,))
    conn.commit()
    logging.info('Inserted %d records into tb_todos', len(titles))
    cursor.close()
    conn.close()
