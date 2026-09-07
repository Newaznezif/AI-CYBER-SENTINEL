import logging
import asyncio
from typing import List
from sqlalchemy.orm import Session

from app.schemas.threat_intel import ThreatIntelResultCreate
from app.repositories.threat_intel import threat_intel_repo
from app.schemas.indicator import IndicatorResponse

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from integrations.cti.base import CTIProvider

logger = logging.getLogger(__name__)

class CTIManager:
    def __init__(self, providers: List[CTIProvider]):
        self.providers = providers

    async def _enrich_with_provider(
        self,
        db: Session,
        provider: CTIProvider,
        indicator: IndicatorResponse
    ) -> None:
        if not provider.supports_type(indicator.type):
            return
            
        logger.info(f"Enriching {indicator.value} with {provider.get_name()}")
        try:
            response = await provider.enrich_indicator(indicator.value, indicator.type)
            
            new_threat_intel = ThreatIntelResultCreate(
                indicator_id=indicator.id,
                provider=response.provider,
                query_type=indicator.type,
                reputation=response.reputation,
                confidence=response.confidence,
                categories=response.categories,
                raw_response=response.raw_response,
                success=response.success,
                error=response.error
            )
            
            # Since this is async but SQLAlchemy is typically sync unless we use asyncSession,
            # this might be running in a threadpool or using a synchronous session. 
            # In production, we'd need to ensure thread safety of `db` if we're gathering tasks.
            # But for standard sync db usage, we might just be passing the session normally.
            threat_intel_repo.create(db, obj_in=new_threat_intel)
            logger.info(f"Successfully enriched {indicator.value} with {provider.get_name()}")
        except Exception as e:
            logger.error(f"Error enriching {indicator.value} with {provider.get_name()}: {str(e)}")
            new_threat_intel = ThreatIntelResultCreate(
                indicator_id=indicator.id,
                provider=provider.get_name(),
                query_type=indicator.type,
                success=False,
                error=str(e)
            )
            threat_intel_repo.create(db, obj_in=new_threat_intel)

    async def enrich_indicator(self, db: Session, indicator: IndicatorResponse) -> None:
        """Enrich a single indicator using all supported and configured CTI providers."""
        # Using a simple loop instead of asyncio.gather if DB session is sync, to avoid concurrent session usage errors.
        for provider in self.providers:
            await self._enrich_with_provider(db, provider, indicator)

