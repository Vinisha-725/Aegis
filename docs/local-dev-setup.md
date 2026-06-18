# Local Development Setup

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Docker Desktop | 4.x+ | [docker.com](https://docker.com) |
| Node.js | 20+ | [nodejs.org](https://nodejs.org) |
| Python | 3.12+ | [python.org](https://python.org) |
| Git | Any | — |

## 1. Clone & Configure

```bash
git clone https://github.com/Vinisha-725/Aegis.git
cd Aegis
cp .env.example .env
```

Edit `.env` and fill in:
- `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` (create an OAuth App at github.com/settings/developers)
- `ANTHROPIC_API_KEY` (for Phase 6+)
- `SECRET_KEY` (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)

## 2. Run with Docker (Recommended)

```bash
docker compose -f docker/docker-compose.yml up --build
```

Wait for all services to become healthy, then visit:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 3. Run Backend Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Start PostgreSQL via Docker only
docker compose -f docker/docker-compose.yml up postgres -d

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8000
```

## 4. Run Frontend Locally

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

## 5. Database Migrations

```bash
cd backend

# Apply all migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "description of change"

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history --verbose
```

## 6. Running Tests

### Backend
```bash
cd backend
pytest tests/ -v
```

### Frontend
```bash
cd frontend
npm run lint
npm run type-check
```

## 7. Linting & Formatting

### Backend (Ruff)
```bash
cd backend
ruff check .          # Check for issues
ruff check --fix .    # Auto-fix issues
ruff format .         # Format code
```

### Frontend (ESLint + Prettier)
```bash
cd frontend
npm run lint          # Check
npm run lint:fix      # Auto-fix
npm run format        # Format with Prettier
```

## Environment Variables Reference

See [../.env.example](../.env.example) for all available variables with descriptions.
