import sys
sys.path.append("/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

from etl.ticker import load_tickers
from etl.company import load_company
from etl.stock_prices import load_stock_prices
from etl.financials import load_financials
from etl.income_statement import load_income_statement
from etl.balance_sheet import load_balance_sheet
from etl.cash_flow import load_cash_flow
from etl.recommendations import load_recommendations
from etl.earnings_dates import load_earnings_dates


with DAG(
    dag_id="finance_dwh",
    start_date=datetime(2026, 6, 28),
    schedule=None,
    catchup=False,
    max_active_runs=1,
) as dag:

    load_tickers_task = PythonOperator(
        task_id="load_tickers",
        python_callable=load_tickers
    )

    load_company_task = PythonOperator(
        task_id="load_company",
        python_callable=load_company
    )

    load_stock_prices_task = PythonOperator(
        task_id="load_stock_prices",
        python_callable=load_stock_prices
    )

    load_financials_task = PythonOperator(
        task_id="load_financials",
        python_callable=load_financials
    )

    load_income_statement_task = PythonOperator(
        task_id="load_income_statement",
        python_callable=load_income_statement
    )

    load_balance_sheet_task = PythonOperator(
        task_id="load_balance_sheet",
        python_callable=load_balance_sheet
    )

    load_cash_flow_task = PythonOperator(
        task_id="load_cash_flow",
        python_callable=load_cash_flow
    )

    load_recommendations_task = PythonOperator(
        task_id="load_recommendations",
        python_callable=load_recommendations
    )

    load_earnings_dates_task = PythonOperator(
        task_id="load_earnings_dates",
        python_callable=load_earnings_dates
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/airflow/finance_dwh && dbt build"
    )

    load_tickers_task >> [
        load_company_task,
        load_stock_prices_task,
        load_financials_task,
        load_income_statement_task,
        load_balance_sheet_task,
        load_cash_flow_task,
        load_recommendations_task,
        load_earnings_dates_task
    ] >> dbt_build