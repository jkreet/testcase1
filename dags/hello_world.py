from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

def print_date():
    f = open("/usr/local/airflow/tmp/dates.txt", "a")
    f.write(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
    f.close()

dag = DAG('print_date', description='Simple tutorial DAG',
          schedule_interval='* 12 * * *',
          start_date=datetime(2020, 3, 20), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

print_operator = PythonOperator(task_id='print_task', python_callable=print_date, dag=dag)

dummy_operator >> print_operator