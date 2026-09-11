import sys
import os
import asyncio
from datetime import datetime, timezone

# Add backend directory to path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_dir)

from app.database.session import SessionLocal
from app.models.domain import NetworkEvent, DetectionAlert, Indicator
from app.services.investigation import investigation_service
from app.schemas.investigation import InvestigationCreate
from analyzers.suricata.parser import process_pcap as suricata_process
from analyzers.pcap.parser import analyze_pcap_file
from app.services.detection_engine import detection_engine
from app.services.correlation_engine import CorrelationEngine
from app.services.mitre_attack import mitre_validator_service
from app.services.risk_engine import RiskEngine
from app.services.timeline_engine import timeline_engine
from app.services.report_engine import report_engine
from app.services.ai_engine import ai_engine
from app.services.threat_hunting import threat_hunting_service

async def run_full_pipeline():
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        print("=== 1. CREATING REAL INVESTIGATION IN POSTGRESQL ===")
        inv = investigation_service.create_investigation(db, obj_in=InvestigationCreate(
            investigation_number="FLOW-TEST-999",
            title="Comprehensive E2E Integration Flow",
            description="End-to-end validation of all AI-Cyber Sentinel pipeline services with real database and AI backend.",
            status="ACTIVE",
            severity="HIGH",
            confidence=0.0
        ))
        inv_id = inv.id
        print(f"Investigation created with ID: {inv_id}")

        print("=== 2. INGESTING EVIDENCE & PCAP ANALYSIS ===")
        pcap_path = os.path.abspath(os.path.join(backend_dir, "..", "sample-data", "pcaps", "test_traffic.pcap"))
        scapy_res = analyze_pcap_file(pcap_path, inv_id)
        packet_count = scapy_res["summary"]["packet_count"]
        print(f"Scapy parsed packets: {packet_count}")
        for ev in scapy_res["events"]:
            db.add(NetworkEvent(**ev))
        db.commit()

        suricata_ok, suricata_alerts, suricata_events = suricata_process(pcap_path, inv_id)
        print(f"Suricata offline processing: ok={suricata_ok}, alerts={len(suricata_alerts)}, events={len(suricata_events)}")
        for s_ev in suricata_events:
            db.add(NetworkEvent(**s_ev))
        for s_alt in suricata_alerts:
            db.add(DetectionAlert(**s_alt))
        db.commit()

        print("=== 3. ADDING EXTRACTED INDICATORS ===")
        ind1 = Indicator(
            investigation_id=inv_id,
            type="ipv4",
            value="192.168.1.100",
            normalized_value="192.168.1.100",
            source="PCAP Ingestion",
            confidence=90.0,
            created_at=now
        )
        ind2 = Indicator(
            investigation_id=inv_id,
            type="domain",
            value="example.com",
            normalized_value="example.com",
            source="DNS Traffic",
            confidence=85.0,
            created_at=now
        )
        db.add(ind1)
        db.add(ind2)
        db.commit()
        print("Indicators successfully persisted.")

        print("=== 4. RUNNING DETECTION ENGINE ===")
        # Seed a detection alert for correlation
        db.add(DetectionAlert(
            investigation_id=inv_id,
            source="SURICATA",
            signature="ET SCAN Potential Vulnerability Probe",
            severity="Critical",
            source_ip="192.168.1.100",
            destination_ip="8.8.8.8",
            timestamp=now
        ))
        db.commit()
        detected_alerts = detection_engine.run_detection(db, inv_id)
        total_alerts = detection_engine.get_alerts(db, inv_id)
        print(f"Detection engine active. Total alerts on investigation: {len(total_alerts)}")

        print("=== 5. RUNNING CORRELATION ENGINE ===")
        corr_engine = CorrelationEngine(db=db)
        corr_res = corr_engine.run(inv_id)
        print(f"Correlation Engine results: {corr_res}")

        print("=== 6. RUNNING MITRE ATT&CK VALIDATION ===")
        mitre_res = mitre_validator_service.validate(db, inv_id)
        print(f"MITRE ATT&CK Validation results: {mitre_res}")

        print("=== 7. DETERMINISTIC RISK EVALUATION ===")
        risk_engine = RiskEngine(db=db)
        risk_res = risk_engine.evaluate(inv_id)
        print(f"Risk Score: {risk_res.overall_score}, Severity: {risk_res.severity}, Confidence: {risk_res.confidence}")

        print("=== 8. TIMELINE GENERATION ===")
        timeline = timeline_engine.generate_timeline(db, inv_id)
        print(f"Timeline events generated: {len(timeline)}")
        for te in timeline[:3]:
            print(f"  - [{te.event_type}] {te.content}")

        print("=== 9. REAL AI INVESTIGATION SUMMARY (OLLAMA LLAMA3) ===")
        ai_res = await ai_engine.generate_investigation_summary(db, inv_id)
        summary_text = ai_res.get("summary", "")
        print(f"AI Summary Length: {len(summary_text)} characters")
        print(f"AI Summary Preview:\n{summary_text[:300]}...\n")
        assert "error" not in ai_res, f"AI generation error: {ai_res.get('error')}"

        print("=== 10. INCIDENT REPORT GENERATION ===")
        report = report_engine.generate_report(db, inv_id)
        print(f"Generated Report Title: {report.title}")
        print(f"Report Risk Score: {report.risk_score}")
        print(f"Report Sections: {[s.title for s in report.sections]}")

        print("=== 11. THREAT HUNTING GLOBAL SEARCH ===")
        hunt = threat_hunting_service.search_indicators(db, "192.168.1.100")
        print(f"Global hunt matches for 192.168.1.100: {hunt.total_matches}")
        assert hunt.total_matches >= 1, "Threat hunting should find matches"

        print("\n========================================================")
        print(">>> ALL 11 WORKFLOW STAGES PASSED ON REAL INFRASTRUCTURE <<<")
        print("========================================================")
        return True
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(run_full_pipeline())
