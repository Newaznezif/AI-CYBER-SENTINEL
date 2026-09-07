# Project Audit & Restoration Plan

## Current Architecture
The AI-Cyber Sentinel architecture follows a microservice-like composite structure:
- **Frontend**: Next.js 15, TailwindCSS, React. Located in `./frontend`
- **Backend**: FastAPI (Python), SQLAlchemy. Located in `./backend`
- **Database**: PostgreSQL
- **AI/LLM**: Ollama

## What went wrong? (Commit 730b3d5)
In commit `730b3d5 Apply local changes`, the entire backend architecture nested within `ai-cyber-sentinel/backend` was deleted from the tree. The initial commit (`4759370`) placed the backend nested unfortunately, which explains why it was dropped, as it didn't align with `docker-compose.yml` mapped to `./backend`. The frontend UI was also left entirely absent/empty in the initial commit.

## Missing Functionality & Frontend Status
The frontend was rebuilt successfully in the current workspace, utilizing mocked JSON arrays (`mockInvestigations`, `mockIndicators`, `mockChartData`). However, this mock state violates true functionality completion requirements.

## Recoverable Functionality
I successfully verified that the backend could be fully restored from Git History using `git checkout 4759370 -- ai-cyber-sentinel/backend` and relocated properly to `./backend`. The repository now accurately mimics the required structure.

## Backend Status
- **Restored**: The FastAPI framework, SQLAlchemy ORM models, Routing patterns (Investigations, Evidence, CTI), and Pydantic schemas.
- **Required Action**: I must configure `.env`, load PostgreSQL, verify the API works, and connect the UI.

## Recommended Restoration Strategy
1. **Audit Database**: Examine `backend/app/models/` and verify Alembic migrations can execute or SQLAlchemy `create_all()` works.
2. **Backend Startup**: Start `uvicorn app.main:app` locally to verify Python endpoints.
3. **Frontend API Wrapping**: Refactor `/investigations`, `/intelligence`, and `/page.tsx` (Dashboard) in the frontend to rip out the mock arrays and connect to `http://localhost:8000` via Axios/Fetch hooks.
4. **End-to-End Validation**: Submit a sample case, process it through the API, and verify the Frontend updates with the exact deterministic risk scoring returned by the backend rules.
