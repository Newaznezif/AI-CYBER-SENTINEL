from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class RiskAssessmentBase(BaseModel):
    investigation_id: int
    overall_score: float = 0.0
    severity: str = "LOW"
    confidence: float = 0.0
    threat_intelligence_score: float = 0.0
    network_evidence_score: float = 0.0
    detection_score: float = 0.0
    exploitation_score: float = 0.0
    historical_score: float = 0.0
    asset_criticality_score: float = 0.0
    explanation: Optional[str] = None

class RiskAssessmentCreate(RiskAssessmentBase):
    pass

class RiskAssessmentUpdate(BaseModel):
    overall_score: Optional[float] = None
    severity: Optional[str] = None
    explanation: Optional[str] = None

class RiskAssessmentResponse(RiskAssessmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
