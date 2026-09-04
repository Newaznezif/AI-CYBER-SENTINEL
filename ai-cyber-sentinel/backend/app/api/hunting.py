from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.threat_hunt import ThreatHuntQuery, ThreatHuntResponse
from app.services.threat_hunting import threat_hunting_service

router = APIRouter(prefix="/hunting", tags=["Threat Hunting"])

@router.post("/search", response_model=ThreatHuntResponse)
def hunt(
    *,
    db: Session = Depends(get_db),
    query: ThreatHuntQuery,
):
    """
    Search across indicators, alerts, and network events for matches.
    """
    return threat_hunting_service.hunt(db=db, query=query)
