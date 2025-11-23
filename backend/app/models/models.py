from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Float, Date, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum


class RiskLevel(str, enum.Enum):
    conservative = "conservative"
    balanced = "balanced"
    aggressive = "aggressive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    preferences = relationship("UserPreference", back_populates="user", uselist=False)


class Security(Base):
    __tablename__ = "securities"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True, nullable=False)
    market = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    sector = Column(String)
    industry = Column(String)

    price_history = relationship("PriceHistory", back_populates="security")
    fundamentals = relationship("FundamentalsSnapshot", back_populates="security")
    news = relationship("NewsArticle", back_populates="security")
    research_notes = relationship("ResearchNote", back_populates="security")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=False)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)

    security = relationship("Security", back_populates="price_history")


class FundamentalsSnapshot(Base):
    __tablename__ = "fundamentals_snapshot"

    id = Column(Integer, primary_key=True)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=False)
    period_end_date = Column(Date, index=True)
    revenue = Column(Float)
    net_income = Column(Float)
    eps = Column(Float)
    roe = Column(Float)
    gross_margin = Column(Float)
    operating_margin = Column(Float)
    pe_ttm = Column(Float)
    pb = Column(Float)
    dividend_yield = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    security = relationship("Security", back_populates="fundamentals")


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=True)
    title = Column(String)
    source = Column(String)
    url = Column(String)
    published_at = Column(DateTime)
    summary = Column(String)
    raw_text = Column(String)

    security = relationship("Security", back_populates="news")


class ResearchNote(Base):
    __tablename__ = "research_notes"

    id = Column(Integer, primary_key=True)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=True)
    broker_name = Column(String)
    title = Column(String)
    url = Column(String)
    published_at = Column(DateTime)
    rating = Column(String)
    target_price = Column(Float)
    summary = Column(String)

    security = relationship("Security", back_populates="research_notes")


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=True)
    analysis_type = Column(String, nullable=False)
    input_snapshot_version = Column(JSON)
    result_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class BrokerConnection(Base):
    __tablename__ = "broker_connections"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    broker_name = Column(String, nullable=False)
    config_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=False)
    broker_connection_id = Column(Integer, ForeignKey("broker_connections.id"))
    trade_date = Column(Date, index=True)
    side = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    fees = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PortfolioPosition(Base):
    __tablename__ = "portfolio_positions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=False)
    date = Column(Date, index=True)
    quantity = Column(Float)
    avg_cost = Column(Float)
    market_value = Column(Float)
    unrealized_pnl = Column(Float)
    realized_pnl_to_date = Column(Float)


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.balanced)
    preferred_holding_period_days = Column(Integer, default=365)
    preferred_sectors = Column(JSON, default=list)
    avoided_sectors = Column(JSON, default=list)
    dca_settings = Column(JSON)
    alert_settings = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="preferences")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String)
    message = Column(String)
    related_security_id = Column(Integer, ForeignKey("securities.id"), nullable=True)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime)
