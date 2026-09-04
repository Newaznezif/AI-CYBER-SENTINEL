from typing import List
from sqlalchemy.orm import Session
from app.models.domain import AttackTechnique
from app.repositories.base import BaseRepository
from app.schemas.attack_technique import AttackTechniqueCreate, AttackTechniqueUpdate

class AttackTechniqueRepository(BaseRepository[AttackTechnique, AttackTechniqueCreate, AttackTechniqueUpdate]):
    def __init__(self):
        super().__init__(AttackTechnique)

    def get_by_investigation(self, db: Session, investigation_id: int) -> List[AttackTechnique]:
        return db.query(self.model).filter(self.model.investigation_id == investigation_id).all()

attack_technique_repo = AttackTechniqueRepository()
