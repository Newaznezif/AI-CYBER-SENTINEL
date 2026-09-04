from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ThreatIntelResultBase(BaseModel):
    indicator_id: int
    provider: str
    query_type: str
    reputation: Optional[str] = None
    confidence: float = 0.0
    categories: List[str] = []
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    raw_response: Dict[str, Any] = {}
    success: bool = True
    error: Optional[str] = None

class ThreatIntelResultCreate(ThreatIntelResultBase):
    pass

class ThreatIntelResultUpdate(BaseModel):
    reputation: Optional[str] = None
    confidence: Optional[float] = None
    categories: Optional[List[str]] = None
    last_seen: Optional[datetime] = None
    raw_response: Optional[Dict[str, Any]] = None
    success: Optional[bool] = None
    error: Optional[str] = None

class ThreatIntelResultInDBBase(ThreatIntelResultBase):
    id: int
    queried_at: datetime

    class Config:
        from_attributes = True

class ThreatIntelResultResponse(ThreatIntelResultInDBBase):
    pass
