# Aegis

**AI-powered trust protocol that verifies software development milestones using AI agents and automatically releases escrowed payments.**

## Overview

Aegis connects GitHub repositories to an AI verification pipeline:

```
GitHub Repository → AI Verification → Agent Consensus → Escrow Release → Reputation Update
```

### AI Verification Agents

| Agent | Responsibility |
|-------|---------------|
| **Argus** | Evidence gathering — verifies work exists (commits, files changed) |
| **Themis** | Scope validation — compares milestone requirements to actual changes |
| **Dike** | Quality analysis — code quality, documentation, implementation completeness |
| **Chronos** | Deadline verification — confirms submission is on time |
| **Kratos** | Consensus engine — aggregates agent results and produces final verdict |

## Getting Started

### Prerequisites
- Docker & Docker Compose v2
- Node.js 20+ (for local frontend dev)
- Python 3.12+ (for local backend dev)

### Run Locally (One Command)

```bash
cp .env.example .env
# Fill in required values in .env
docker compose -f docker/docker-compose.yml up --build
```

Services:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

### Development Setup

#### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Database Migrations
```bash
cd backend
alembic upgrade head
```

## Project Structure

```
Aegis/
├── frontend/           # Next.js 14 (TypeScript)
├── backend/            # FastAPI (Python 3.12)
├── docker/             # Docker Compose + Dockerfiles
├── docs/               # Architecture & agent specifications
├── ARCHITECTURE.md     # System architecture
├── AGENT_SPECIFICATIONS.md  # AI agent specs
├── CHANGELOG.md        # Version history
└── PROJECT_PROGRESS.md # Phase tracking
```

## Documentation

- [Architecture](./ARCHITECTURE.md)
- [Agent Specifications](./AGENT_SPECIFICATIONS.md)
- [Changelog](./CHANGELOG.md)
- [Project Progress](./PROJECT_PROGRESS.md)

## License

MIT
