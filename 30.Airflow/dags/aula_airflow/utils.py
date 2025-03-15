# airflow_project/aula_airflow/utils.py
import requests
import mysql.connector

def fetch_data():
    response = requests.get('https://jsonplaceholder.typicode.com/todos')
    response.raise_for_status()
    return response.json()

def filter_data(todos):
    return [todo['title'] for todo in todos if todo['completed']]

def insert_data(titles):
    conn = mysql.connector.connect(
        host="mysql",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255)
        )
    """)
    for title in titles:
        cursor.execute("INSERT INTO tb_todos (title) VALUES (%s)", (title,))
    conn.commit()
    cursor.close()
    conn.close()
