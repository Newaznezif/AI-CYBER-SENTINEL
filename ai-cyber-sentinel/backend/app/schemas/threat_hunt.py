from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ThreatHuntQuery(BaseModel):
    query_string: str
    indicator_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class HuntResultItem(BaseModel):
    id: int
    type: str # 'indicator', 'alert', 'network_event', 'observation'
    match_field: str
    match_value: str
    timestamp: Optional[datetime] = None
    investigation_id: int

class ThreatHuntResponse(BaseModel):
    query_string: str
    results: List[HuntResultItem]
    total_matches: int
