# Garmin Dashboard - Project Plan

## Goal

A personal desktop application that fetches Garmin health/fitness data and displays it in a clean dashboard. Self-use only.

## Architecture

```
Browser / Electron (renderer)  <-->  FastAPI (server)  <-->  python-garminconnect  <-->  Garmin API
        HTML/CSS/JS                   localhost HTTP            Python library
                                           |
                                        SQLite
                                     (TTL cache)
```

- **FastAPI** is the core -- serves both the API and static frontend files
- **SQLite** caches Garmin responses per endpoint with a TTL (1 hour default); avoids redundant API calls and survives app restarts
- **Browser first** -- Phase 1-2 run in a plain browser tab, no Electron needed
- **Electron** is added in Phase 3 as a shell around the already-working app
- **python-garminconnect** handles Garmin auth and data fetching

---

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI + uvicorn | Learning goal; minimal, async |
| Cache | SQLite (stdlib) | Zero deps; TTL per endpoint; survives restarts |
| Garmin data | python-garminconnect | Thin wrapper, already familiar from garmin-mcp |
| Frontend | HTML/CSS/JS (static files served by FastAPI) | No build step; browser-first dev |
| Charts | Chart.js (bundled locally) | Simple; no CDN dependency |
| Desktop shell | Electron (Phase 3) | Learning goal; added after app is proven in browser |
| Python env | uv | Fast, modern |

---

## Phase 1 - FastAPI Backend ✓

**Goal:** A running HTTP server that returns real Garmin data, with a SQLite cache layer.

### What was built

- `garmin-backend/cache.py` -- `Cache` class: SQLite-backed TTL cache, single table `(key, data, fetched_at)`, `get`/`set`/`clear` methods
- `garmin-backend/garmin_client.py` -- `get_client()` singleton: lazy-init Garmin client, tokens persisted to `~/.garminconnect`
- `garmin-backend/main.py` -- FastAPI app with a `fetch(key, fn)` helper that abstracts the cache-or-call pattern, keeping each endpoint a one-liner

**Endpoints:**
```
GET  /summary          - steps, calories, stress; body_battery as sampled list
GET  /sleep-data       - sleep score, stage durations, HRV, SpO2
GET  /heart-rate       - resting HR + intraday time-series (raw Garmin dict)
GET  /hrv              - weekly avg, last night avg, status, nightly readings
GET  /activities       - last 7 days; date range via ?start=&end=
GET  /training-status  - training load + readiness score with factor breakdown
POST /cache/clear      - delete all cache entries
```

**Key implementation notes:**
- `sqlite3.connect(..., check_same_thread=False)` -- required because FastAPI may dispatch requests across threads
- Garmin client is a lazy singleton -- avoids auth overhead on every request, and defers the token load until the first actual call
- `fetch(key, fn)` maps garminconnect exceptions to HTTP status codes: 429 rate limit, 401 auth failure, 503 connection error
- Cache keys encode both endpoint and date (e.g. `summary:2026-06-28`) -- prevents stale cross-day hits on a long-running server
- Date query param is aliased as `?date=` in the URL but named `date_str` in Python to avoid shadowing the stdlib `date` type
- All endpoints return `Any` -- Garmin API responses are passed through untyped; no response models

**Tooling added:**
- `uv` for Python env, `ruff` for linting, `pre-commit` for hooks

**Verify:** `curl http://localhost:8000/summary` returns real data. Second call returns same data instantly (from cache). `curl -X POST http://localhost:8000/cache/clear` resets it.

---

## Phase 2 - Browser Dashboard UI ✓

**Goal:** A functional, readable dashboard with charts -- running in a plain browser tab.

FastAPI serves the frontend via `app.frontend("/", directory="../frontend")`. Open `http://localhost:8000` in a browser.

### What was built

- `frontend/index.html` -- semantic layout: 5 stat cards, 3 chart canvases, activities table
- `frontend/style.css` -- dark theme, CSS grid, shimmer skeleton loading state
- `frontend/app.js` -- parallel data fetching via `Promise.allSettled`; one render function per section
- `frontend/chart.umd.min.js` + `frontend/chartjs-adapter-date-fns.bundle.min.js` -- bundled locally

**Stat cards (top row):** Steps (with goal), Sleep Score, Body Battery, Resting HR, HRV + status

**Charts (middle row):**
- Heart rate over the day (line, time axis) -- from `/heart-rate`; intraday `[[timestamp_ms, bpm]]` series
- Sleep stages (horizontal stacked bar) -- from `/sleep-data`; deep/light/REM/awake in minutes
- HRV trend (line + 7-day avg reference line) -- from `/hrv`; nightly readings

**Activities table (bottom row):** date, name, duration, distance, avg HR, calories -- from `/activities`

**Tooling added:**
- `// @ts-check` + JSDoc in `app.js` -- type checking without a compiler
- Prettier wired into pre-commit (`.js`/`.css`/`.html`) and `.claude/settings.json` hooks
- `.prettierrc` -- single quotes, 120 char line width

**Key implementation notes:**
- `app.frontend()` (FastAPI built-in) is used instead of `app.mount(StaticFiles(...))` -- it checks API routes first automatically, so placement in `main.py` doesn't matter
- Chart.js `time` axis requires the date-fns adapter; bundled as a second local file
- `getEl(id)` helper asserts non-null on `getElementById` -- satisfies the type checker and catches HTML/JS mismatches early
- Body battery requires flattening `bodyBatteryStatList` arrays across multiple time-window objects and sorting by `endGMT`
- Heart rate intraday field name (`heartRateValues`) may vary by firmware -- first load logs the full response to console

**Verify:** Dashboard shows real data at `http://localhost:8000`. Charts render correctly. Data matches Garmin Connect.

---

## Phase 3 - Electron Shell

**Goal:** Wrap the already-working app in an Electron window.

### Steps

1. Init Electron project
   - `npm init` + install `electron`
   - Learn: main process vs renderer process, the IPC bridge between them

2. Main process (`main.js`)
   - Spawn FastAPI (`uvicorn`) as a child process on app start
   - Kill it on app close
   - Open a `BrowserWindow` loading `http://localhost:8000`

3. Dev workflow: `npm start` launches both Electron and FastAPI

4. Learn: Electron's `contextBridge` / `nodeIntegration` security model
   - Even though we're loading localhost (not a file), understand why `nodeIntegration: false` is the right default

**Verify:** `npm start` opens a window showing the same dashboard as the browser. FastAPI spawns and dies with the window.

---

## Phase 4 - Polish

**Goal:** App feels like a finished tool, not a dev prototype.

### Steps

1. First-run auth flow
   - If no token file exists, show a login screen (email + password fields)
   - On success, store tokens and proceed to dashboard

2. Loading states and errors
   - Show a spinner while data loads
   - Show an error message if Garmin API is unreachable

3. Refresh button
   - POSTs to `/cache/clear` then re-fetches all endpoints

4. Extend Garmin API coverage
   - Phase 1 exposes 6 endpoints, a small subset of python-garminconnect (130+ methods)
   - Wrap additional methods as cached HTTP endpoints on demand

5. Packaging (optional)
   - `electron-builder` to produce a `.exe` installer
   - Bundle Python + FastAPI into the package (via PyInstaller)

**Verify:** App works end-to-end from a cold start with no manual steps.

---

## Key Learning Outcomes

| Phase | What you learn |
|---|---|
| 1 | FastAPI routing, async endpoints, Python OAuth token handling, sqlite3 |
| 2 | `app.frontend()` in FastAPI, DOM manipulation from fetch data, Chart.js, CSS grid, JSDoc + ts-check |
| 3 | Electron architecture (main/renderer split), child process management, IPC security model |
| 4 | Electron packaging, bundling a Python backend |

---

## Out of Scope (for now)

- Historical data beyond what the Garmin API returns directly
- Local database / GarminDB
- AI coaching suggestions
- Multi-user support
- Auto-start on login
