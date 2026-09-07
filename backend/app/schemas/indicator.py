import re
import ipaddress
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator

class IndicatorBase(BaseModel):
    investigation_id: int
    type: str
    value: str
    source: str
    confidence: float = 0.0

class IndicatorCreate(IndicatorBase):
    @field_validator("type")
    @classmethod
    def format_type(cls, v: str) -> str:
        return v.upper()

    @model_validator(mode="after")
    def validate_value_for_type(self) -> 'IndicatorCreate':
        ind_type = self.type
        v = self.value
        
        try:
            if ind_type == "IPV4":
                ipaddress.IPv4Address(v)
            elif ind_type == "IPV6":
                ipaddress.IPv6Address(v)
            elif ind_type == "MD5" and not re.match(r"^[a-fA-F0-9]{32}$", v):
                raise ValueError("MD5 must be exactly 32 hexadecimal characters")
            elif ind_type == "SHA1" and not re.match(r"^[a-fA-F0-9]{40}$", v):
                raise ValueError("SHA1 must be exactly 40 hexadecimal characters")
            elif ind_type == "SHA256" and not re.match(r"^[a-fA-F0-9]{64}$", v):
                raise ValueError("SHA256 must be exactly 64 hexadecimal characters")
        except ipaddress.AddressValueError:
            raise ValueError(f"Invalid {ind_type} address format")
            
        return self

class IndicatorUpdate(BaseModel):
    confidence: Optional[float] = None

class IndicatorInDBBase(IndicatorBase):
    id: int
    normalized_value: str
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class IndicatorResponse(IndicatorInDBBase):
    pass
