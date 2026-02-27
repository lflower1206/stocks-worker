"""
Fetch US Stocks (`fetch_us_stocks.py`)

1. Query Active Symbols: Selects symbols from `tracked_symbols` where `market = 'US'` and `is_active = TRUE`.
2. Fetch Data: Uses `yfinance.download()` with `period="1mo"`. (1 month lookback ensures missing or updated data from the recent past is seamlessly upserted).
3. Transform & Validate: Converts pandas dataframe rows into list of dicts, validating each row via the Pydantic model.
4. Load: Upserts the validated data to the `historical_prices` table.
"""
import sys
import logging
import yfinance as yf
from datetime import datetime, date
from db_utils import get_session, upsert_historical_prices
from models import DailyStockPrice
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_active_us_symbols(session):
    result = session.execute(
        text("SELECT symbol FROM tracked_symbols WHERE market = 'US' AND is_active = TRUE")
    )
    return [row[0] for row in result.fetchall()]

def fetch_us_stocks():
    session = get_session()
    symbols = get_active_us_symbols(session)
    
    if not symbols:
        logger.info("No active US symbols found.")
        return

    logger.info(f"Fetching data for US symbols: {symbols}")
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    # Fetch a reasonable chunk, e.g., last 30 days if running daily, 
    # to ensure any delayed records are covered by the UPSERT.
    # Alternatively, you could fetch "max" on first run. For a daily cron, "1mo" or "1d" is typical.
    data = yf.download(symbols, period="1mo", group_by="ticker", threads=True, auto_adjust=False)
    
    prices_data_dicts = []
    
    # yfinance output format varies depending on single vs multiple tickers.
    if len(symbols) == 1:
        # Standard dataframe
        ticker = symbols[0]
        data = data.dropna()
        for idx, row in data.iterrows():
            trade_date = idx.date() if isinstance(idx, datetime) else idx.to_pydatetime().date()
            prices_data_dicts.append({
                'symbol': ticker,
                'trade_date': trade_date,
                'market': 'US',
                'open_price': float(row['Open']),
                'high_price': float(row['High']),
                'low_price': float(row['Low']),
                'close_price': float(row['Close']),
                'volume': int(row['Volume']),
            })
    else:
        # Multi-index dataframe
        for ticker in symbols:
            try:
                ticker_data = data[ticker].dropna()
                for idx, row in ticker_data.iterrows():
                    trade_date = idx.date() if isinstance(idx, datetime) else idx.to_pydatetime().date()
                    prices_data_dicts.append({
                        'symbol': ticker,
                        'trade_date': trade_date,
                        'market': 'US',
                        'open_price': float(row['Open']),
                        'high_price': float(row['High']),
                        'low_price': float(row['Low']),
                        'close_price': float(row['Close']),
                        'volume': int(row['Volume']),
                    })
            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")

    # Validate with Pydantic
    validated_data = []
    for item in prices_data_dicts:
        try:
            validated_item = DailyStockPrice(**item)
            validated_data.append(validated_item.model_dump())
        except Exception as e:
            logger.error(f"Validation error for {item['symbol']} on {item['trade_date']}: {e}")
            
    if validated_data:
        logger.info(f"Inserting/Updating {len(validated_data)} records into DB.")
        upsert_historical_prices(session, validated_data)
    else:
        logger.info("No new completed records to insert.")

if __name__ == "__main__":
    fetch_us_stocks()
