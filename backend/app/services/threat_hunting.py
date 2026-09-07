from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.domain import Indicator, DetectionAlert, NetworkEvent, Observation
from app.schemas.threat_hunt import ThreatHuntQuery, HuntResultItem, ThreatHuntResponse

class ThreatHuntingService:
    def hunt(self, db: Session, query: ThreatHuntQuery) -> ThreatHuntResponse:
        results = []
        q = query.query_string.lower()
        
        # Search Indicators
        indicators = db.query(Indicator).filter(
            or_(
                Indicator.value.ilike(f"%{q}%"),
                Indicator.type.ilike(f"%{q}%")
            )
        ).all()
        for ind in indicators:
            results.append(HuntResultItem(
                id=ind.id,
                type="indicator",
                match_field="value/type",
                match_value=ind.value,
                timestamp=ind.created_at,
                investigation_id=ind.investigation_id
            ))
            
        # Search Detection Alerts
        alerts = db.query(DetectionAlert).filter(
            or_(
                DetectionAlert.signature.ilike(f"%{q}%"),
                DetectionAlert.source_ip.ilike(f"%{q}%"),
                DetectionAlert.destination_ip.ilike(f"%{q}%")
            )
        ).all()
        for al in alerts:
            val = al.source_ip if q in (al.source_ip or "").lower() else (al.destination_ip if q in (al.destination_ip or "").lower() else al.signature)
            results.append(HuntResultItem(
                id=al.id,
                type="detection_alert",
                match_field="signature/ip",
                match_value=val,
                timestamp=al.timestamp,
                investigation_id=al.investigation_id
            ))
            
        # Search Network Events
        events = db.query(NetworkEvent).filter(
            or_(
                NetworkEvent.source_ip.ilike(f"%{q}%"),
                NetworkEvent.destination_ip.ilike(f"%{q}%"),
                NetworkEvent.http_host.ilike(f"%{q}%"),
                NetworkEvent.dns_name.ilike(f"%{q}%")
            )
        ).all()
        for ev in events:
            val = ev.source_ip if q in (ev.source_ip or "").lower() else (ev.destination_ip if q in (ev.destination_ip or "").lower() else (ev.http_host if q in (ev.http_host or "").lower() else ev.dns_name))
            results.append(HuntResultItem(
                id=ev.id,
                type="network_event",
                match_field="ip/host/dns",
                match_value=val or q,
                timestamp=ev.timestamp,
                investigation_id=ev.investigation_id
            ))
            
        return ThreatHuntResponse(
            query_string=query.query_string,
            results=results,
            total_matches=len(results)
        )

threat_hunting_service = ThreatHuntingService()
