import os
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services.evidence import evidence_service
from analyzers.pcap import parser
from analyzers.zeek import parser as zeek_parser
from analyzers.suricata import parser as suricata_parser
from app.models.domain import NetworkEvent, Observation, DetectionAlert

router = APIRouter(prefix="/pcap", tags=["PCAP Analyzer"])

def process_pcap_background(filepath: str, investigation_id: int, evidence_id: int, db: Session):
    try:
        results = parser.analyze_pcap_file(filepath, investigation_id)
        
        zeek_available, zeek_events = zeek_parser.process_pcap(filepath, investigation_id)
        
        # Safe Suricata processing
        suricata_available, suricata_alerts, suricata_events = suricata_parser.process_pcap(filepath, investigation_id)
        
        db.add(Observation(
            investigation_id=investigation_id,
            evidence_id=evidence_id,
            observation_type="ANALYZER_STATUS",
            source="SYSTEM",
            data={
                "analyzer": "Zeek", "available": zeek_available, "events_extracted": len(zeek_events),
                "suricata": "Suricata", "suricata_available": suricata_available, "alerts": len(suricata_alerts)
            },
            confidence=1.0
        ))
        
        # Save overarching observation from Scapy natively
        obs = Observation(
            investigation_id=investigation_id,
            evidence_id=evidence_id,
            observation_type="PCAP_SUMMARY",
            source="SCAPY",
            data=results["summary"],
            confidence=1.0
        )
        db.add(obs)
        
        # We only save up to 1000 events to not overload without bulk logic
        for event_data in results["events"][:1000]:
            event_obj = NetworkEvent(**event_data)
            db.add(event_obj)
            
        # Combine zeek events securely preserving normalization bindings
        for z_event in zeek_events[:1000]:
            db.add(NetworkEvent(**z_event))
            
        for s_event in suricata_events[:1000]:
            db.add(NetworkEvent(**s_event))
            
        for alert_data in suricata_alerts:
            db.add(DetectionAlert(**alert_data))
            
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Failed to process PCAP {filepath}: {e}")
    finally:
        db.close()

@router.post("/analyze/{evidence_id}", status_code=status.HTTP_202_ACCEPTED)
def analyze_pcap(
    evidence_id: int, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db) 
):
    evidence = evidence_service.get(db, id=evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
        
    if evidence.type != "PCAP":
        raise HTTPException(status_code=400, detail="Evidence is not a valid PCAP")
        
    storage_path = evidence.metadata_json.get("storage_path")
    if not storage_path or not os.path.exists(storage_path):
        raise HTTPException(status_code=404, detail="Underlying PCAP file not found locally")
        
    # Kick off processing avoiding API block
    background_tasks.add_task(process_pcap_background, storage_path, evidence.investigation_id, evidence.id, Session(bind=db.get_bind()))
    return {"message": "PCAP analysis queued successfully"}
