import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_path, bucket_name, object_name):
    logging.info("Initializing S3 client...")
    s3_client = boto3.client('s3',
                             aws_access_key_id='...',
                             aws_secret_access_key='...',
                             region_name='eu-central-1')
    try:
        logging.info(f"Uploading {file_path} to bucket {bucket_name} as {object_name}...")
        s3_client.upload_file(file_path, bucket_name, object_name)
        logging.info(f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
    except NoCredentialsError:
        logging.error("Credentials not available.")
        raise
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise


def upload_task():
    file_path = '/opt/airflow/data/train.json'
    bucket_name = 'mlops-news-trends'
    object_name = 'data/train.json'
    upload_to_s3(file_path, bucket_name, object_name)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG('upload_train_data_to_s3_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    start = DummyOperator(task_id='start')

    end = DummyOperator(task_id='end')

    upload_to_s3_task = PythonOperator(
        task_id='upload_to_s3_task',
        python_callable=upload_task
    )

    start >> upload_to_s3_task >> end


