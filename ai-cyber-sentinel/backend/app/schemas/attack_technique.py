from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class AttackTechniqueBase(BaseModel):
    investigation_id: int
    technique_id: str
    technique_name: str
    tactic: str
    confidence: float = 0.0
    status: str = "CANDIDATE"
    supporting_evidence: List[Dict[str, Any]] = []

class AttackTechniqueCreate(AttackTechniqueBase):
    pass

class AttackTechniqueUpdate(BaseModel):
    confidence: Optional[float] = None
    status: Optional[str] = None
    supporting_evidence: Optional[List[Dict[str, Any]]] = None

class AttackTechniqueResponse(AttackTechniqueBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
