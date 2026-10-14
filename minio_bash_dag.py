
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


MINIO_CONFIG_DIR = "/opt/airflow/files/.mc"

SOURCE_FILE = "/opt/airflow/dags/bronze.py"
MINIO_DESTINATION = "local/matrix/test_bash/bronze.py"


with DAG(
    dag_id="minio_bash_task",
    description="Upload bronze.py to MinIO using BashOperator",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["exam", "bash", "minio"],
) as dag:

    # TASK 1: Configure MinIO connection

    configure_minio = BashOperator(
        task_id="configure_minio",
        bash_command="""
        set -e

        echo "Step 1: Creating directory..."

        mkdir -p /tmp/matrix
        mkdir -p "$MC_CONFIG_DIR"

        echo "Step 2: Configuring MinIO alias..."

        mc alias set local \
            http://minio:9000 \
            "$MINIO_ROOT_USER" \
            "$MINIO_ROOT_PASSWORD"

        echo "Step 3: Checking MinIO connection..."

        mc ls local/matrix

        echo "SUCCESS: MinIO configured!"
        """,
        env={
            "MC_CONFIG_DIR": MINIO_CONFIG_DIR,
        },
        append_env=True,
    )

    # TASK 2: Upload bronze.py to MinIO

    upload_bronze = BashOperator(
        task_id="upload_bronze",
        bash_command=f"""
        set -e

        echo "Step 1: Checking source file..."

        test -f "{SOURCE_FILE}"

        echo "Step 2: Uploading bronze.py..."

        mc cp \
            "{SOURCE_FILE}" \
            "{MINIO_DESTINATION}"

        echo "SUCCESS: bronze.py uploaded to MinIO!"
        """,
        env={
            "MC_CONFIG_DIR": MINIO_CONFIG_DIR,
        },
        append_env=True,
    )

    # TASK 3: List and verify uploaded file

    verify_upload = BashOperator(
        task_id="verify_upload",
        bash_command="""
        set -e

        echo "Step 1: Listing files..."

        mc ls local/matrix/test_bash/

        echo "Step 2: Verifying bronze.py..."

        mc stat local/matrix/test_bash/bronze.py

        echo "SUCCESS: bronze.py exists in MinIO!"
        """,
        env={
            "MC_CONFIG_DIR": MINIO_CONFIG_DIR,
        },
        append_env=True,
    )

    # TASK DEPENDENCIES

    configure_minio >> upload_bronze >> verify_upload
