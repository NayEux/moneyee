from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from ..core.database import get_db
from ..services import auth as auth_service, portfolio as portfolio_service
from ..models import models
from ..schemas import portfolio as schemas
from ..mock.broker import MockBrokerConnector

router = APIRouter(prefix="/api", tags=["portfolio"])


@router.post("/brokers/connect")
def connect_broker(broker_name: str = "MockBroker", db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    broker = portfolio_service.sync_mock_broker(db, current_user.id, broker_name)
    return {"id": broker.id, "broker_name": broker.broker_name}


@router.get("/brokers/connections")
def list_connections(db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    return db.query(models.BrokerConnection).filter_by(user_id=current_user.id).all()


@router.get("/portfolio/positions", response_model=list[schemas.PositionOut])
def get_positions(db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    positions = portfolio_service.compute_positions(db, current_user.id)
    total = sum(p["market_value"] for p in positions) or 1
    return [
        schemas.PositionOut(
            symbol=p["security"].symbol,
            market=p["security"].market,
            name=p["security"].name,
            quantity=p["quantity"],
            avg_cost=p["avg_cost"],
            last_price=p["last_price"],
            market_value=p["market_value"],
            unrealized_pnl=p["unrealized_pnl"],
            weight=p["market_value"] / total,
        ) for p in positions
    ]


@router.get("/portfolio/transactions", response_model=list[schemas.TransactionOut])
def get_transactions(db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    txs = db.query(models.Transaction).filter_by(user_id=current_user.id).all()
    result = []
    for tx in txs:
        sec = db.get(models.Security, tx.security_id)
        result.append(schemas.TransactionOut(
            symbol=sec.symbol,
            trade_date=tx.trade_date,
            side=tx.side,
            quantity=tx.quantity,
            price=tx.price,
            fees=tx.fees,
        ))
    return result


@router.get("/portfolio/summary", response_model=schemas.PortfolioSummary)
def get_summary(db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    positions = portfolio_service.compute_positions(db, current_user.id)
    equity = sum(p["market_value"] for p in positions)
    pnl = sum(p["unrealized_pnl"] for p in positions)
    return schemas.PortfolioSummary(equity=equity, pnl=pnl, today_change=pnl * 0.01, ytd_return=0.12)


@router.get("/portfolio/equity_curve", response_model=list[schemas.EquityPoint])
def equity_curve(from_date: date | None = None, to_date: date | None = None, db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    from_date = from_date or date.today() - timedelta(days=30)
    to_date = to_date or date.today()
    points = []
    equity = 100000
    cur = from_date
    while cur <= to_date:
        equity *= 1 + 0.001
        points.append(schemas.EquityPoint(date=cur, equity=equity))
        cur += timedelta(days=1)
    return points


@router.get("/portfolio/holdings_breakdown", response_model=list[schemas.HoldingsBreakdown])
def holdings_breakdown(db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    positions = portfolio_service.compute_positions(db, current_user.id)
    total = sum(p["market_value"] for p in positions) or 1
    sectors = {}
    for p in positions:
        sector = p["security"].sector or "Unknown"
        sectors[sector] = sectors.get(sector, 0) + p["market_value"] / total
    return [schemas.HoldingsBreakdown(label=k, weight=v) for k, v in sectors.items()]
