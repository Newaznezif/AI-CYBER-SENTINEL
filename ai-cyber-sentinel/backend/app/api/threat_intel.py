from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.database.session import SessionLocal
from app.schemas.threat_intel import ThreatIntelResultResponse
from app.repositories.threat_intel import threat_intel_repo
from app.repositories.indicator import indicator_repo
from app.services.cti_manager import CTIManager
from app.config import settings

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from integrations.cti.abuseipdb import AbuseIPDBProvider
from integrations.cti.otx import OTXProvider
from integrations.cti.virustotal import VirusTotalProvider

router = APIRouter()

def get_cti_manager() -> CTIManager:
    providers = []
    if settings.ABUSEIPDB_API_KEY:
        providers.append(AbuseIPDBProvider(api_key=settings.ABUSEIPDB_API_KEY))
    if settings.OTX_API_KEY:
        providers.append(OTXProvider(api_key=settings.OTX_API_KEY))
    if settings.VIRUSTOTAL_API_KEY:
        providers.append(VirusTotalProvider(api_key=settings.VIRUSTOTAL_API_KEY))
    
    return CTIManager(providers=providers)

async def _bg_enrich_indicator(manager: CTIManager, indicator):
    db: Session = SessionLocal()
    try:
        await manager.enrich_indicator(db, indicator)
    finally:
        db.close()

@router.post("/{indicator_id}/enrich", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def enrich_indicator(
    indicator_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    indicator = indicator_repo.get(db, id=indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
        
    manager = get_cti_manager()
    if not manager.providers:
        # For DEMO mode, we could use mock providers, but here we return error if missing configs
        raise HTTPException(
            status_code=400, 
            detail="No CTI providers are configured (Missing API keys)"
        )
        
    background_tasks.add_task(_bg_enrich_indicator, manager, indicator)
    
    return {"status": "Enrichment started"}

@router.get("/{indicator_id}/results", response_model=List[ThreatIntelResultResponse])
def get_enrichment_results(indicator_id: int, db: Session = Depends(get_db)):
    results = threat_intel_repo.get_by_indicator(db, indicator_id=indicator_id)
    return results
