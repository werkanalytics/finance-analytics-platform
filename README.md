## Why this project?

Most finance analytics projects only provide dashboards.

This platform delivers an end-to-end analytics solution including ETL, Data Warehouse, transformations, data quality checks and interactive dashboards.

Designed for production-ready deployments.


# Finance Analytics Platform

End-to-end financial analytics platform for ingesting, transforming, modeling and visualizing financial data using PostgreSQL, Airflow, dbt and Superset.

---

## Overview

Finance Analytics Platform is an end-to-end modern data platform designed for financial analytics and reporting.

The platform automates data ingestion, transformation, warehousing and dashboard creation using modern data engineering tools.

---

## Features

- Automated ETL Pipelines
- Data Warehouse
- Data Modeling with dbt
- Interactive Dashboards
- Data Quality Checks
- Docker Deployment
- Yahoo Finance Integration
- World Bank Integration

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| PostgreSQL | Data Warehouse |
| Python | ETL |
| Apache Airflow | Workflow Orchestration |
| dbt | Data Transformation |
| Apache Superset | Dashboards |
| Docker | Deployment |


## Architecture

<img width="1536" height="1024" alt="dwh_mimari" src="https://github.com/user-attachments/assets/edb45501-4dcf-4bce-ae69-8cab648eb81e" />



## Data Source

  Yahoo Finance
  World Bank
  (ileride)
SEC

FRED

ECB


## Data Model

src
↓
stg
↓
dim
↓
fact
↓
mart

dbt manages model dependencies and provides end-to-end lineage from raw financial data sources to analytical marts.

<img width="1865" height="752" alt="dbt-dag" src="https://github.com/user-attachments/assets/bba47987-50c0-48bd-a33e-eb255c37078c" />

Apache Airflow Diagram:
<img width="1551" height="734" alt="image" src="https://github.com/user-attachments/assets/016cf708-2841-4bcf-8d7b-f170899a90c0" />



# Dashboard

Finance Overview
Market Summary
Company Details
Revenue Analysis

# Installation

git clone
docker compose up
localhost

## Project Structure

etl/

dbt/

docker/

superset/

docs/

## Roadmap

✅ ETL
✅ Warehouse
✅ Dashboard
⬜ LLM

## Screenshots

## Documentation

Installation
Architecture
ETL
Dashboard
FAQ

## License

MIT
Apache
Commercial

## Contact

GitHub
Instagram
Website




