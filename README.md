# Svigl

> A multiplayer SVG-based drawing and guessing game.

Svigl is a real-time multiplayer web application inspired by Skribbl.io, except every drawing is constructed from editable SVG primitives instead of freehand raster strokes.

Players draw using vector shapes such as paths, rectangles and circles while others attempt to guess the hidden word in real time. Every drawing is stored as an operation history rather than a static image, enabling replay, validation and future editing.

The project explores backend architecture, real-time systems and WebSockets while delivering a polished product with a modern frontend.

---

## Goals

* Multiplayer rooms supporting **2–10 active players**
* Unlimited spectators
* Real-time drawing synchronization
* Real-time guessing chat
* Turn-based gameplay
* Google authentication and anonymous guests
* SVG-based drawing editor
* Gallery for published drawings
* Replay every drawing from stored operations
* Responsive modern UI

---

## Core principles

**Server authoritative** — The backend owns all game state. Clients only send intentions; the server validates every action.

**Event driven** — Every meaningful action is represented as an event that updates room state and may be persisted for replay.

**Vector first** — No raster drawing. Supported shapes: path, rectangle, circle.

**Replayable documents** — Drawings are stored as operation sequences, not static SVG files.

---

## Technology stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js, TypeScript, Tailwind CSS, Framer Motion, Zustand |
| Backend | FastAPI, native WebSockets, Pydantic, Uvicorn |
| Database | PostgreSQL (Supabase-compatible) |
| Deployment | Docker Compose |

---

## Repository structure

```text
svigl/
├── svigl/              # Next.js frontend
├── backend/            # FastAPI + WebSockets
├── docs/               # Architecture and domain docs
├── docker-compose.yml
└── README.md
```

---

## Development

### Full stack (Docker)

From the repo root:

```bash
docker compose up
```

Starts the frontend (`3000`) and backend (`8000`). For Postgres-backed persistence, set `SVIGL_DATABASE_URL` and apply migrations (see below).

### Local dev

**Frontend**

```bash
cd svigl
npm install
npm run dev
```

**Backend**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Point the frontend at the backend with `svigl/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Key environment variables

| Variable | Where | Purpose |
|----------|-------|---------|
| `NEXT_PUBLIC_WS_URL` | frontend | WebSocket base URL |
| `NEXT_PUBLIC_API_URL` | frontend | REST base for gallery and auth |
| `SVIGL_DATABASE_URL` | backend | Postgres connection string |
| `NEXT_PUBLIC_GOOGLE_CLIENT_ID` | frontend | Google OAuth (optional) |

See `backend/.env.example` for other backend settings.

### Database migrations

Apply manually (no Alembic):

```bash
psql $DATABASE_URL -f backend/migrations/001_gallery_schema.sql
psql $DATABASE_URL -f backend/migrations/002_match_players_stats.sql
```

### Tests

Backend (from `backend/`):

```bash
pip install -r requirements.txt
python -m pytest
```

Frontend production build:

```bash
cd svigl && npm install && npm run build
```

---

## Architecture

Design docs live in [`docs/`](docs/):

- [architecture.md](docs/architecture.md)
- [state_machine.md](docs/state_machine.md)
- [events.md](docs/events.md)
- [domain_model.md](docs/domain_model.md)
- [drawing_model.md](docs/drawing_model.md)
- [database.md](docs/database.md)

---

## Current status

| Area | Status |
|------|--------|
| Real-time multiplayer (2–10 players, spectators) | Done |
| Turn-based rounds, guessing, scoring, chat | Done |
| SVG drawing editor (path, rectangle, circle) | Done |
| Server-authoritative WebSocket protocol | Done |
| Gallery publish + upvote | Done |
| Match history + player statistics (Postgres) | Done |
| Google OAuth sign-in + guest play | Done |
| Backend test suite + GitHub Actions CI | Done |
| Frontend production build | Verified |
