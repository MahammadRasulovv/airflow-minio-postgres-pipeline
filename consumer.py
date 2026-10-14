#producer daginin davami (hometask) 2-ci dagi consumer dagi kodlari yazilir
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models.param import Param
import os


@dag(
    dag_id="consumer_dag",
    start_date=days_ago(1),
    schedule=None,
    catchup=False,
) as dag:
