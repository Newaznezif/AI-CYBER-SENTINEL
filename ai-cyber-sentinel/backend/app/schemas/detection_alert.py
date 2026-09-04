from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class DetectionAlertBase(BaseModel):
    investigation_id: int
    source: str
    signature: str
    severity: str
    timestamp: Optional[datetime] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    protocol: Optional[str] = None
    raw_alert: Optional[Dict[str, Any]] = {}

class DetectionAlertCreate(DetectionAlertBase):
    pass

class DetectionAlertUpdate(BaseModel):
    pass

class DetectionAlertResponse(DetectionAlertBase):
    id: int

    class Config:
        from_attributes = True
