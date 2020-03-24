from clickhouse_driver import Client
from datetime import datetime
import json
import codecs
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

server_addr = 'clickhouse'

def make_table(server_addr):
    try:
        client = Client(server_addr)
        query = 'CREATE DATABASE IF NOT EXISTS user'
        client.execute(query)
        print('DB created')

        query = 'CREATE TABLE IF NOT EXISTS user.sessions \
        (\
            ts Int64,\
            userId String,\
            sessionId Int16,\
            page String,\
            auth String,\
            method String,\
            status Int16,\
            level String,\
            itemInSession Int16,\
            location String,\
            userAgent String,\
            lastName String,\
            firstName String,\
            registration Int64,\
            gender String,\
            artist String,\
            song String,\
            length Float32\
        )\
        ENGINE = MergeTree() \
        PARTITION BY ts \
        ORDER BY (ts, intHash32(sessionId)) \
        SAMPLE BY intHash32(sessionId)'
        client.execute(query)
        print('Table created')
    except Client as e:
        print(e)
    except Exception as e:
        print(e)

def format_data(filename):
    attrs = [
        'ts',
        'userId',
        'sessionId',
        'page',
        'auth',
        'mod',
        'status',
        'level',
        'itemInSession',
        'location',
        'userAgent',
        'lastName',
        'firstName',
        'registration',
        'gender',
        'artist',
        'song',
        'length'
    ]

    data = ''
    for line in codecs.open(filename, "r", "utf_8" ):
        data_list = []
        json_decode = json.loads(line)
        for attr in attrs:
            try:
                data_list.append(json_decode[attr])
            except:
                data_list.append('')
        data = data + '\t'.join(str(e) for e in data_list) + "\n"

    return data



def insert_data():
    make_table(server_addr)

    query = "INSERT INTO user.sessions FORMAT TabSeparated\n" + format_data('event-data.json')

    try:
        client = Client(server_addr)
        result = client.execute(query)
        print(result)
    except Client as e:
        print(e)
    except Exception as e:
        print(e)

dag = DAG('insert_data', description='Insert data to clickhouse',
          schedule_interval='* 1 * * *',
          start_date=datetime(2020, 3, 20), catchup=False)

insert_operator = PythonOperator(task_id='insert_task', python_callable=insert_data, dag=dag)

insert_operator