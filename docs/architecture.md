# Architecture

> Target architecture for Svigl. The repo currently ships a **frontend prototype** with mocked data and an empty backend skeleton. Use this document when implementing server features.

---

## Overview

Svigl is a real-time multiplayer drawing and guessing game. Players draw with SVG vector shapes while others guess the hidden word.

```text
Browser (Next.js)
       │
       │  HTTP (gallery, auth)
       │  WebSocket (game events)
       ▼
FastAPI backend
       │
       │  SQLAlchemy
       ▼
PostgreSQL / Supabase
```

---

## Core principles

### Server authoritative

The backend owns all game state. Clients never decide:

* Scores, winners, turn order
* Words, timers, document validity

Clients only send **intentions**. The server validates every action.

### Event driven

Every meaningful action is an event (`player.joined`, `shape.committed`, `guess.submit`, etc.). Events update room state and may be persisted for replay.

### Vector first

No raster drawing. Shapes are path, rectangle, and circle primitives. See [drawing_model.md](drawing_model.md).

### Replayable documents

Drawings are stored as operation history, not static SVG files. See [drawing_model.md](drawing_model.md).

### Server simplicity (v1)

* In-memory room state
* FastAPI native WebSockets (no Socket.IO)
* Postgres for persistence only
* No Redis / horizontal scaling in v1

---

## Technology stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js, TypeScript, Tailwind CSS, Zustand, Framer Motion |
| Backend | FastAPI, Pydantic, Uvicorn |
| Real-time | Native WebSockets |
| Database | PostgreSQL (Supabase-compatible) |
| Deployment | Docker Compose |

---

## Repository layout

```text
svigl/
├── svigl/              # Next.js frontend
│   ├── app/            # Routes
│   ├── components/     # UI
│   ├── features/       # Screen modules
│   ├── services/       # Mock data (prototype) → replace with API calls
│   ├── stores/         # Zustand client state
│   └── types/          # Shared domain + protocol types
├── backend/            # FastAPI (skeleton today)
│   ├── app/            # Factory, config, logging
│   ├── api/            # REST routers
│   ├── websocket/      # WS router + handlers
│   ├── room/           # Room manager
│   ├── game/           # Round engine + timers
│   ├── drawing/        # Document validation
│   ├── gallery/        # Publish + votes
│   ├── matches/        # Match persistence
│   ├── auth/           # Google OAuth + JWT
│   └── db/             # SQLAlchemy models
├── docs/               # This folder — source of truth
└── docker-compose.yml
```

---

## REST API (target)

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Health check |
| `GET` | `/gallery` | List published drawings |
| `POST` | `/auth/google` | Google sign-in |
| `GET` | `/auth/me` | Current user + stats |

---

## WebSocket

**Endpoint:** `ws://host/ws/{roomCode}`

Single connection per client. All real-time game traffic uses the protocol in [events.md](events.md).

### Connection manager

Tracks connections by connection id, room, and player. Supports:

* Room-wide broadcast
* Drawer-only delivery
* Single-player delivery

### Heartbeat

Client sends `connection.ping`; server responds with `connection.pong`. Used for reconnect detection and stale connection cleanup.

---

## Backend modules (implementation order)

1. FastAPI skeleton + health + config
2. WebSocket router + connection manager
3. Room manager (join, leave, ready, capacity)
4. Lobby (`player.ready`, `game.start`)
5. Round engine (word select, timer, guesses, scoring)
6. Drawing document engine (preview, commit, undo)
7. Chat + guess routing
8. Disconnect / reconnect grace timers
9. Gallery publish + voting
10. Postgres persistence (gallery, matches, stats)
11. Google OAuth

---

## Frontend integration path

Today the frontend uses mocked services in `svigl/services/` that return `Promise.resolve(...)`.

When implementing each backend feature:

1. Build the server module per this architecture.
2. Replace the matching function in `svigl/services/` with a real `fetch()` or WebSocket handler.
3. Keep types in `svigl/types/` aligned with [domain_model.md](domain_model.md) and [events.md](events.md).

---

## Related docs

| Doc | Topic |
|-----|-------|
| [events.md](events.md) | WebSocket protocol |
| [state_machine.md](state_machine.md) | Room, game, player FSMs |
| [domain_model.md](domain_model.md) | Core entities |
| [drawing_model.md](drawing_model.md) | SVG document model |
| [database.md](database.md) | Postgres schema |
