import uuid
from sqlalchemy.orm import Session
from app.models.domain import Investigation
from app.schemas.investigation import InvestigationCreate, InvestigationUpdate
from app.repositories.base import BaseRepository

class InvestigationRepository(BaseRepository[Investigation, InvestigationCreate, InvestigationUpdate]):
    def create(self, db: Session, *, obj_in: InvestigationCreate) -> Investigation:
        inv_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        db_obj = Investigation(
            title=obj_in.title,
            description=obj_in.description,
            severity=obj_in.severity,
            confidence=obj_in.confidence,
            investigation_number=inv_number
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

investigation_repo = InvestigationRepository(Investigation)
