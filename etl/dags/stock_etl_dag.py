from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_stock_etl',
    default_args=default_args,
    description='A simple daily ETL DAG for US and TW stocks',
    schedule_interval='0 10 * * *', # Adjust schedule based on market close timezone
    catchup=False,
    tags=['stocks'],
) as dag:

    start = DummyOperator(task_id='start')

    fetch_us = BashOperator(
        task_id='fetch_us_stocks',
        bash_command='python /opt/airflow/scripts/fetch_us_stocks.py',
        env={
            **os.environ,
            "DB_USER": "airflow",
            "DB_PASSWORD": "airflow",
            "DB_HOST": "mariadb",
            "DB_PORT": "3306",
            "DB_NAME": "stocks"
        }
    )

    fetch_tw = BashOperator(
        task_id='fetch_tw_stocks',
        bash_command='python /opt/airflow/scripts/fetch_tw_stocks.py',
        env={
            **os.environ,
            "DB_USER": "airflow",
            "DB_PASSWORD": "airflow",
            "DB_HOST": "mariadb",
            "DB_PORT": "3306",
            "DB_NAME": "stocks"
        }
    )

    end = DummyOperator(task_id='end')

    start >> [fetch_us, fetch_tw] >> end
