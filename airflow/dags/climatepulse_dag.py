from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def run_weather_ingestion():
    from ingestion.api_ingestion import main
    main()


def run_air_quality_ingestion():
    from ingestion.air_quality_api_ingestion import main
    main()


def run_weather_kafka_producer():
    from streaming.weather_producer import main
    main()


def run_air_quality_kafka_producer():
    from streaming.air_quality_producer import main
    main()


def run_weather_kafka_consumer():
    from processing.kafka_to_s3 import consume_weather_data
    consume_weather_data()


def run_air_quality_kafka_consumer():
    from processing.kafka_to_s3_air_quality import consume_air_quality_data
    consume_air_quality_data()


def run_weather_s3_upload():
    from processing.s3_upload_kafka_weather import upload_to_s3
    upload_to_s3()



def run_air_quality_s3_upload():
    from processing.s3_upload_kafka_air_quality import upload_to_s3
    upload_to_s3()



def run_cleaning():
    from processing.clean_data import main
    main()


def run_combining():
    from processing.combine_data import combine_data
    combine_data()


def run_transformation():
    from processing.transform_data import transform_data
    transform_data()


def run_processed_s3_upload():
    from processing.s3_upload_processed import upload_to_s3
    upload_to_s3()


with DAG(
    dag_id="climatepulse_pipeline",
    start_date=datetime(2026, 9, 28),
    schedule=None,
    catchup=False,
    tags=["climatepulse", "data-engineering"],
) as dag:

    weather_ingestion = PythonOperator(
        task_id="weather_ingestion",
        python_callable=run_weather_ingestion,
    )

    air_quality_ingestion = PythonOperator(
        task_id="air_quality_ingestion",
        python_callable=run_air_quality_ingestion,
    )

    weather_kafka_producer = PythonOperator(
        task_id="weather_kafka_producer",
        python_callable=run_weather_kafka_producer,
    )

    air_quality_kafka_producer = PythonOperator(
        task_id="air_quality_kafka_producer",
        python_callable=run_air_quality_kafka_producer,
    )

    weather_kafka_consumer = PythonOperator(
        task_id="weather_kafka_consumer",
        python_callable=run_weather_kafka_consumer,
    )

    air_quality_kafka_consumer = PythonOperator(
        task_id="air_quality_kafka_consumer",
        python_callable=run_air_quality_kafka_consumer,
    )

    weather_s3_upload = PythonOperator(
        task_id="weather_s3_upload",
        python_callable=run_weather_s3_upload,
    )

    air_quality_s3_upload = PythonOperator(
        task_id="air_quality_s3_upload",
        python_callable=run_air_quality_s3_upload,
    )

    cleaning = PythonOperator(
        task_id="cleaning",
        python_callable=run_cleaning,
    )

    combining = PythonOperator(
        task_id="combining",
        python_callable=run_combining,
    )

    transformation = PythonOperator(
        task_id="transformation",
        python_callable=run_transformation,
    )

    processed_s3_upload = PythonOperator(
        task_id="processed_s3_upload",
        python_callable=run_processed_s3_upload,
    )

    weather_ingestion >> weather_kafka_producer
    air_quality_ingestion >> air_quality_kafka_producer

    weather_kafka_producer >> weather_kafka_consumer
    air_quality_kafka_producer >> air_quality_kafka_consumer

    weather_kafka_consumer >> weather_s3_upload
    air_quality_kafka_consumer >> air_quality_s3_upload

    weather_s3_upload >> cleaning
    air_quality_s3_upload >> cleaning

    cleaning >> combining
    combining >> transformation
    transformation >> processed_s3_upload