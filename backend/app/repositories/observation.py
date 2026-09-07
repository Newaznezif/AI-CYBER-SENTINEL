from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.domain import Observation
from app.repositories.base import BaseRepository
from app.schemas.observation import ObservationCreate, ObservationUpdate

class ObservationRepository(BaseRepository[Observation, ObservationCreate, ObservationUpdate]):
    def __init__(self):
        super().__init__(Observation)

    def get_by_investigation(self, db: Session, investigation_id: int) -> List[Observation]:
        return db.query(self.model).filter(self.model.investigation_id == investigation_id).all()

observation_repo = ObservationRepository()
