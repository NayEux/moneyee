from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..models import models
from ..mock.data_source import MockDataSource


def ingest_security(db: Session, security: models.Security, data_source: MockDataSource):
    today = date.today()
    history = data_source.fetch_price_history(security.symbol, security.market, today - timedelta(days=30), today)
    for h in history:
        db.add(models.PriceHistory(security_id=security.id, **h))

    for f in data_source.fetch_fundamentals(security.symbol, security.market):
        db.add(models.FundamentalsSnapshot(security_id=security.id, **f))

    for n in data_source.fetch_news(security.symbol, security.market):
        db.add(models.NewsArticle(security_id=security.id, **n))

    for r in data_source.fetch_research_notes(security.symbol, security.market):
        db.add(models.ResearchNote(security_id=security.id, **r))

    db.commit()


def refresh_quotes(db: Session, security: models.Security, data_source: MockDataSource):
    quote = data_source.fetch_quote(security.symbol, security.market)
    return quote
