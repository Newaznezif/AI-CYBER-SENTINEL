from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.indicator import IndicatorCreate, IndicatorUpdate, IndicatorResponse
from app.services.indicator import indicator_service

router = APIRouter(prefix="/indicators", tags=["Indicators"])

@router.post("", response_model=IndicatorResponse, status_code=status.HTTP_201_CREATED)
def create_indicator(
    *,
    db: Session = Depends(get_db),
    indicator_in: IndicatorCreate,
):
    try:
        return indicator_service.create_indicator(db, obj_in=indicator_in)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("", response_model=List[IndicatorResponse])
def read_indicators(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return indicator_service.get_multi(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=IndicatorResponse)
def read_indicator(
    *,
    db: Session = Depends(get_db),
    id: int,
):
    indicator = indicator_service.get(db, id=id)
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return indicator
