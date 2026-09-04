from typing import List, Dict, Any
from .base import CTIProvider, CTIResponse
import httpx

class AbuseIPDBProvider(CTIProvider):
    def _setup_client(self):
        self.client.headers.update({
            'Accept': 'application/json',
            'Key': self.api_key
        })

    def get_name(self) -> str:
        return "AbuseIPDB"

    def supports_type(self, indicator_type: str) -> bool:
        return indicator_type in ["IPV4", "IPV6"]

    async def enrich_indicator(self, indicator_value: str, indicator_type: str) -> CTIResponse:
        url = 'https://api.abuseipdb.com/api/v2/check'
        params = {
            'ipAddress': indicator_value,
            'maxAgeInDays': '90',
            'verbose': 'true'
        }
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Parsing AbuseIPDB response
            resp_data = data.get('data', {})
            abuse_score = resp_data.get('abuseConfidenceScore', 0)
            
            reputation = "MALICIOUS" if abuse_score > 50 else "SUSPICIOUS" if abuse_score > 0 else "BENIGN"
            confidence = float(abuse_score) / 100.0
            
            categories = []
            if resp_data.get('usageType'):
                categories.append(f"Usage: {resp_data['usageType']}")
            if resp_data.get('isp'):
                categories.append(f"ISP: {resp_data['isp']}")

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
