import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

_db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _db

    _db = sqlite3.connect('trades.db', check_same_thread=False)
    try:
        yield
    finally:
        _db.close()


app = FastAPI(lifespan=lifespan)


def get_cursor():
    with _db as cursor:
        yield cursor


class Side(Enum):
    buy = 'buy'
    sell = 'sell'


class Trade(BaseModel):
    user: str = Field(min_length=3)
    time: datetime
    symbol: str = Field(min_length=3)
    price: int = Field(gt=0)  # In ¢
    volume: int = Field(gt=0)
    side: Side


@app.post('/trades')
def new_trade(trade: Trade, cursor=Depends(get_cursor)):
    # TODO: Validate trade
    params = {
        'user': trade.user,
        'time': trade.time,
        'symbol': trade.symbol,
        'price': trade.price,
        'volume': trade.volume,
        'side': trade.side.value,
    }

    cursor.execute(insert_sql, params)
    return {'error': None}


insert_sql = """
INSERT INTO trades 
    (user, time, symbol, price, volume, side) 
VALUES 
    (:user, :time, :symbol, :price, :volume, :side) 
"""
