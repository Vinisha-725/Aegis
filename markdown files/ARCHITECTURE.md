# Aegis — Architecture

## Overview

Aegis is an AI-powered trust protocol that verifies software development milestones through a multi-agent consensus system and releases escrowed payments automatically upon approval.

```
┌─────────────────────────────────────────────────────────────────────┐
│                          AEGIS SYSTEM                               │
│                                                                     │
│  ┌──────────────┐     ┌──────────────────────────────────────────┐  │
│  │   Frontend   │────▶│               Backend API                │  │
│  │  (Next.js)   │     │              (FastAPI)                   │  │
│  └──────────────┘     └──────────────────────────────────────────┘  │
│                                │                                    │
│                    ┌───────────┼───────────┐                        │
│                    ▼           ▼           ▼                        │
│              ┌──────────┐ ┌────────┐ ┌─────────┐                   │
│              │PostgreSQL│ │ GitHub │ │ Solana  │                   │
│              │    DB    │ │  API   │ │ Devnet  │                   │
│              └──────────┘ └────────┘ └─────────┘                   │
│                                                                     │
│              AI Verification Pipeline:                              │
│                                                                     │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌─────────┐  ┌────────────┐  │
│  │ Argus  │  │ Themis │  │  Dike  │  │ Chronos │  │   Kratos   │  │
│  │(Evidence│  │(Scope  │  │(Quality│  │(Deadline│  │(Consensus  │  │
│  │Gather) │  │ Match) │  │ Score) │  │ Check)  │  │  Engine)   │  │
│  └────────┘  └────────┘  └────────┘  └─────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: React Server Components + Client hooks
- **Linting**: ESLint + Prettier

### Backend
- **Framework**: FastAPI (Python 3.12)
- **ORM**: SQLAlchemy 2.x (async)
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Linting/Formatting**: Ruff
- **Auth**: GitHub OAuth + JWT

### Infrastructure
- **Database**: PostgreSQL 16
- **Containerization**: Docker + Docker Compose
- **CI**: GitHub Actions
- **Deployment**: TBD (Phase 13)

### Blockchain (Phase 11)
- **Chain**: Solana Devnet
- **Token**: Mock USDC (SPL)

## Service Communication

All internal communication between frontend and backend is via REST API (JSON).

Agent-to-agent communication is internal to the backend — agents are Python modules invoked sequentially, not separate services.

## Directory Structure

```
Aegis/
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js App Router pages
│   │   ├── components/    # Reusable UI components
│   │   ├── lib/           # API client, utilities
│   │   └── types/         # TypeScript type definitions
│   └── public/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI route handlers
│   │   │   └── v1/        # API version 1
│   │   ├── agents/        # AI verification agents
│   │   │   ├── argus/
│   │   │   ├── themis/
│   │   │   ├── dike/
│   │   │   ├── chronos/
│   │   │   └── kratos/
│   │   ├── core/          # Config, security, dependencies
│   │   ├── db/            # Database engine and session
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   └── services/      # Business logic layer
│   ├── alembic/           # Database migrations
│   └── tests/             # Pytest test suite
├── docker/                # Dockerfiles + docker-compose.yml
├── docs/                  # Additional documentation
├── .github/workflows/     # CI/CD pipelines
└── [root docs]
```

## Data Flow

### Milestone Verification Flow

```
1. Client submits milestone for verification
2. Backend creates VerificationJob
3. Argus agent collects repository evidence
4. Themis agent validates scope against requirements
5. Dike agent analyzes code quality
6. Chronos agent checks deadline compliance
7. Kratos consensus engine aggregates results
8. If approved: Escrow release is triggered on Solana
9. Reputation score is updated
10. Client and freelancer are notified
```

### Consensus Rules (Kratos)

```python
approved = (
    argus.confidence > 0.70 and
    themis.scope_match > 0.75 and
    dike.quality_score > 0.65
    # chronos.on_time is advisory, not blocking
)
```

## Security Considerations

- All secrets in environment variables (never committed)
- GitHub OAuth tokens stored encrypted
- API endpoints require authentication (Phase 2+)
- Solana transactions require keypair in secure storage
- Database credentials never exposed to frontend

## Future Architecture (Not Building Now)

- **Nemesis**: Dispute resolution agent
- **Plutus**: Streaming micropayments
- **Cross-chain**: Support beyond Solana
- **DAO Governance**: Decentralized parameter control
