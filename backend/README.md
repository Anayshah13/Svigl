# Svigl Backend (Skeleton)

This folder is **not connected to the frontend**. The Next.js app uses mocked services only and makes no HTTP or WebSocket calls.

Use this skeleton when you are ready to implement backend features yourself.

## What exists

- FastAPI project structure
- `GET /health` → `{ "status": "ok" }`
- Pytest smoke test

## Run locally

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Open [http://localhost:8000/health](http://localhost:8000/health).

## Adding features

1. Add routes under `api/`
2. Register them in `app/create_app.py`
3. When ready to connect the frontend, replace the matching function in `svigl/services/` with a real API call
