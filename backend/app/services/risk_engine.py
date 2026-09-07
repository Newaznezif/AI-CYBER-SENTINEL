import logging
from sqlalchemy.orm import Session

from app.repositories.indicator import indicator_repo
from app.repositories.detection_alert import detection_alert_repo
from app.repositories.threat_intel import threat_intel_repo
from app.repositories.attack_technique import attack_technique_repo
from app.repositories.risk_assessment import risk_assessment_repo
from app.schemas.risk_assessment import RiskAssessmentCreate
from app.services.investigation import investigation_service
from app.schemas.investigation import InvestigationUpdate

logger = logging.getLogger(__name__)

class RiskEngine:
    def __init__(self, db: Session):
        self.db = db

    def evaluate(self, investigation_id: int):
        logger.info(f"Running Deterministic Risk Engine on investigation {investigation_id}")
        
        investigation = investigation_service.get(self.db, id=investigation_id)
        if not investigation:
            raise ValueError("Investigation not found")

        # Gather inputs
        indicators = indicator_repo.get_by_investigation(self.db, investigation_id)
        alerts = detection_alert_repo.get_by_investigation(self.db, investigation_id)
        ttps = attack_technique_repo.get_by_investigation(self.db, investigation_id)

        # 1. Threat Intel Score
        ti_score = 0.0
        malicious_indicators = 0
        for ind in indicators:
            results = threat_intel_repo.get_by_indicator(self.db, ind.id)
            if any(r.reputation == "MALICIOUS" for r in results):
                malicious_indicators += 1
        
        if malicious_indicators > 0:
            ti_score = min(20.0 * malicious_indicators, 100.0)

        # 2. Detection Score
        det_score = 0.0
        high_alerts = sum(1 for a in alerts if a.severity in ["High", "Critical"])
        if high_alerts > 0:
            det_score = min(25.0 * high_alerts, 100.0)

        # 3. Exploitation Score (MITRE)
        exp_score = 0.0
        if len(ttps) > 0:
            exp_score = min(30.0 * len(ttps), 100.0)

        # Aggregate Score (Weighted sum for example)
        # 35% TI, 35% Detections, 30% Exploitation/TTPs
        overall = (ti_score * 0.35) + (det_score * 0.35) + (exp_score * 0.30)
        
        # Calculate Severity
        severity = "LOW"
        if overall >= 75:
            severity = "CRITICAL"
        elif overall >= 50:
            severity = "HIGH"
        elif overall >= 25:
            severity = "MEDIUM"

        explanation = f"Risk evaluated from {malicious_indicators} malicious indicators, {high_alerts} high-severity alerts, and {len(ttps)} MITRE techniques."
        
        # Calculate Confidence
        confidence = 1.0 if (len(indicators) > 0 or len(alerts) > 0 or len(ttps) > 0) else 0.5 

        # Save Assessment
        ra = RiskAssessmentCreate(
            investigation_id=investigation_id,
            overall_score=overall,
            severity=severity,
            confidence=confidence,
            threat_intelligence_score=ti_score,
            network_evidence_score=0.0,
            detection_score=det_score,
            exploitation_score=exp_score,
            historical_score=0.0,
            asset_criticality_score=0.0,
            explanation=explanation
        )
        
        saved_ra = risk_assessment_repo.create(self.db, obj_in=ra)

        # Update Investigation status/severity to match if higher
        investigation_service.update(self.db, db_obj=investigation, obj_in=InvestigationUpdate(
            severity=severity,
            confidence=confidence
        ))

        return saved_ra

