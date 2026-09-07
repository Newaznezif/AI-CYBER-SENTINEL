from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class InvestigationBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str = "INFO"
    confidence: float = 0.0

class InvestigationCreate(InvestigationBase):
    pass

class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    severity: Optional[str] = None
    confidence: Optional[float] = None

class InvestigationInDBBase(InvestigationBase):
    id: int
    investigation_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InvestigationResponse(InvestigationInDBBase):
    pass
