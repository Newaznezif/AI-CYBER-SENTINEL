from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TimelineEventBase(BaseModel):
    investigation_id: int
    timestamp: datetime
    source: str
    event_type: str
    content: str
    related_id: Optional[str] = None

class TimelineEventCreate(TimelineEventBase):
    pass

class TimelineEventResponse(TimelineEventBase):
    id: int

    class Config:
        from_attributes = True

class TimelineGenerationRequest(BaseModel):
    investigation_id: int
