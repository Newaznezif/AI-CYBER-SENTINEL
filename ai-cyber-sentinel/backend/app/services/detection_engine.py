from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.domain import DetectionAlert, NetworkEvent, Observation
from app.schemas.detection_alert import DetectionAlertCreate
from app.services.base import ServiceBase

class DetectionEngineService(ServiceBase[DetectionAlert, DetectionAlertCreate, DetectionAlertCreate]):
    
    def run_detection(self, db: Session, investigation_id: int) -> List[DetectionAlert]:
        alerts = []
        network_events = db.query(NetworkEvent).filter(NetworkEvent.investigation_id == investigation_id).all()
        observations = db.query(Observation).filter(Observation.investigation_id == investigation_id).all()
        
        # Rule 1: Possible SSH Brute Force
        ssh_events = [e for e in network_events if e.destination_port == 22]
        if len(ssh_events) > 10: # threshold
            alert = DetectionAlertCreate(
                investigation_id=investigation_id,
                source="Custom Detection Engine",
                signature="Possible SSH Brute Force",
                severity="HIGH",
                timestamp=datetime.utcnow(),
                protocol="SSH",
                raw_alert={"event_count": len(ssh_events), "description": "High volume of SSH traffic detected."}
            )
            alerts.append(alert)

        # Rule 2: Suspicious HTTP User Agent
        suspicious_uas = ["curl", "wget", "nmap", "sqlmap", "nikto"]
        for event in network_events:
            if event.user_agent and any(sua in event.user_agent.lower() for sua in suspicious_uas):
                alert = DetectionAlertCreate(
                    investigation_id=investigation_id,
                    source="Custom Detection Engine",
                    signature="Suspicious User-Agent Detected",
                    severity="MEDIUM",
                    timestamp=event.timestamp or datetime.utcnow(),
                    source_ip=event.source_ip,
                    destination_ip=event.destination_ip,
                    protocol=event.protocol,
                    raw_alert={"user_agent": event.user_agent}
                )
                alerts.append(alert)

        # Rule 3: Direct IP access on HTTP (No DNS)
        # Normally HTTP requests without host or where Host is an IP
        for event in network_events:
            if event.destination_port in [80, 443, 8080] and not event.dns_name:
                # Basic check, just an example rule
                if event.http_host and event.http_host.replace('.', '').isnumeric():
                    alert = DetectionAlertCreate(
                        investigation_id=investigation_id,
                        source="Custom Detection Engine",
                        signature="Direct IP web access",
                        severity="LOW",
                        timestamp=event.timestamp or datetime.utcnow(),
                        source_ip=event.source_ip,
                        destination_ip=event.destination_ip,
                        protocol=event.protocol,
                        raw_alert={"http_host": event.http_host}
                    )
                    alerts.append(alert)

        # Save all generated alerts
        saved_alerts = []
        for alert_data in alerts:
            # Check if this alert already exists (simple deduplication based on signature and timestamp/source_ip)
            existing = db.query(DetectionAlert).filter(
                DetectionAlert.investigation_id == alert_data.investigation_id,
                DetectionAlert.signature == alert_data.signature,
                DetectionAlert.source_ip == alert_data.source_ip
            ).first()
            
            if not existing:
                db_obj = DetectionAlert(**alert_data.model_dump())
                db.add(db_obj)
                saved_alerts.append(db_obj)
        
        db.commit()
        return saved_alerts

    def get_alerts(self, db: Session, investigation_id: int) -> List[DetectionAlert]:
        return db.query(DetectionAlert).filter(DetectionAlert.investigation_id == investigation_id).all()

detection_engine = DetectionEngineService(DetectionAlert)
