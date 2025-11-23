from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas import security as schemas
from ..models import models
from ..services import auth as auth_service, data_ingestion
from ..mock.data_source import MockDataSource
from datetime import date

router = APIRouter(prefix="/api", tags=["securities"])

data_source = MockDataSource()


@router.get("/securities/search", response_model=list[schemas.SecurityOut])
def search_securities(query: str, db: Session = Depends(get_db)):
    return db.query(models.Security).filter(models.Security.symbol.ilike(f"%{query}%") | models.Security.name.ilike(f"%{query}%")).all()


@router.get("/securities/{symbol}", response_model=schemas.SecurityOut)
def get_security(symbol: str, market: str, db: Session = Depends(get_db)):
    sec = db.query(models.Security).filter_by(symbol=symbol, market=market).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Security not found")
    return sec


@router.get("/securities/{symbol}/price_history", response_model=list[schemas.PriceHistoryOut])
def get_price_history(symbol: str, market: str, from_date: date | None = None, to: date | None = None, db: Session = Depends(get_db)):
    sec = db.query(models.Security).filter_by(symbol=symbol, market=market).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Security not found")
    q = db.query(models.PriceHistory).filter_by(security_id=sec.id)
    if from_date:
        q = q.filter(models.PriceHistory.date >= from_date)
    if to:
        q = q.filter(models.PriceHistory.date <= to)
    return q.order_by(models.PriceHistory.date).all()


@router.get("/securities/{symbol}/fundamentals", response_model=list[schemas.FundamentalsOut])
def get_fundamentals(symbol: str, market: str, limit: int = 3, db: Session = Depends(get_db)):
    sec = db.query(models.Security).filter_by(symbol=symbol, market=market).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Security not found")
    return db.query(models.FundamentalsSnapshot).filter_by(security_id=sec.id).order_by(models.FundamentalsSnapshot.period_end_date.desc()).limit(limit).all()


@router.get("/securities/{symbol}/news", response_model=list[schemas.NewsArticleOut])
def get_news(symbol: str, market: str, limit: int = 5, db: Session = Depends(get_db)):
    sec = db.query(models.Security).filter_by(symbol=symbol, market=market).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Security not found")
    return db.query(models.NewsArticle).filter_by(security_id=sec.id).order_by(models.NewsArticle.published_at.desc()).limit(limit).all()


@router.get("/securities/{symbol}/research", response_model=list[schemas.ResearchNoteOut])
def get_research(symbol: str, market: str, limit: int = 3, db: Session = Depends(get_db)):
    sec = db.query(models.Security).filter_by(symbol=symbol, market=market).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Security not found")
    return db.query(models.ResearchNote).filter_by(security_id=sec.id).order_by(models.ResearchNote.published_at.desc()).limit(limit).all()


@router.post("/securities/{symbol}/refresh")
def refresh_security(symbol: str, market: str, db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    sec = db.query(models.Security).filter_by(symbol=symbol, market=market).first()
    if not sec:
        sec = models.Security(symbol=symbol, market=market, name=f"{symbol} Corp", sector="Tech", industry="Software")
        db.add(sec)
        db.commit()
        db.refresh(sec)
    data_ingestion.ingest_security(db, sec, data_source)
    return {"status": "refreshed"}
