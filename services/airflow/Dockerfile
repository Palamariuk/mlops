FROM apache/airflow:2.9.1-python3.8

COPY requirements.txt .

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r requirements.txt