from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class EvidenceBase(BaseModel):
    investigation_id: int
    type: str
    source: str
    metadata_json: Optional[Dict[str, Any]] = {}

class EvidenceCreate(EvidenceBase):
    filename: str
    sha256: str
    size: int

class EvidenceUpdate(BaseModel):
    metadata_json: Optional[Dict[str, Any]] = None

class EvidenceInDBBase(EvidenceBase):
    id: int
    filename: str
    sha256: str
    size: int
    created_at: datetime

    class Config:
        from_attributes = True

class EvidenceResponse(EvidenceInDBBase):
    pass
