# Stocks Worker Documentation

Welcome to the `stocks-worker` documentation directory. This folder contains the specifications and architectural plans for the ETL data pipeline.

## Table of Contents

- [ETL Pipeline Overview & Architecture](./ETL_SPEC.md) - The high-level architecture and data flow diagram of the system.
- [Airflow DAG Specifications](./AIRFLOW_SPEC.md) - Details on the Airflow scheduling and task execution flow.
- [Database Specifications](./DATABASE_SPEC.md) - The MariaDB schema design for storing tracked symbols and historical prices.

For specific implementation details regarding the Python fetch scripts (`fetch_tw_stocks.py`, `fetch_us_stocks.py`, etc.), please refer to the docstrings within the respective python source files.
