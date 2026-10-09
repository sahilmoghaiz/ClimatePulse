
FROM apache/airflow:3.3.2

COPY airflow/requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY airflow/dags/ /opt/airflow/dags/
COPY ingestion/ /opt/airflow/ingestion/
COPY streaming/ /opt/airflow/streaming/
COPY processing/ /opt/airflow/processing/
COPY config/ /opt/airflow/config/

RUN mkdir -p /opt/airflow/data/raw /opt/airflow/data/staging /opt/airflow/data/processed
# Make project packages importable in Airflow task processes
ENV PYTHONPATH="/opt/airflow"
