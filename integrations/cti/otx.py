from typing import List, Dict, Any
from .base import CTIProvider, CTIResponse
import httpx

class OTXProvider(CTIProvider):
    def _setup_client(self):
        self.client.headers.update({
            'X-OTX-API-KEY': self.api_key,
            'Accept': 'application/json'
        })

    def get_name(self) -> str:
        return "AlienVault OTX"

    def supports_type(self, indicator_type: str) -> bool:
        return indicator_type in ["IPV4", "IPV6", "DOMAIN", "MD5", "SHA1", "SHA256"]

    async def enrich_indicator(self, indicator_value: str, indicator_type: str) -> CTIResponse:
        ep_map = {
            "IPV4": "IPv4",
            "IPV6": "IPv6",
            "DOMAIN": "domain",
            "MD5": "file",
            "SHA1": "file",
            "SHA256": "file"
        }
        
        otx_type = ep_map[indicator_type]
        url = f"https://otx.alienvault.com/api/v1/indicators/{otx_type}/{indicator_value}/general"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            pulse_info = data.get("pulse_info", {})
            pulse_count = pulse_info.get("count", 0)
            pulses = pulse_info.get("pulses", [])
            
            categories = list(set([tag for p in pulses for tag in p.get("tags", [])]))[:5]
            
            reputation = "MALICIOUS" if pulse_count > 2 else "SUSPICIOUS" if pulse_count > 0 else "BENIGN"
            confidence = min(pulse_count * 0.2, 1.0)
            
            return CTIResponse(
                provider=self.get_name(),
                reputation=reputation,
                confidence=confidence,
                categories=categories,
                raw_response=data,
                success=True
            )
        except httpx.HTTPError as e:
            return CTIResponse(
                provider=self.get_name(),
                reputation="UNKNOWN",
                confidence=0.0,
                categories=[],
                raw_response={},
                success=False,
                error=str(e)
            )
