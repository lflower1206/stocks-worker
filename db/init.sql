-- db/init.sql

-- Create stocks database if it doesn't exist.
CREATE DATABASE IF NOT EXISTS stocks;
USE stocks;

-- Table to manage available pool of stocks
CREATE TABLE IF NOT EXISTS stock_list (
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(255) NOT NULL,
    market VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, market)
);

-- Table to manage symbols we are interested in tracking
CREATE TABLE IF NOT EXISTS tracked_symbols (
    symbol VARCHAR(20) NOT NULL,
    market VARCHAR(10) NOT NULL, -- 'US' or 'TW'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, market)
);

-- Table to store historical price data for the tracked symbols
CREATE TABLE IF NOT EXISTS historical_prices (
    symbol VARCHAR(20) NOT NULL,
    trade_date DATE NOT NULL,
    market VARCHAR(10) NOT NULL,
    open_price DECIMAL(10, 4),
    high_price DECIMAL(10, 4),
    low_price DECIMAL(10, 4),
    close_price DECIMAL(10, 4),
    volume BIGINT,
    PRIMARY KEY (symbol, trade_date, market),
    FOREIGN KEY (symbol, market) REFERENCES tracked_symbols(symbol, market) ON DELETE CASCADE
);
