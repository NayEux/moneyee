from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import models
from ..schemas import security as security_schemas
from ..schemas import ai as ai_schemas
from ..services import auth as auth_service

router = APIRouter(prefix="/api", tags=["ai"])


@router.get("/ai_context/security/{symbol}", response_model=security_schemas.SecurityContext)
def get_ai_context(symbol: str, market: str, price_days: int = 30, fundamentals_periods: int = 3, news_limit: int = 5, research_limit: int = 3, db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    sec = db.query(models.Security).filter_by(symbol=symbol, market=market).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Security not found")
    price_history = db.query(models.PriceHistory).filter_by(security_id=sec.id).order_by(models.PriceHistory.date.desc()).limit(price_days).all()[::-1]
    fundamentals = db.query(models.FundamentalsSnapshot).filter_by(security_id=sec.id).order_by(models.FundamentalsSnapshot.period_end_date.desc()).limit(fundamentals_periods).all()
    news = db.query(models.NewsArticle).filter_by(security_id=sec.id).order_by(models.NewsArticle.published_at.desc()).limit(news_limit).all()
    research = db.query(models.ResearchNote).filter_by(security_id=sec.id).order_by(models.ResearchNote.published_at.desc()).limit(research_limit).all()
    latest_quote = {"price": price_history[-1].close if price_history else None, "change_pct": 0}
    latest_analysis = db.query(models.AIAnalysis).filter_by(user_id=current_user.id, security_id=sec.id).order_by(models.AIAnalysis.created_at.desc()).first()

    position = None
    pos_row = db.query(models.PortfolioPosition).filter_by(user_id=current_user.id, security_id=sec.id).order_by(models.PortfolioPosition.date.desc()).first()
    if pos_row:
        position = {
            "quantity": pos_row.quantity,
            "avg_cost": pos_row.avg_cost,
            "market_value": pos_row.market_value,
            "unrealized_pnl": pos_row.unrealized_pnl,
        }

    return security_schemas.SecurityContext(
        security=sec,
        latest_quote={"price": latest_quote["price"], "change_pct": latest_quote["change_pct"]},
        price_history=price_history,
        fundamentals=fundamentals,
        news=news,
        research_notes=research,
        position=position,
        analysis=latest_analysis.result_json if latest_analysis else None
    )


@router.post("/ai_analysis", response_model=ai_schemas.AIAnalysisOut)
def create_analysis(payload: ai_schemas.AIAnalysisCreate, db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    analysis = models.AIAnalysis(
        user_id=current_user.id,
        security_id=payload.security_id,
        analysis_type=payload.analysis_type,
        result_json=payload.result_json,
        input_snapshot_version=payload.input_snapshot_version,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.get("/ai_analysis/security/{symbol}", response_model=ai_schemas.AIAnalysisOut | None)
def get_latest_analysis(symbol: str, market: str, db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    sec = db.query(models.Security).filter_by(symbol=symbol, market=market).first()
    if not sec:
        raise HTTPException(status_code=404, detail="Security not found")
    analysis = db.query(models.AIAnalysis).filter_by(user_id=current_user.id, security_id=sec.id).order_by(models.AIAnalysis.created_at.desc()).first()
    return analysis
