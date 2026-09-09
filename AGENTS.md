# AI-CYBER SENTINEL

## Project Overview

AI-Cyber Sentinel is a defensive cybersecurity platform designed to help analysts investigate suspicious activity by combining PCAP analysis, network telemetry, IDS/IPS alerts, security logs, threat-intelligence enrichment, MITRE ATT&CK mapping, deterministic risk scoring, AI-assisted analysis, and more.

The system operates strictly as an evidence-first analytical assistant.

## Features

- Complete incident investigation workflow.
- Indicator extraction, scoring, and management.
- PCAP and log parsing and analysis using zeek/suricata/scapy.
- Multi-provider CTI (Cyber Threat Intelligence) enrichment.
- Deterministic Risk assessment based on local rule-set.
- Local, private AI investigation using Ollama.
- MITRE ATT&CK extraction and defense evaluation.
- Incident report generation and threat response recommendation.

## Architecture

See `docs/architecture.md` for full component breakdown. Key pieces include:

- Next.js TypeScript Frontend
- FastAPI Python Backend
- PostgreSQL DB
- PCAP, Zeek, & Suricata Analysis Services
- CTI Managers & Correlation Engines
- Local AI via Ollama

## Technology Stack

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL
- **AI**: Ollama
- **Infrastructure**: Docker, Docker Compose

## Installation

(Docker is the primary deployment target, but local builds are fully supported via WSL2/Linux).

## Docker Setup

```bash
docker-compose up -d
```

Contains services for Frontend, Backend, PostgreSQL, and Ollama.

## Environment Variables

Copy `.env.example` to `.env` and fill in necessary details (DB endpoints, API keys).

## Running the Application

Check `Makefile` targets.
To run locally without docker:

- Backend: `cd backend && uvicorn app.main:app --reload`
- Frontend: `cd frontend && npm run dev`

## Adding CTI API Keys

Add keys in backend `.env` variables for `OTX_API_KEY`, `ABUSEIPDB_API_KEY`, and `VIRUSTOTAL_API_KEY`. These are never exposed to the frontend.

## Installing Zeek

Run on Ubuntu: `apt-get install zeek` or run zeek via the provided container (future phase).

## Installing Suricata

Run on Ubuntu: `apt-get install suricata`. Suricata is parsed when PCAP processes produce events.

## Running Ollama

Install Ollama from <https://ollama.ai/>. Used as the Local Inference Engine for assessment correlations.

## Running Tests

Run backend tests with `pytest` and frontend tests with `jest`.

## Demo Investigation

(Refer to `sample-data` and Phase 25/26 of Roadmap for mock lab info).

## Project Structure

Standard API -> Service -> Repository format.

## Security Considerations

Refer to `docs/security.md` and `docs/threat-model.md`.

## Limitations

This is a defensive product and must NOT be connected directly to production control networks for autonomous prevention without human guardrails.

## Roadmap

Refer to `docs/development-roadmap.md`.
