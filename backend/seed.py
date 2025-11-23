from datetime import date
from app.core.database import SessionLocal, engine
from app.core.database import Base
from app.models import models
from app.mock.data_source import MockDataSource
from app.services import data_ingestion

Base.metadata.create_all(bind=engine)

db = SessionLocal()

securities = [
    {"symbol": "600519.SS", "market": "CN", "name": "贵州茅台", "sector": "Consumer", "industry": "Beverage"},
    {"symbol": "000651.SZ", "market": "CN", "name": "格力电器", "sector": "Consumer", "industry": "Appliance"},
    {"symbol": "0700.HK", "market": "HK", "name": "腾讯控股", "sector": "Tech", "industry": "Internet"},
    {"symbol": "BABA", "market": "US", "name": "Alibaba", "sector": "Tech", "industry": "Ecommerce"},
    {"symbol": "AAPL", "market": "US", "name": "Apple", "sector": "Tech", "industry": "Hardware"},
]

source = MockDataSource()

for sec in securities:
    existing = db.query(models.Security).filter_by(symbol=sec["symbol"], market=sec["market"]).first()
    if existing:
        security = existing
    else:
        security = models.Security(**sec)
        db.add(security)
        db.commit()
        db.refresh(security)
    data_ingestion.ingest_security(db, security, source)

if not db.query(models.User).filter_by(email="demo@example.com").first():
    from app.utils.security import get_password_hash
    user = models.User(email="demo@example.com", password_hash=get_password_hash("password"))
    db.add(user)
    db.commit()
    db.refresh(user)
    pref = models.UserPreference(user_id=user.id)
    db.add(pref)
    db.commit()

print("Seed completed")
