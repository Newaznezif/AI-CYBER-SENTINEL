from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.models.domain import TimelineEvent, NetworkEvent, Observation, DetectionAlert
from app.schemas.timeline import TimelineEventCreate
from app.services.base import BaseService

class TimelineEngineService(BaseService[TimelineEvent, TimelineEventCreate, TimelineEventCreate]):
    
    def generate_timeline(self, db: Session, investigation_id: int) -> List[TimelineEvent]:
        # Delete existing timeline events for this investigation
        db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).delete()
        db.commit()

        events = []

        # Gather Network Events
        network_events = db.query(NetworkEvent).filter(NetworkEvent.investigation_id == investigation_id).all()
        for ne in network_events:
            events.append(
                TimelineEventCreate(
                    investigation_id=investigation_id,
                    timestamp=ne.timestamp,
                    source="Network",
                    event_type="Network Connection",
                    content=f"Connection from {ne.source_ip}:{ne.source_port} to {ne.destination_ip}:{ne.destination_port} over {ne.protocol}",
                    related_id=f"NE-{ne.id}"
                )
            )

        # Gather Observations
        observations = db.query(Observation).filter(Observation.investigation_id == investigation_id).all()
        for ob in observations:
            events.append(
                TimelineEventCreate(
                    investigation_id=investigation_id,
                    timestamp=ob.timestamp or ob.created_at,
                    source=ob.source,
                    event_type=ob.observation_type,
                    content=f"Observation of {ob.observation_type} from {ob.source}",
                    related_id=f"OB-{ob.id}"
                )
            )

        # Gather Detection Alerts
        alerts = db.query(DetectionAlert).filter(DetectionAlert.investigation_id == investigation_id).all()
        for al in alerts:
            events.append(
                TimelineEventCreate(
                    investigation_id=investigation_id,
                    timestamp=al.timestamp,
                    source=al.source,
                    event_type="Detection Alert",
                    content=f"Alert: {al.signature} (Severity: {al.severity})",
                    related_id=f"AL-{al.id}"
                )
            )

        # Sort and save
        events.sort(key=lambda x: x.timestamp)
        saved_events = []
        for e in events:
            db_obj = TimelineEvent(**e.model_dump())
            db.add(db_obj)
            saved_events.append(db_obj)
            
        db.commit()
        return saved_events

    def get_timeline(self, db: Session, investigation_id: int) -> List[TimelineEvent]:
        return db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).order_by(asc(TimelineEvent.timestamp)).all()

timeline_engine = TimelineEngineService(TimelineEvent)
