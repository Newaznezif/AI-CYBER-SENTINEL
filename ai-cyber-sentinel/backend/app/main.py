from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import investigations, indicators, evidence, pcap, threat_intel, hunting

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
        return {
            "API": True,
            "PostgreSQL": False,
            "Ollama": False,
            "Zeek": False,
            "Suricata": False,
            "OTX": False,
            "AbuseIPDB": False,
            "VirusTotal": False
        }

    app.include_router(investigations.router, prefix="/api/v1")
    app.include_router(indicators.router, prefix="/api/v1")
    app.include_router(evidence.router, prefix="/api/v1")
    app.include_router(pcap.router, prefix="/api/v1")
    app.include_router(threat_intel.router, prefix="/api/v1/threat-intel")
    app.include_router(hunting.router, prefix="/api/v1")

    return app

app = create_app()
