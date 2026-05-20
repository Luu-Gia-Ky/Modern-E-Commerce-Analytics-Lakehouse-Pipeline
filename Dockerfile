FROM apache/airflow:2.7.2-python3.10

USER root
# Cài đặt các thư viện hệ thống và Java 17 JRE (cần thiết cho PySpark 3.5.x)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    openjdk-17-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow
# Cài đặt các thư viện Python
RUN pip install --no-cache-dir dbt-postgres faker pyspark psycopg2-binary
