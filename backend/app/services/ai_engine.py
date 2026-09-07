import logging
import httpx
from sqlalchemy.orm import Session
from app.config import settings
from app.repositories.investigation import investigation_repo
from app.repositories.observation import observation_repo
from app.repositories.attack_technique import attack_technique_repo

logger = logging.getLogger(__name__)

class AIEngine:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    async def generate_investigation_summary(self, db: Session, investigation_id: int):
        investigation = investigation_repo.get(db, id=investigation_id)
        if not investigation:
            raise ValueError("Investigation not found")

        observations = observation_repo.get_by_investigation(db, investigation_id)
        techniques = attack_technique_repo.get_by_investigation(db, investigation_id)

        prompt = f"Analyze the following security investigation: {investigation.title}\n"
        prompt += f"Description: {investigation.description}\n"
        
        prompt += "\nObservations:\n"
        for obs in observations:
            prompt += f"- Type: {obs.observation_type}, Confidence: {obs.confidence}, Data: {obs.data}\n"

        prompt += "\nMITRE ATT&CK Tactics:\n"
        for t in techniques:
            prompt += f"- {t.technique_id}: {t.technique_name} ({t.tactic})\n"

        prompt += "\nPlease provide a concise security analysis summary, identifying the primary threats and risk level."

        # Make the request to Ollama
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                
                summary = data.get("response", "No summary generated.")
                
                # We could update the database or just return it to the caller
                return {"summary": summary, "prompt_length": len(prompt)}
        except httpx.HTTPError as e:
            logger.error(f"Error accessing Ollama AI Engine: {str(e)}")
            return {"summary": "AI Engine unavailable.", "error": str(e)}

ai_engine = AIEngine()
