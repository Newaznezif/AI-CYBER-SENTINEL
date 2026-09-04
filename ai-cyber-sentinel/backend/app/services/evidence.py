import os
import hashlib
from typing import Dict, Any
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.domain import Evidence
from app.schemas.evidence import EvidenceCreate, EvidenceUpdate
from app.services.base import BaseService
from app.repositories.evidence import evidence_repo
from app.config import settings

UPLOAD_DIR = os.path.join(os.getcwd(), "storage", "evidence")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class EvidenceService(BaseService[Evidence, EvidenceCreate, EvidenceUpdate]):
    async def process_upload(self, db: Session, file: UploadFile, investigation_id: int, source: str) -> Evidence:
        content = await file.read()
        size = len(content)
        
        if size > settings.MAX_UPLOAD_SIZE:
            raise ValueError(f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes")
            
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Save absolute safe path out of execution stream
        safe_filename = f"{file_hash}_{file.filename}"
        storage_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        with open(storage_path, "wb") as f:
            f.write(content)
            
        evidence_create = EvidenceCreate(
            investigation_id=investigation_id,
            type="PCAP" if file.filename.endswith(".pcap") else "FILE",
            filename=safe_filename,
            sha256=file_hash,
            size=size,
            source=source,
            metadata_json={"original_name": file.filename, "storage_path": storage_path}
        )
        
        return self.repository.create(db, obj_in=evidence_create)

evidence_service = EvidenceService(evidence_repo)
