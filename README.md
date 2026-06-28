# Svigl

> A multiplayer SVG-based drawing and guessing game — **frontend prototype**.

Svigl is a polished UI prototype for a real-time drawing game inspired by Skribbl.io. Every drawing is built from editable SVG primitives (paths, rectangles, circles) instead of raster strokes.

**The frontend is fully self-contained.** All screens use mocked data in `svigl/services/`. Nothing in the frontend calls a backend.

The `backend/` folder is a separate empty FastAPI skeleton for when you start building server features yourself.

---

## What's included

| Area | Status |
|------|--------|
| Landing, lobby, game, gallery, profile, settings | UI with mock data |
| SVG drawing editor (path, rectangle, circle, undo) | Client-side only |
| Mock auth (Mock User / Mock Guest) | In-memory, no OAuth |
| `backend/` | Optional skeleton — not wired to the frontend |

---

## Routes

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/room/demo` | Demo lobby (Create Room) |
| `/lobby` | Lobby with 8 dummy players |
| `/game` | Game screen with dummy timer, chat, scores |
| `/gallery` | Static gallery data |
| `/profile` | Mock profile stats |
| `/settings` | Preferences (saved locally) |

---

## Development

```bash
cd svigl
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). No `.env` file needed.

### Docker (frontend only)

```bash
docker compose up
```

### Backend skeleton (optional, separate)

Not connected to the frontend. See `backend/README.md`.

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Project structure

```text
svigl/
├── svigl/              # Next.js frontend prototype
│   ├── app/            # Routes
│   ├── components/     # UI, layout, auth
│   ├── features/       # Screen modules
│   ├── services/       # Mock data (Promise.resolve only)
│   └── stores/         # Zustand client state
├── backend/            # Unconnected FastAPI skeleton
├── docs/               # Architecture and domain specs
└── README.md
```

---

## Mock services

| File | Purpose |
|------|---------|
| `services/auth.ts` | Mock User / Mock Guest |
| `services/room.ts` | Lobby players |
| `services/game.ts` | Game state, chat, scores |
| `services/gallery.ts` | Static gallery entries |
| `services/profile.ts` | Profile stats |

---

## Design docs

Target specs for when you implement the backend (the frontend prototype does not use these yet):

- [architecture.md](docs/architecture.md) — system overview and module layout
- [state_machine.md](docs/state_machine.md) — room, game, and player states
- [events.md](docs/events.md) — WebSocket protocol
- [domain_model.md](docs/domain_model.md) — core entities
- [drawing_model.md](docs/drawing_model.md) — SVG document model
- [database.md](docs/database.md) — Postgres schema

---

## Tech stack

**Frontend:** Next.js, TypeScript, Tailwind CSS, Framer Motion, Zustand

**Backend (skeleton, optional):** FastAPI, Uvicorn
