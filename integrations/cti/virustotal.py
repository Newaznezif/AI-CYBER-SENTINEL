from typing import List, Dict, Any
from .base import CTIProvider, CTIResponse
import httpx
import base64

class VirusTotalProvider(CTIProvider):
    def _setup_client(self):
        self.client.headers.update({
            'x-apikey': self.api_key,
            'accept': 'application/json'
        })

    def get_name(self) -> str:
        return "VirusTotal"

    def supports_type(self, indicator_type: str) -> bool:
        return indicator_type in ["IPV4", "IPV6", "DOMAIN", "URL", "MD5", "SHA1", "SHA256"]

    async def enrich_indicator(self, indicator_value: str, indicator_type: str) -> CTIResponse:
        ep_map = {
            "IPV4": f"ip_addresses/{indicator_value}",
            "IPV6": f"ip_addresses/{indicator_value}",
            "DOMAIN": f"domains/{indicator_value}",
            "MD5": f"files/{indicator_value}",
            "SHA1": f"files/{indicator_value}",
            "SHA256": f"files/{indicator_value}"
        }
        
        if indicator_type == "URL":
            url_id = base64.urlsafe_b64encode(indicator_value.encode()).decode().strip("=")
            endpoint = f"urls/{url_id}"
        else:
            endpoint = ep_map[indicator_type]
            
        url = f"https://www.virustotal.com/api/v3/{endpoint}"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            total = sum(stats.values()) if stats else 1
            
            score = (malicious + suspicious) / total if total > 0 else 0
            
            # Additional tags or categories
            tags = data.get("data", {}).get("attributes", {}).get("tags", [])
            categories = tags[:5] if isinstance(tags, list) else []
            
            reputation = "MALICIOUS" if malicious > 0 else "SUSPICIOUS" if suspicious > 0 else "BENIGN"
            if malicious == 0 and suspicious == 0 and stats.get("undetected", 0) == 0 and stats.get("harmless", 0) == 0:
                reputation = "UNKNOWN"
            
            return CTIResponse(
                provider=self.get_name(),
                reputation=reputation,
                confidence=score,
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
