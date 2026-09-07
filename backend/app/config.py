from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Cyber Sentinel"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ai_cyber_sentinel"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    
    # CTI Keys
    OTX_API_KEY: str | None = None
    ABUSEIPDB_API_KEY: str | None = None
    VIRUSTOTAL_API_KEY: str | None = None
    
    MOCK_CTI: bool = False
    DEMO_MODE: bool = False
    LOG_LEVEL: str = "INFO"
    MAX_UPLOAD_SIZE: int = 52428800

    class Config:
        env_file = ".env"

settings = Settings()
