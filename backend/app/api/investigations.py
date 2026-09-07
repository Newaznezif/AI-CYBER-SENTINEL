from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.investigation import InvestigationCreate, InvestigationUpdate, InvestigationResponse
from app.services.investigation import investigation_service
from app.services.correlation_engine import CorrelationEngine
from app.services.mitre_attack import mitre_validator_service
from app.services.ai_engine import ai_engine
from app.services.risk_engine import RiskEngine
from app.schemas.risk_assessment import RiskAssessmentResponse
from app.services.timeline_engine import timeline_engine
from app.schemas.timeline import TimelineEventResponse
from app.services.detection_engine import detection_engine
from app.schemas.detection_alert import DetectionAlertResponse
from app.services.report_engine import report_engine
from app.schemas.report import InvestigationReport

router = APIRouter(prefix="/investigations", tags=["Investigations"])

@router.post("", response_model=InvestigationResponse, status_code=status.HTTP_201_CREATED)
def create_investigation(
    *,
    db: Session = Depends(get_db),
    investigation_in: InvestigationCreate,
):
    return investigation_service.create_investigation(db, obj_in=investigation_in)

@router.get("", response_model=List[InvestigationResponse])
def read_investigations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return investigation_service.get_multi(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=InvestigationResponse)
def read_investigation(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    investigation = investigation_service.get(db, id=id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return investigation

@router.patch("/{id}", response_model=InvestigationResponse)
def update_investigation(
    *,
    db: Session = Depends(get_db),
    id: int,
    investigation_in: InvestigationUpdate,
):
    investigation = investigation_service.get(db, id=id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return investigation_service.update(db, db_obj=investigation, obj_in=investigation_in)

@router.delete("/{id}", response_model=InvestigationResponse)
def delete_investigation(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    investigation = investigation_service.get(db, id=id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return investigation_service.remove(db, id=id)

@router.post("/{id}/correlate", response_model=dict, status_code=status.HTTP_200_OK)
def run_correlation(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    investigation = investigation_service.get(db, id=id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    engine = CorrelationEngine(db=db)
    result = engine.run(investigation_id=id)
    return result

@router.post("/{id}/mitre", response_model=dict, status_code=status.HTTP_200_OK)
def run_mitre_validation(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    investigation = investigation_service.get(db, id=id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    result = mitre_validator_service.validate(db=db, investigation_id=id)
    return result

@router.post("/{id}/ai-summary", response_model=dict, status_code=status.HTTP_200_OK)
async def generate_ai_summary(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    try:
        result = await ai_engine.generate_investigation_summary(db=db, investigation_id=id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{id}/risk_assessment", response_model=RiskAssessmentResponse, status_code=status.HTTP_200_OK)
def evaluate_risk(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    try:
        engine = RiskEngine(db=db)
        result = engine.evaluate(investigation_id=id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{id}/timeline", response_model=List[TimelineEventResponse], status_code=status.HTTP_200_OK)
def generate_timeline(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    investigation = investigation_service.get(db, id=id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    result = timeline_engine.generate_timeline(db=db, investigation_id=id)
    return result

@router.get("/{id}/timeline", response_model=List[TimelineEventResponse])
def get_timeline(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    investigation = investigation_service.get(db, id=id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
        
    return timeline_engine.get_timeline(db=db, investigation_id=id)

@router.post("/{id}/detect", response_model=List[DetectionAlertResponse], status_code=status.HTTP_200_OK)
def run_detection(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    investigation = investigation_service.get(db, id=id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    result = detection_engine.run_detection(db=db, investigation_id=id)
    return result

@router.get("/{id}/alerts", response_model=List[DetectionAlertResponse])
def get_alerts(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    investigation = investigation_service.get(db, id=id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
        
    return detection_engine.get_alerts(db=db, investigation_id=id)

@router.get("/{id}/report", response_model=InvestigationReport)
def generate_report(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    try:
        return report_engine.generate_report(db=db, investigation_id=id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
