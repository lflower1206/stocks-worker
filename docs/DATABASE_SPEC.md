# Stocks Worker - Database Specification

Database Name: `stocks`

## 1. `stock_list` Table

Contains list of all available symbols for selection.

- `symbol` (VARCHAR 20, PK)
- `name` (VARCHAR 255)
- `market` (VARCHAR 10, PK) - 'US' or 'TW'
- `is_active` (BOOLEAN) - Default TRUE.
- `updated_at` (TIMESTAMP)

## 2. `tracked_symbols` Table

Tracks which symbols are actively monitored.

- `symbol` (VARCHAR 20, PK)
- `market` (VARCHAR 10, PK) - 'US' or 'TW'
- `is_active` (BOOLEAN) - Default TRUE.
- `created_at` (TIMESTAMP)

## 2. `historical_prices` Table

Stores daily OHLCV (Open, High, Low, Close, Volume) data.

- `symbol` (VARCHAR 20, PK, FK)
- `trade_date` (DATE, PK)
- `market` (VARCHAR 10, PK, FK)
- `open_price`, `high_price`, `low_price`, `close_price` (DECIMAL 10, 4)
- `volume` (BIGINT)
