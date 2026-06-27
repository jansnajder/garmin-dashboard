# CLAUDE.md

## Project

Personal Garmin health dashboard. Electron desktop app wrapping a FastAPI backend that fetches and caches Garmin data.

See `PLAN.md` for the full architecture and phase breakdown.

## Structure

```
garmin-backend/     Python project (uv) - FastAPI server + SQLite cache + Garmin client
frontend/           Static HTML/CSS/JS - served by FastAPI, no build step
main.js             Electron entry point (Phase 3+)
```

## Dev

```bash
# Backend
cd garmin-backend
uv run uvicorn main:app --reload --port 8000

# Frontend - just open http://localhost:8000 in a browser (Phase 1-2)
```

## Key constraints

- Python env managed by `uv` -- do not use pip directly
- No JS build tooling -- plain HTML/CSS/JS only, no npm bundler, no JSX
- Chart.js bundled locally in `frontend/` -- no CDN
- SQLite cache TTL is 3600s per endpoint; `GET /cache/clear` busts it

## Current phase

Phase 1 - FastAPI backend (not started)
