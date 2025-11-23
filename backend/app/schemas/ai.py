from pydantic import BaseModel
from typing import Any, Optional


class AIAnalysisCreate(BaseModel):
    security_id: Optional[int] = None
    analysis_type: str
    result_json: Any
    input_snapshot_version: Any | None = None


class AIAnalysisOut(BaseModel):
    id: int
    analysis_type: str
    result_json: Any
    created_at: str

    class Config:
        from_attributes = True
