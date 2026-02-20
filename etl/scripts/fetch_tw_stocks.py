import sys
import logging
import yfinance as yf
from datetime import datetime, date
from db_utils import get_session, upsert_historical_prices
from models import DailyStockPrice
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_active_tw_symbols(session):
    result = session.execute(
        text("SELECT symbol FROM tracked_symbols WHERE market = 'TW' AND is_active = TRUE")
    )
    return [row[0] for row in result.fetchall()]

def fetch_tw_stocks():
    session = get_session()
    symbols = get_active_tw_symbols(session)
    
    if not symbols:
        logger.info("No active TW symbols found.")
        return

    # yfinance requires .TW or .TWO suffix for Taiwan stocks. 
    # We assume the symbol in DB might just be the number (e.g., "2330"), 
    # so we'll append .TW by default for this example. 
    # In a full app, you might distinguish between list (TWSE) and OTC (TPEx).
    yf_symbols = [f"{s}.TW" if not s.endswith('.TW') and not s.endswith('.TWO') else s for s in symbols]
    
    logger.info(f"Fetching data for TW symbols: {yf_symbols}")
    
    data = yf.download(yf_symbols, period="1mo", group_by="ticker", threads=True, auto_adjust=False)
    
    prices_data_dicts = []
    
    if len(yf_symbols) == 1:
        ticker = yf_symbols[0]
        # Remove the .TW suffix for DB insertion
        db_symbol = ticker.replace('.TW', '').replace('.TWO', '')
        data = data.dropna()
        for idx, row in data.iterrows():
            trade_date = idx.date() if isinstance(idx, datetime) else idx.to_pydatetime().date()
            prices_data_dicts.append({
                'symbol': db_symbol,
                'trade_date': trade_date,
                'market': 'TW',
                'open_price': float(row['Open']),
                'high_price': float(row['High']),
                'low_price': float(row['Low']),
                'close_price': float(row['Close']),
                'volume': int(row['Volume']),
            })
    else:
        for ticker in yf_symbols:
            try:
                db_symbol = ticker.replace('.TW', '').replace('.TWO', '')
                ticker_data = data[ticker].dropna()
                for idx, row in ticker_data.iterrows():
                    trade_date = idx.date() if isinstance(idx, datetime) else idx.to_pydatetime().date()
                    prices_data_dicts.append({
                        'symbol': db_symbol,
                        'trade_date': trade_date,
                        'market': 'TW',
                        'open_price': float(row['Open']),
                        'high_price': float(row['High']),
                        'low_price': float(row['Low']),
                        'close_price': float(row['Close']),
                        'volume': int(row['Volume']),
                    })
            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")

    validated_data = []
    for item in prices_data_dicts:
        try:
            validated_item = DailyStockPrice(**item)
            validated_data.append(validated_item.model_dump())
        except Exception as e:
            logger.error(f"Validation error for {item['symbol']} on {item['trade_date']}: {e}")
            
    if validated_data:
        logger.info(f"Inserting/Updating {len(validated_data)} TW records into DB.")
        upsert_historical_prices(session, validated_data)
    else:
        logger.info("No new completed records to insert.")

if __name__ == "__main__":
    fetch_tw_stocks()
