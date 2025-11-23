from datetime import date
from collections import defaultdict
from sqlalchemy.orm import Session
from ..models import models
from ..mock.broker import MockBrokerConnector


def sync_mock_broker(db: Session, user_id: int, broker_name: str = "DemoBroker"):
    connector = MockBrokerConnector(broker_name)
    broker = models.BrokerConnection(user_id=user_id, broker_name=broker_name, config_json={"token": "mock"})
    db.add(broker)
    db.commit()
    db.refresh(broker)

    for pos in connector.fetch_positions():
        security = db.query(models.Security).filter_by(symbol=pos["symbol"], market=pos["market"]).first()
        if not security:
            security = models.Security(symbol=pos["symbol"], market=pos["market"], name=pos["name"], sector="Tech", industry="Software")
            db.add(security)
            db.commit()
            db.refresh(security)
        tx = models.Transaction(
            user_id=user_id,
            security_id=security.id,
            broker_connection_id=broker.id,
            trade_date=date.today(),
            side="buy",
            quantity=pos["quantity"],
            price=pos["avg_cost"],
            fees=0
        )
        db.add(tx)
    db.commit()
    return broker


def compute_positions(db: Session, user_id: int):
    transactions = db.query(models.Transaction).filter_by(user_id=user_id).all()
    qty_map = defaultdict(float)
    cost_map = defaultdict(float)
    for tx in transactions:
        key = tx.security_id
        if tx.side == "buy":
            total_cost = qty_map[key] * cost_map[key] + tx.quantity * tx.price + tx.fees
            qty_map[key] += tx.quantity
            cost_map[key] = total_cost / qty_map[key] if qty_map[key] else 0
        else:
            qty_map[key] -= tx.quantity
    positions = []
    for security_id, qty in qty_map.items():
        security = db.get(models.Security, security_id)
        last_price = db.query(models.PriceHistory).filter_by(security_id=security_id).order_by(models.PriceHistory.date.desc()).first()
        price = last_price.close if last_price else cost_map[security_id]
        positions.append({
            "security": security,
            "quantity": qty,
            "avg_cost": cost_map[security_id],
            "last_price": price,
            "market_value": qty * price,
            "unrealized_pnl": (price - cost_map[security_id]) * qty,
        })
    return positions
