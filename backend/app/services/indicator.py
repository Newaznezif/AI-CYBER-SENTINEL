from sqlalchemy.orm import Session
from app.models.domain import Indicator
from app.schemas.indicator import IndicatorCreate, IndicatorUpdate
from app.services.base import BaseService
from app.repositories.indicator import indicator_repo

class IndicatorService(BaseService[Indicator, IndicatorCreate, IndicatorUpdate]):
    def create_indicator(self, db: Session, obj_in: IndicatorCreate) -> Indicator:
        return self.repository.create(db, obj_in=obj_in)

indicator_service = IndicatorService(indicator_repo)
