from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ReportSection(BaseModel):
    title: str
    content: str

class InvestigationReport(BaseModel):
    investigation_id: int
    generated_at: datetime
    title: str
    summary: str
    status: str
    severity: str
    risk_score: float
    sections: List[ReportSection]
    metadata: Dict[str, Any]
