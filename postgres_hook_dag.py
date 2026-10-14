
from datetime import datetime
import logging

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


logger = logging.getLogger(__name__)


# TASK 1: Connect to PostgreSQL and execute SELECT 1

def test_postgres_connection():

    logger.info("Connecting to PostgreSQL")

    # Create PostgreSQL Hook using Airflow Connection
    postgres_hook = PostgresHook(
        postgres_conn_id="postgres_exam"
    )

    logger.info("Executing SELECT 1 query")

    result = postgres_hook.get_first("SELECT 1;")

    logger.info("Displaying query result")

    logger.info("Query result: %s", result[0])

    if result[0] != 1:
        raise ValueError("PostgreSQL query returned wrong result")

    logger.info("SUCCESS: PostgreSQL connection works")
    logger.info("SUCCESS: SELECT 1 returned 1!")


# DAG DEFINITION

with DAG(
    dag_id="postgres_hook_task",
    description="PostgreSQL connection test using PostgresHook",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["exam", "postgres", "hook"],
) as dag:

    postgres_test = PythonOperator(
        task_id="test_postgres_connection",
        python_callable=test_postgres_connection,
    )