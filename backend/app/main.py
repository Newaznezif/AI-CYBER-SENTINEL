from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import investigations, indicators, evidence, pcap, threat_intel, hunting

import httpx
from sqlalchemy import text
from app.database.session import engine
from analyzers.suricata.parser import check_suricata_availability
from analyzers.zeek.parser import check_zeek_availability

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

    @app.get("/api/v1/system-health")
    def health_check():
        db_ok = False
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                db_ok = True
        except Exception:
            pass

        ollama_ok = False
        try:
            r = httpx.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=2.0)
            ollama_ok = r.status_code == 200
        except Exception:
            pass

        return {
            "API": True,
            "PostgreSQL": db_ok,
            "Ollama": ollama_ok,
            "Zeek": check_zeek_availability(),
            "Suricata": check_suricata_availability(),
            "OTX": bool(settings.OTX_API_KEY),
            "AbuseIPDB": bool(settings.ABUSEIPDB_API_KEY),
            "VirusTotal": bool(settings.VIRUSTOTAL_API_KEY)
        }

    app.include_router(investigations.router, prefix="/api/v1")
    app.include_router(indicators.router, prefix="/api/v1")
    app.include_router(evidence.router, prefix="/api/v1")
    app.include_router(pcap.router, prefix="/api/v1")
    app.include_router(threat_intel.router, prefix="/api/v1/threat-intel")
    app.include_router(hunting.router, prefix="/api/v1")

    return app

app = create_app()
