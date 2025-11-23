from pydantic import BaseModel
from typing import List, Optional, Any
from ..models.models import RiskLevel


class PreferenceUpdate(BaseModel):
    risk_level: RiskLevel
    preferred_holding_period_days: int
    preferred_sectors: List[str] | None = None
    avoided_sectors: List[str] | None = None
    dca_settings: Any | None = None
    alert_settings: Any | None = None


class PreferenceOut(PreferenceUpdate):
    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    id: int
    type: str
    message: str
    triggered_at: str
    read_at: str | None = None

    class Config:
        from_attributes = True
