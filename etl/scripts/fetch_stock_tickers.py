"""
Fetch complete lists of US and TW stocks to populate the metadata table.
"""
import urllib.request
import json
import logging
from db_utils import get_session, upsert_stock_list

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_us_tickers():
    url = "https://www.sec.gov/files/company_tickers.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        
        tickers = []
        # format: {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}, ...}
        for key, val in data.items():
            tickers.append({
                'symbol': val['ticker'],
                'name': val['title'],
                'market': 'US',
                'is_active': True
            })
        return tickers
    except Exception as e:
        logger.error(f"Error fetching US tickers: {e}")
        return []

def fetch_tw_tickers():
    url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        
        tickers = []
        # format: [{"Code":"0050", "Name":"元大台灣50", ...}, ...]
        for item in data:
            tickers.append({
                'symbol': item['Code'],
                'name': item['Name'],
                'market': 'TW',
                'is_active': True
            })
        return tickers
    except Exception as e:
        logger.error(f"Error fetching TW tickers: {e}")
        return []

def main():
    session = get_session()
    
    us_tickers = fetch_us_tickers()
    if us_tickers:
        logger.info(f"Fetched {len(us_tickers)} US tickers")
        upsert_stock_list(session, us_tickers)
        
    tw_tickers = fetch_tw_tickers()
    if tw_tickers:
        logger.info(f"Fetched {len(tw_tickers)} TW tickers")
        upsert_stock_list(session, tw_tickers)

if __name__ == "__main__":
    main()
