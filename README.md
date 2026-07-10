## Why this project?

Most finance analytics projects only provide dashboards.

This platform delivers an end-to-end analytics solution including ETL, Data Warehouse, transformations, data quality checks and interactive dashboards.

Designed for production-ready deployments.


# Finance Analytics Platform

Production-ready finance analytics platform built with PostgreSQL, Apache Airflow, dbt and Apache Superset.

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

Yahoo Finance
↓
Python ETL
↓
PostgreSQL
↓
dbt
↓
Apache Superset


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




