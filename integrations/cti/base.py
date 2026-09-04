from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict
import httpx

class CTIResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    provider: str
    reputation: str
    confidence: float = 0.0
    categories: List[str] = []
    raw_response: Dict[str, Any] = {}
    success: bool = True
    error: Optional[str] = None
    
class CTIProvider(ABC):
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=10.0)
        if self.api_key:
            self._setup_client()

    def _setup_client(self):
        """Setup headers or auth based on api key, implemented by subclass optionally."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the CTI provider."""
        pass

    @abstractmethod
    def supports_type(self, indicator_type: str) -> bool:
        """Check if the provider supports the given indicator type."""
        pass

    @abstractmethod
    async def enrich_indicator(self, indicator_value: str, indicator_type: str) -> CTIResponse:
        """Enrich a specific indicator."""
        pass
        
    async def close(self):
        await self.client.aclose()
