from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

class Investigation(Base):
    __tablename__ = "investigations"
    id = Column(Integer, primary_key=True, index=True)
    investigation_number = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="NEW")
    severity = Column(String, default="INFO")
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

class Indicator(Base):
    __tablename__ = "indicators"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    type = Column(String, index=True)
    value = Column(String, index=True)
    normalized_value = Column(String, index=True)
    source = Column(String)
    confidence = Column(Float, default=0.0)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    type = Column(String, index=True)
    filename = Column(String)
    sha256 = Column(String, index=True)
    size = Column(Integer)
    source = Column(String)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    evidence_id = Column(Integer, ForeignKey("evidence.id"), nullable=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"), nullable=True)
    observation_type = Column(String, index=True)
    timestamp = Column(DateTime, nullable=True)
    source = Column(String)
    confidence = Column(Float, default=0.0)
    data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

class NetworkEvent(Base):
    __tablename__ = "network_events"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    source_ip = Column(String, index=True)
    destination_ip = Column(String, index=True)
    source_port = Column(Integer, nullable=True)
    destination_port = Column(Integer, nullable=True)
    protocol = Column(String, nullable=True)
    timestamp = Column(DateTime, nullable=True)
    direction = Column(String, nullable=True)
    bytes = Column(Integer, nullable=True)
    packets = Column(Integer, nullable=True)
    dns_name = Column(String, nullable=True)
    http_host = Column(String, nullable=True)
    http_method = Column(String, nullable=True)
    http_uri = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    status_code = Column(Integer, nullable=True)
    tls_metadata = Column(JSON, nullable=True)

class ThreatIntelResult(Base):
    __tablename__ = "threat_intel_results"
    id = Column(Integer, primary_key=True, index=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"))
    provider = Column(String, index=True)
    query_type = Column(String)
    reputation = Column(String)
    confidence = Column(Float, default=0.0)
    categories = Column(JSON, default=list)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    raw_response = Column(JSON, default=dict)
    queried_at = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True)
    error = Column(String, nullable=True)

class DetectionAlert(Base):
    __tablename__ = "detection_alerts"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    source = Column(String, index=True)
    signature = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime, nullable=True)
    source_ip = Column(String, nullable=True)
    destination_ip = Column(String, nullable=True)
    protocol = Column(String, nullable=True)
    raw_alert = Column(JSON, default=dict)

class AttackTechnique(Base):
    __tablename__ = "attack_techniques"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    technique_id = Column(String, index=True)
    technique_name = Column(String)
    tactic = Column(String)
    confidence = Column(Float, default=0.0)
    status = Column(String, default="CANDIDATE")
    supporting_evidence = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    overall_score = Column(Float, default=0.0)
    severity = Column(String, default="LOW")
    confidence = Column(Float, default=0.0)
    threat_intelligence_score = Column(Float, default=0.0)
    network_evidence_score = Column(Float, default=0.0)
    detection_score = Column(Float, default=0.0)
    exploitation_score = Column(Float, default=0.0)
    historical_score = Column(Float, default=0.0)
    asset_criticality_score = Column(Float, default=0.0)
    explanation = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    category = Column(String)
    priority = Column(String)
    action = Column(String)
    reason = Column(String)
    evidence = Column(JSON, default=list)
    status = Column(String, default="PENDING")

class TimelineEvent(Base):
    __tablename__ = "timeline_events"
    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(Integer, ForeignKey("investigations.id"))
    timestamp = Column(DateTime)
    source = Column(String)
    event_type = Column(String)
    content = Column(String)
    related_id = Column(String, nullable=True)
