from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.domain import Investigation
from app.schemas.investigation import InvestigationCreate, InvestigationUpdate
from app.services.base import BaseService
from app.repositories.investigation import investigation_repo

class InvestigationService(BaseService[Investigation, InvestigationCreate, InvestigationUpdate]):
    def create_investigation(self, db: Session, obj_in: InvestigationCreate) -> Investigation:
        return self.repository.create(db, obj_in=obj_in)
        
    def close_investigation(self, db: Session, id: int) -> Optional[Investigation]:
        from datetime import datetime
        db_obj = self.get(db, id)
        if hasattr(db_obj, 'status'):
            db_obj.status = "CLOSED"
            db_obj.closed_at = datetime.utcnow()
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

investigation_service = InvestigationService(investigation_repo)
