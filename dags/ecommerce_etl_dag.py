from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from scripts.generate_data import generate_mock_data

default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 5, 15),
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'modern_ecommerce_lakehouse_pipeline',
    default_args=default_args,
    description='End-to-End ELT Pipeline for ShopBack Interview Demo',
    schedule_interval='@daily',
    catchup=False
)

# Task 1: Data Generation (Python)
generate_data_task = PythonOperator(
    task_id='generate_mock_data',
    python_callable=generate_mock_data,
    op_kwargs={'output_path': '/opt/airflow/data/bronze', 'num_records': 10000},
    dag=dag,
)

# Task 2: Spark Transformation (Bronze to Silver to Postgres)
# Sử dụng BashOperator để gọi lệnh chạy spark script bên trong container
spark_transform_task = BashOperator(
    task_id='spark_processing',
    bash_command='python /opt/airflow/dags/scripts/spark_transform.py',
    dag=dag,
)

# Task 3: dbt Run & Test (Silver to Gold)
dbt_run_and_test = BashOperator(
    task_id='dbt_transformations',
    bash_command='cd /opt/airflow/dbt_analytics && dbt run --profiles-dir . && dbt test --profiles-dir .',
    dag=dag,
)

generate_data_task >> spark_transform_task >> dbt_run_and_test