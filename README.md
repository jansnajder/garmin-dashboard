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
frontend/           web frontend served by the backend (PoC vanilla JS, React rewrite planned)
main.js             Electron entry point
PLAN.md             MVP roadmap and architecture
docs/               PoC plan archive
```

### Everyday commands

```bash
# Install the Electron/packaging dependencies (once)
npm install

# Backend + frontend in the browser (http://localhost:8000, --reload picks up code changes)
cd backend
uv run uvicorn app.main:app --reload --port 8000

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
