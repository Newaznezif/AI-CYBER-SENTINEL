from typing import List
from sqlalchemy.orm import Session
from app.models.domain import NetworkEvent
from app.repositories.base import BaseRepository
from app.schemas.network_event import NetworkEventCreate, NetworkEventUpdate

class NetworkEventRepository(BaseRepository[NetworkEvent, NetworkEventCreate, NetworkEventUpdate]):
    def __init__(self):
        super().__init__(NetworkEvent)

    def get_by_investigation(self, db: Session, investigation_id: int) -> List[NetworkEvent]:
        return db.query(self.model).filter(self.model.investigation_id == investigation_id).all()

network_event_repo = NetworkEventRepository()
