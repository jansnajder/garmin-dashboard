# garmin-dashboard

Personal dashboard to display Garmin measured metrics.

Electron desktop app wrapping a FastAPI backend that fetches data via
[python-garminconnect](https://github.com/cyberjunky/python-garminconnect) and caches it in SQLite.

## Development

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (manages the Python environment, Python 3.12 is installed automatically)
- Node.js + npm (Electron shell and packaging)

### Repository layout

```
backend/            Python project (uv) - FastAPI server, SQLite cache, Garmin client
    app/            the FastAPI package: main.py (assembly), core/, routers/
    tests/          pytest suite
frontend/           React + Vite + TypeScript app, served by the backend in production (builds to frontend/dist)
main.js             Electron entry point
PLAN.md             MVP roadmap and architecture
docs/               PoC plan archive
```

### Everyday commands

```bash
# Install dependencies (once) - root and frontend are separate npm packages,
# frontend is NOT an npm workspace, so both installs are required
npm install
cd frontend && npm install && cd ..

# Full dev loop: backend + Vite dev server + Electron (HMR), via concurrently
npm run dev

# Backend + frontend, no Electron: uvicorn + Vite dev server in separate terminals,
# then open http://localhost:5173 (Vite proxies /api to :8000)
cd backend && uv run uvicorn app.main:app --reload --port 8000
cd frontend && npm run dev

# Production-equivalent: build the frontend, then serve it from FastAPI alone
cd frontend && npm run build
cd backend && uv run uvicorn app.main:app --port 8000
# Open http://localhost:8000

# Backend tests
uv run --directory backend pytest

# All linters (ruff + prettier), same set the pre-commit hook runs
uv run --directory backend pre-commit run --all-files

# The full desktop app (spawns uvicorn itself - do not run it twice)
npm start
```

Backend credentials setup (`.env`, Garmin login) is described in [backend/README.md](backend/README.md),
along with the API endpoint list.

### Packaging

```bash
npm run freeze   # PyInstaller: backend + frontend -> backend/dist/backend/backend.exe
npm run pack     # freeze + unpacked Electron app (for inspection)
npm run dist     # freeze + NSIS one-exe installer -> release/
```

### Where things live at runtime

- SQLite cache: `%LOCALAPPDATA%\GarminDashboard\cache.db` (past days are cached permanently,
  today's data expires after 1 h)
- Garmin OAuth tokens: `~/.garminconnect`

See [PLAN.md](PLAN.md) for the roadmap; the finished PoC phases are archived in
[docs/PLAN-POC.md](docs/PLAN-POC.md).
