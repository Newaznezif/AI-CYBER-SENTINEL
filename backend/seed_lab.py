import sys
import os
import random
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.domain import (
    Investigation, Indicator, Evidence, Observation, NetworkEvent, 
    DetectionAlert, RiskAssessment, TimelineEvent
)

def create_mock_lab_data(db: Session):
    print("Initializing Phase 25 Mock Lab...")

    # Clear existing db for demo purposes, or just append
    print("Generating demo investigation...")
    now = datetime.utcnow()
    
    # 1. Create Investigation
    inv = Investigation(
        investigation_number="LAB-DEMO-001",
        title="Automated Ransomware Exfiltration (Simulated)",
        description="Demo attack simulating ingress via RDP brute force followed by internal reconnaissance and lateral movement.",
        status="ACTIVE",
        severity="CRITICAL",
        confidence=95.0,
        created_at=now - timedelta(hours=5)
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)

    inv_id = inv.id

    # 2. Add Indicators
    indicators = [
        {"type": "ipv4", "value": "193.168.10.55", "source": "Firewall RDP Logs", "confidence": 100},
        {"type": "ipv4", "value": "185.20.10.2", "source": "Zeek conn.log", "confidence": 85},
        {"type": "domain", "value": "evil-c2-xyz.com", "source": "Suricata DNS Logs", "confidence": 90},
        {"type": "hash_sha256", "value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "source": "Endpoint EDR", "confidence": 100},
    ]

    for ind in indicators:
        db.add(Indicator(
            investigation_id=inv_id,
            type=ind["type"],
            value=ind["value"],
            normalized_value=ind["value"].lower(),
            source=ind["source"],
            confidence=ind["confidence"],
            first_seen=now - timedelta(hours=4),
            created_at=now
        ))

    # 3. Add Network Events (telemetry)
    # RDP Brute force
    for i in range(15):
        db.add(NetworkEvent(
            investigation_id=inv_id,
            source_ip="193.168.10.55",
            destination_ip="10.0.0.50",
            source_port=random.randint(10000, 60000),
            destination_port=3389,
            protocol="TCP",
            timestamp=now - timedelta(hours=4) + timedelta(seconds=i*3),
            direction="inbound",
            bytes=1500,
            packets=10
        ))

    # Beaconing
    db.add(NetworkEvent(
        investigation_id=inv_id,
        source_ip="10.0.0.50",
        destination_ip="185.20.10.2",
        source_port=55432,
        destination_port=443,
        protocol="TLS",
        timestamp=now - timedelta(hours=3),
        direction="outbound",
        dns_name="evil-c2-xyz.com"
    ))

    # 4. Add Detection Alerts
    db.add(DetectionAlert(
        investigation_id=inv_id,
        source="Suricata",
        signature="ET SCAN Potential SSH/RDP Brute Force",
        severity="HIGH",
        timestamp=now - timedelta(hours=4, minutes=5),
        source_ip="193.168.10.55",
        destination_ip="10.0.0.50"
    ))
    db.add(DetectionAlert(
        investigation_id=inv_id,
        source="Custom Detection Engine",
        signature="Suspicious C2 Domain Resolution",
        severity="CRITICAL",
        timestamp=now - timedelta(hours=3, minutes=1),
        source_ip="10.0.0.50",
        raw_alert={"dns": "evil-c2-xyz.com"}
    ))

    # 5. Timeline Events
    db.add(TimelineEvent(
        investigation_id=inv_id,
        timestamp=now - timedelta(hours=4, minutes=5),
        source="Suricata",
        event_type="Alert",
        content="External IP 193.168.10.55 rapidly attempting to authenticate via RDP to 10.0.0.50"
    ))
    db.add(TimelineEvent(
        investigation_id=inv_id,
        timestamp=now - timedelta(hours=3, minutes=10),
        source="Telemetry",
        event_type="Network",
        content="Successful RDP connection established from 193.168.10.55 (Bytes: 4.2MB)"
    ))
    db.add(TimelineEvent(
        investigation_id=inv_id,
        timestamp=now - timedelta(hours=3, minutes=1),
        source="Zeek",
        event_type="DNS",
        content="Internal Host 10.0.0.50 resolved known malicious domain evil-c2-xyz.com"
    ))

    # 6. Risk Assessment
    db.add(RiskAssessment(
        investigation_id=inv_id,
        overall_score=98.5,
        severity="CRITICAL",
        confidence=0.9,
        threat_intelligence_score=90.0,
        network_evidence_score=95.0,
        detection_score=100.0,
        explanation="High severity alert correlated with known C2 domain resolution following external access."
    ))

    db.commit()
    print(f"Mock Lab successfully deployed! Target Investigation ID: {inv_id}")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_mock_lab_data(db)
    finally:
        db.close()
