"""
Database Utilities (`db_utils.py`)

- Sets up the SQLAlchemy Engine.
- Implements `upsert_historical_prices`, securely inserting data using MariaDB's 
  `ON DUPLICATE KEY UPDATE` to avoid duplicate primary key errors if pipelines re-run.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert

def get_engine():
    # Use fallback for local testing without docker if needed
    db_user = os.getenv('DB_USER', 'airflow')
    db_password = os.getenv('DB_PASSWORD', 'airflow')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'stocks')
    
    # pymysql is the driver
    connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_string)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def upsert_historical_prices(session, prices_data):
    """
    Perform an UPSERT on the historical_prices table.
    expected format for prices_data: list of dicts.
    """
    if not prices_data:
        return

    from sqlalchemy import Table, MetaData
    metadata = MetaData()
    historical_prices = Table('historical_prices', metadata, autoload_with=session.bind)

    stmt = insert(historical_prices).values(prices_data)
    
    # ON DUPLICATE KEY UPDATE logic for MariaDB/MySQL
    update_dict = {
        'open_price': stmt.inserted.open_price,
        'high_price': stmt.inserted.high_price,
        'low_price': stmt.inserted.low_price,
        'close_price': stmt.inserted.close_price,
        'volume': stmt.inserted.volume,
    }
    
    on_duplicate_stmt = stmt.on_duplicate_key_update(update_dict)
    
    session.execute(on_duplicate_stmt)
    session.commit()

def upsert_stock_list(session, stock_data):
    """
    Perform an UPSERT on the stock_list table.
    expected format: list of dicts with symbol, name, market, is_active.
    """
    if not stock_data:
        return

    from sqlalchemy import Table, MetaData
    metadata = MetaData()
    stock_list = Table('stock_list', metadata, autoload_with=session.bind)

    stmt = insert(stock_list).values(stock_data)

    update_dict = {
        'name': stmt.inserted.name,
        'is_active': stmt.inserted.is_active,
    }

    on_duplicate_stmt = stmt.on_duplicate_key_update(update_dict)

    session.execute(on_duplicate_stmt)
    session.commit()
