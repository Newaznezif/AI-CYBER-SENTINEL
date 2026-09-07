from sqlalchemy.orm import Session
from datetime import datetime
from app.models.domain import Investigation, Indicator, DetectionAlert, RiskAssessment, TimelineEvent
from app.schemas.report import InvestigationReport, ReportSection

class ReportEngineService:
    
    def generate_report(self, db: Session, investigation_id: int) -> InvestigationReport:
        inv = db.query(Investigation).filter(Investigation.id == investigation_id).first()
        if not inv:
            raise ValueError("Investigation not found")

        # Gather context
        indicators = db.query(Indicator).filter(Indicator.investigation_id == investigation_id).all()
        alerts = db.query(DetectionAlert).filter(DetectionAlert.investigation_id == investigation_id).all()
        risk = db.query(RiskAssessment).filter(RiskAssessment.investigation_id == investigation_id).order_by(RiskAssessment.id.desc()).first()
        timeline = db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).order_by(TimelineEvent.timestamp.asc()).all()

        sections = []
        
        # Section 1: Indicators Overview
        ind_content = f"Total Indicators: {len(indicators)}\n"
        for ind in indicators:
            ind_content += f"- [{ind.type}] {ind.value} (Confidence: {ind.confidence})\n"
        sections.append(ReportSection(title="Extracted Indicators of Compromise (IoCs)", content=ind_content))

        # Section 2: Detections
        det_content = f"Total Alerts triggered: {len(alerts)}\n"
        for al in alerts:
            det_content += f"- [{al.severity}] {al.signature} @ {al.timestamp} ({al.source_ip} -> {al.destination_ip})\n"
        sections.append(ReportSection(title="Detection Alerts", content=det_content))

        # Section 3: Timeline
        time_content = ""
        for te in timeline:
            time_content += f"[{te.timestamp}] {te.event_type} - {te.content}\n"
        if not time_content:
            time_content = "Timeline empty or not yet generated."
        sections.append(ReportSection(title="Incident Timeline", content=time_content))

        # Compile report
        report = InvestigationReport(
            investigation_id=inv.id,
            generated_at=datetime.utcnow(),
            title=inv.title or f"Investigation {inv.id}",
            summary=inv.description or "Automated investigation analysis report.",
            status=inv.status,
            severity=inv.severity,
            risk_score=risk.overall_score if risk else 0.0,
            sections=sections,
            metadata={
                "indicator_count": len(indicators),
                "alert_count": len(alerts),
                "timeline_events": len(timeline)
            }
        )
        
        return report

report_engine = ReportEngineService()
