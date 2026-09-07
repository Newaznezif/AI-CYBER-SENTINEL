from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.domain import RiskAssessment
from app.repositories.base import BaseRepository
from app.schemas.risk_assessment import RiskAssessmentCreate, RiskAssessmentUpdate

class RiskAssessmentRepository(BaseRepository[RiskAssessment, RiskAssessmentCreate, RiskAssessmentUpdate]):
    def __init__(self):
        super().__init__(RiskAssessment)

    def get_by_investigation(self, db: Session, investigation_id: int) -> Optional[RiskAssessment]:
        return db.query(self.model).filter(self.model.investigation_id == investigation_id).order_by(self.model.created_at.desc()).first()

risk_assessment_repo = RiskAssessmentRepository()
