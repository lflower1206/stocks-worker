"""
Models (`models.py`)

Uses Pydantic (`DailyStockPrice` model) to strictly validate row data 
(types, constraints like max_length for symbol) before insertion.
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Literal

class DailyStockPrice(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    symbol: str = Field(..., max_length=20)
    trade_date: date
    market: Literal['US', 'TW']
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
