from sqlalchemy.orm import Session
from app.models.domain import Indicator
from app.schemas.indicator import IndicatorCreate, IndicatorUpdate
from app.repositories.base import BaseRepository

class IndicatorRepository(BaseRepository[Indicator, IndicatorCreate, IndicatorUpdate]):
    def create(self, db: Session, *, obj_in: IndicatorCreate) -> Indicator:
        # Normalize the indicator before enrichment as per specifications
        normalized = obj_in.value.strip().lower()
        if obj_in.type in ["DOMAIN", "MD5", "SHA1", "SHA256", "EMAIL"]:
            normalized = normalized
        elif obj_in.type in ["URL"]:
            normalized = obj_in.value.strip() # URLs may be case sensitive
            
        db_obj = Indicator(
            investigation_id=obj_in.investigation_id,
            type=obj_in.type,
            value=obj_in.value,
            normalized_value=normalized,
            source=obj_in.source,
            confidence=obj_in.confidence
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

indicator_repo = IndicatorRepository(Indicator)
