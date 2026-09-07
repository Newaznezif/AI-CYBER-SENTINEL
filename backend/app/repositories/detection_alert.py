from typing import List
from sqlalchemy.orm import Session
from app.models.domain import DetectionAlert
from app.repositories.base import BaseRepository
from app.schemas.detection_alert import DetectionAlertCreate, DetectionAlertUpdate

class DetectionAlertRepository(BaseRepository[DetectionAlert, DetectionAlertCreate, DetectionAlertUpdate]):
    def __init__(self):
        super().__init__(DetectionAlert)

    def get_by_investigation(self, db: Session, investigation_id: int) -> List[DetectionAlert]:
        return db.query(self.model).filter(self.model.investigation_id == investigation_id).all()

detection_alert_repo = DetectionAlertRepository()
