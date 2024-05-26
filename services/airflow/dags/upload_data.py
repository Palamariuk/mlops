import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime
from minio import Minio
from minio.error import S3Error


def upload_to_minio(file_path, bucket_name, object_name):
    logging.info("Initializing Minio client...")
    client = Minio(
        'minio:9000',
        access_key='minio',
        secret_key='minio123',
        secure=False
    )
    try:
        logging.info(f"Uploading {file_path} to bucket {bucket_name} as {object_name}...")
        client.fput_object(bucket_name, object_name, file_path)
        logging.info(f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
    except S3Error as e:
        logging.error(f"Error occurred: {e}")
        raise


def upload_task():
    file_path = '/opt/airflow/data/train.json'
    bucket_name = 'mybucket'
    object_name = 'data/train.json'
    upload_to_minio(file_path, bucket_name, object_name)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG('upload_to_minio_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    start = DummyOperator(task_id='start')

    end = DummyOperator(task_id='end')

    upload_to_minio_task = PythonOperator(
        task_id='upload_to_minio_task',
        python_callable=upload_task
    )

    start >> upload_to_minio_task >> end


