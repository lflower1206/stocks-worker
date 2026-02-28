# Stocks Worker - ETL Pipeline Specification

## 1. System Overview

The Stocks Worker is a data pipeline application that fetches historical stock prices for US and Taiwan (TW) markets and stores them in a relational database. It utilizes **Apache Airflow** for scheduling and orchestration, **MariaDB** for data storage, and **yfinance** for fetching Yahoo Finance data.

## 2. Architecture & Infrastructure

- **Deployment**: Managed via `docker-compose.yml`.
- **Services**:
  - `mariadb`: MariaDB 11.4 database instance.
  - `airflow-webserver` & `airflow-scheduler`: Airflow components (image `apache/airflow:3.1.7-python3.12`) with `LocalExecutor`.
- **Volumes mapped**:
  - `etl/dags`, `etl/logs`, `etl/plugins`, `etl/scripts` to `/opt/airflow/...`
  - `db/init.sql` to `/docker-entrypoint-initdb.d/` for database initialization.

## 3. Data Flow

```mermaid
graph TD
    subgraph Airflow Scheduler
        A(daily_stock_etl DAG)
        A --> Tickers[fetch_stock_tickers.py]
        Tickers --> B[fetch_us_stocks.py]
        Tickers --> C[fetch_tw_stocks.py]
    end

    subgraph Data Sources
        Tickers -- "SEC/TWSE Open API" --> API[Public APIs]
        B -- "Downloads 1mo period" --> YF[Yahoo Finance API]
        C -- "Downloads 1mo period" --> YF
    end

    subgraph Python Processing
        API -- "JSON List" --> T_Proc[Data Transform]
        YF -- "Raw Data" --> B_Proc[Data Transform & Pydantic Validation]
        YF -- "Raw Data" --> C_Proc[Data Transform & Pydantic Validation]

        Tickers -.-> T_Proc
        B -.-> B_Proc
        C -.-> C_Proc
    end

    subgraph MariaDB
        T_Proc -- "SQLAlchemy Upsert" --> DB[(stocks DB)]
        B_Proc -- "SQLAlchemy Upsert" --> DB
        C_Proc -- "SQLAlchemy Upsert" --> DB
        DB -.-> S[stock_list]
        DB -.-> T[tracked_symbols]
        DB -.-> H[historical_prices]
    end
```
