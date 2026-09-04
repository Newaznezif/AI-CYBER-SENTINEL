import logging
from sqlalchemy.orm import Session
from datetime import datetime

from app.repositories.indicator import indicator_repo
from app.repositories.network_event import network_event_repo
from app.repositories.detection_alert import detection_alert_repo
from app.repositories.threat_intel import threat_intel_repo
from app.repositories.observation import observation_repo
from app.schemas.observation import ObservationCreate

logger = logging.getLogger(__name__)

class CorrelationEngine:
    def __init__(self, db: Session):
        self.db = db

    def run(self, investigation_id: int):
        '''Runs the correlation tree generator on the specified investigation.'''
        logger.info(f"Starting correlation block for investigation_id {investigation_id}")
        
        # 1. Gather context
        indicators = indicator_repo.get_by_investigation(self.db, investigation_id)
        network_events = network_event_repo.get_by_investigation(self.db, investigation_id)
        alerts = detection_alert_repo.get_by_investigation(self.db, investigation_id)

        # Basic sets for matching logic
        indicator_values = {i.value: i for i in indicators}
        
        observations_created = 0

        # 2. Correlate Alerts
        for alert in alerts:
            # Check if alert contains an indicator
            matched_indicator = None
            if alert.source_ip in indicator_values:
                matched_indicator = indicator_values[alert.source_ip]
            elif alert.destination_ip in indicator_values:
                matched_indicator = indicator_values[alert.destination_ip]

            if matched_indicator:
                obs = ObservationCreate(
                    investigation_id=investigation_id,
                    observation_type="CORRELATED_ALERT",
                    source=alert.source,
                    indicator_id=matched_indicator.id,
                    timestamp=alert.timestamp or datetime.utcnow(),
                    confidence=0.8,
                    data={"alert_id": alert.id, "signature": alert.signature, "severity": alert.severity}
                )
                observation_repo.create(self.db, obj_in=obs)
                observations_created += 1

        # 3. Correlate Network Events -> Threat Intel / Malicious Indicators
        for ne in network_events:
            for ip in [ne.source_ip, ne.destination_ip]:
                if ip and ip in indicator_values:
                    ind = indicator_values[ip]
                    
                    # See if intel considers it malicious
                    intel_results = threat_intel_repo.get_by_indicator(self.db, ind.id)
                    is_malicious = any(tr.reputation == "MALICIOUS" for tr in intel_results)
                    
                    if is_malicious:
                        obs = ObservationCreate(
                            investigation_id=investigation_id,
                            observation_type="MALICIOUS_NETWORK_TRAFFIC",
                            source="CORRELATION_ENGINE",
                            indicator_id=ind.id,
                            timestamp=ne.timestamp,
                            confidence=0.9,
                            data={"network_event_id": ne.id, "protocol": ne.protocol}
                        )
                        observation_repo.create(self.db, obj_in=obs)
                        observations_created += 1
        
        logger.info(f"Correlation finished for investigation_id {investigation_id}. {observations_created} observations created.")
        return {"status": "success", "observations_created": observations_created}

