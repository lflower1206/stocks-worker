# Stocks Worker - Airflow DAG Specification

## 1. `daily_stock_etl` DAG

**DAG Name**: `daily_stock_etl`

- **Schedule**: `0 10 * * *` (Daily at 10 AM UTC)
- **Tasks**:
  1. `start` (EmptyOperator)
  2. `fetch_stock_tickers` (BashOperator running `fetch_stock_tickers.py`)
  3. `fetch_us_stocks` (BashOperator running `fetch_us_stocks.py`)
  4. `fetch_tw_stocks` (BashOperator running `fetch_tw_stocks.py`)
  5. `end` (EmptyOperator)
- **Execution Flow**: `start >> fetch_stock_tickers >> [fetch_us, fetch_tw] >> end`
