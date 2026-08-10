FROM apache/airflow:2.9.3

USER airflow

RUN pip install --no-cache-dir \
    "apache-airflow==2.9.3" \
    "dbt-core==1.8.7" \
    "dbt-postgres==1.8.2" \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.12.txt"