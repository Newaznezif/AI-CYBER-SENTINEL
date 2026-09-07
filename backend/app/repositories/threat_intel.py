from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.domain import ThreatIntelResult
from app.repositories.base import BaseRepository
from app.schemas.threat_intel import ThreatIntelResultCreate, ThreatIntelResultUpdate

class ThreatIntelRepository(BaseRepository[ThreatIntelResult, ThreatIntelResultCreate, ThreatIntelResultUpdate]):
    def __init__(self):
        super().__init__(ThreatIntelResult)

    def get_by_indicator(self, db: Session, indicator_id: int) -> List[ThreatIntelResult]:
        return db.query(self.model).filter(self.model.indicator_id == indicator_id).all()

    def get_by_indicator_and_provider(self, db: Session, indicator_id: int, provider: str) -> Optional[ThreatIntelResult]:
        return db.query(self.model).filter(
            self.model.indicator_id == indicator_id,
            self.model.provider == provider
        ).order_by(self.model.queried_at.desc()).first()

threat_intel_repo = ThreatIntelRepository()
