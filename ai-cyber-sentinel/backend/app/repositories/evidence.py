from sqlalchemy.orm import Session
from app.models.domain import Evidence
from app.schemas.evidence import EvidenceCreate, EvidenceUpdate
from app.repositories.base import BaseRepository

class EvidenceRepository(BaseRepository[Evidence, EvidenceCreate, EvidenceUpdate]):
    def create(self, db: Session, *, obj_in: EvidenceCreate) -> Evidence:
        db_obj = Evidence(
            investigation_id=obj_in.investigation_id,
            type=obj_in.type,
            filename=obj_in.filename,
            sha256=obj_in.sha256,
            size=obj_in.size,
            source=obj_in.source,
            metadata_json=obj_in.metadata_json
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

evidence_repo = EvidenceRepository(Evidence)
