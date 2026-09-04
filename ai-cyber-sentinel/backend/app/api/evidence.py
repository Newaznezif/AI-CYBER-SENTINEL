from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.evidence import EvidenceResponse
from app.services.evidence import evidence_service

router = APIRouter(prefix="/evidence", tags=["Evidence"])

@router.post("/upload", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
async def upload_evidence(
    investigation_id: int = Form(...),
    source: str = Form("UPLOAD"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        evidence = await evidence_service.process_upload(
            db=db, 
            file=file, 
            investigation_id=investigation_id, 
            source=source
        )
        return evidence
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", response_model=EvidenceResponse)
def get_evidence(id: int, db: Session = Depends(get_db)):
    evidence = evidence_service.get(db, id=id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence
