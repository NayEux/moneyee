from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class PositionOut(BaseModel):
    symbol: str
    market: str
    name: str
    quantity: float
    avg_cost: float
    last_price: float
    market_value: float
    unrealized_pnl: float
    weight: float


class TransactionOut(BaseModel):
    symbol: str
    trade_date: date
    side: str
    quantity: float
    price: float
    fees: float


class EquityPoint(BaseModel):
    date: date
    equity: float


class HoldingsBreakdown(BaseModel):
    label: str
    weight: float


class PortfolioSummary(BaseModel):
    equity: float
    pnl: float
    today_change: float
    ytd_return: float
