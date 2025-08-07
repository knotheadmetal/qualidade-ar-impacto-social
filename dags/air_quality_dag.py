from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Adicionar o diretório raiz do projeto ao sys.path para que os módulos possam ser importados
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, project_root)

from src.ingestao.ingest_data import main as ingest_main
from src.transformacao.transform_data import main as transform_main

def _ingest_data():
    ingest_main()

def _transform_data():
    transform_main()

with DAG(
    dag_id='air_quality_etl_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=timedelta(days=1), # Executa diariamente
    catchup=False,
    tags=['air_quality', 'etl', 'portfolio'],
) as dag:
    ingest_task = PythonOperator(
        task_id='ingest_air_quality_data',
        python_callable=_ingest_data,
    )

    transform_task = PythonOperator(
        task_id='transform_air_quality_data',
        python_callable=_transform_data,
    )

    ingest_task >> transform_task

