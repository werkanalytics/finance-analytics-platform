# Finance Analytics Platform

An end-to-end financial data engineering and analytics platform built with Python, PostgreSQL, Apache Airflow, dbt, Docker, and Apache Superset.

## Overview

Finance Analytics Platform is a personal data engineering project designed to collect, transform, model, and analyze financial market data.

The platform uses Python-based ETL pipelines to ingest financial data into PostgreSQL. Apache Airflow orchestrates the pipelines, while dbt handles data transformation and warehouse modeling. Analytical datasets are then exposed through Apache Superset for visualization and exploration.

## Architecture

The platform follows an end-to-end analytics pipeline:

Data Sources  
↓  
Python ETL  
↓  
Apache Airflow  
↓  
PostgreSQL  
↓  
dbt  
↓  
Staging → DWH → Data Marts  
↓  
Apache Superset

## Tech Stack

- **Python** — data extraction and loading
- **PostgreSQL** — data warehouse
- **Apache Airflow** — workflow orchestration
- **dbt** — transformation and data modeling
- **Apache Superset** — analytics and dashboards
- **Docker** — containerized development environment

## Data Sources

The platform currently processes financial datasets including:

- Stock prices
- Company information
- Income statements
- Balance sheets
- Cash flow statements
- Earnings dates
- Analyst recommendations

## ETL & Orchestration

Python ETL modules handle data ingestion and loading into PostgreSQL.

Apache Airflow orchestrates the pipeline and coordinates the ingestion tasks with downstream dbt transformations.

## Data Warehouse Architecture

The dbt project follows a layered modeling approach:

### Staging

Raw source data is cleaned and standardized before warehouse modeling.

### DWH

The warehouse contains lookup and transactional models for companies, tickers, financial statements, stock prices, and other financial datasets.

### Data Marts

Business-oriented analytical models are built on top of the warehouse for reporting and visualization.

## Analytics

Apache Superset is used as the BI and visualization layer of the platform.

The analytical layer is designed to support company, market, category, and thematic analysis.

## Project Structure

```text
finance-analytics-platform/
├── dags/                 # Airflow DAGs
├── etl/                  # Python ETL pipelines
├── models/
│   ├── staging/          # dbt staging models
│   ├── dwh/              # warehouse models
│   └── mart/             # analytical marts
├── macros/               # dbt macros
├── tests/                # custom dbt tests (planned)
├── Dockerfile
├── Dockerfile.superset
├── docker-compose.yaml
└── docker-compose-superset.yml
