from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class NetworkEventBase(BaseModel):
    investigation_id: int
    source_ip: str
    destination_ip: str
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    protocol: Optional[str] = None
    timestamp: Optional[datetime] = None
    direction: Optional[str] = None
    bytes: Optional[int] = None
    packets: Optional[int] = None
    dns_name: Optional[str] = None
    http_host: Optional[str] = None
    http_method: Optional[str] = None
    http_uri: Optional[str] = None
    user_agent: Optional[str] = None
    status_code: Optional[int] = None
    tls_metadata: Optional[Dict[str, Any]] = None

class NetworkEventCreate(NetworkEventBase):
    pass

class NetworkEventUpdate(NetworkEventBase):
    pass

class NetworkEventResponse(NetworkEventBase):
    id: int

    class Config:
        from_attributes = True
