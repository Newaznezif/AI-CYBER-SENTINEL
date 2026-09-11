import logging
import json
from sqlalchemy.orm import Session
from app.repositories.observation import observation_repo
from app.repositories.attack_technique import attack_technique_repo
from app.schemas.attack_technique import AttackTechniqueCreate

logger = logging.getLogger(__name__)

class MitreValidatorService:
    def __init__(self):
        # We can load mapping from a static file or DB.
        # For Phase 14, we demonstrate simple heuristic mapping based on alerts and observations.
        self.signature_to_mitre = {
            "ET MALWARE": ("T1048", "Exfiltration Over Alternative Protocol", "Exfiltration"),
            "ET EXPLOIT": ("T1190", "Exploit Public-Facing Application", "Initial Access"),
            "ET SCAN": ("T1046", "Network Service Discovery", "Discovery"),
            "ET INFO": ("T1082", "System Information Discovery", "Discovery"), 
            "MALICIOUS_NETWORK_TRAFFIC": ("T1071", "Application Layer Protocol", "Command and Control")
        }

    def validate(self, db: Session, investigation_id: int):
        logger.info(f"Running MITRE ATT&CK validation for investigation {investigation_id}")
        
        observations = observation_repo.get_by_investigation(db, investigation_id)
        created_techniques = 0

        for obs in observations:
            matched_ttp = None
            if obs.observation_type == "CORRELATED_ALERT" and obs.data:
                sig = obs.data.get("signature", "")
                for key, ttp in self.signature_to_mitre.items():
                    if key in sig:
                        matched_ttp = ttp
                        break
            elif obs.observation_type == "MALICIOUS_NETWORK_TRAFFIC":
                matched_ttp = self.signature_to_mitre["MALICIOUS_NETWORK_TRAFFIC"]

            if matched_ttp:
                tech_id, tech_name, tactic = matched_ttp
                
                # Check if we already have it
                existing_ttps = attack_technique_repo.get_by_investigation(db, investigation_id)
                if not any(t.technique_id == tech_id for t in existing_ttps):
                    new_ttp = AttackTechniqueCreate(
                        investigation_id=investigation_id,
                        technique_id=tech_id,
                        technique_name=tech_name,
                        tactic=tactic,
                        confidence=obs.confidence,
                        status="VALIDATED" if obs.confidence > 0.8 else "CANDIDATE",
                        supporting_evidence=[{"observation_id": obs.id, "observation_type": obs.observation_type}]
                    )
                    attack_technique_repo.create(db, obj_in=new_ttp)
                    created_techniques += 1

        logger.info(f"MITRE Validation mapped {created_techniques} techniques for investigation_id {investigation_id}")
        return {"status": "success", "techniques_added": created_techniques}

mitre_validator_service = MitreValidatorService()
