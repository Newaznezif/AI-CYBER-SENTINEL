from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class ObservationBase(BaseModel):
    investigation_id: int
    observation_type: str
    source: str
    evidence_id: Optional[int] = None
    indicator_id: Optional[int] = None
    timestamp: Optional[datetime] = None
    confidence: float = 0.0
    data: Optional[Dict[str, Any]] = {}

class ObservationCreate(ObservationBase):
    pass

class ObservationUpdate(BaseModel):
    pass

class ObservationResponse(ObservationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
