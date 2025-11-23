from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List, Any


class SecurityBase(BaseModel):
    symbol: str
    market: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None


class SecurityOut(SecurityBase):
    id: int

    class Config:
        from_attributes = True


class PriceHistoryOut(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float

    class Config:
        from_attributes = True


class FundamentalsOut(BaseModel):
    period_end_date: date
    revenue: float | None
    net_income: float | None
    eps: float | None
    roe: float | None
    gross_margin: float | None
    operating_margin: float | None
    pe_ttm: float | None
    pb: float | None
    dividend_yield: float | None
    created_at: datetime | None

    class Config:
        from_attributes = True


class NewsArticleOut(BaseModel):
    title: str
    source: str
    url: str
    published_at: datetime
    summary: str | None = None

    class Config:
        from_attributes = True


class ResearchNoteOut(BaseModel):
    broker_name: str
    title: str
    url: str
    published_at: datetime
    rating: str | None
    target_price: float | None
    summary: str | None

    class Config:
        from_attributes = True


class SecurityContext(BaseModel):
    security: SecurityOut
    latest_quote: dict[str, Any]
    price_history: List[PriceHistoryOut]
    fundamentals: List[FundamentalsOut]
    news: List[NewsArticleOut]
    research_notes: List[ResearchNoteOut]
    position: Optional[dict[str, Any]] = None
    analysis: Optional[Any] = None
