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

## Phase 1 - FastAPI Backend

**Goal:** A running HTTP server that returns real Garmin data, with a SQLite cache layer.

### Steps

1. Init Python project with `uv`
   - `uv init garmin-backend`
   - Add deps: `fastapi`, `uvicorn`, `garminconnect`, `python-dotenv`

2. Garmin authentication
   - First run: prompt for Garmin credentials, store OAuth tokens to a local file
   - Subsequent runs: load tokens from file, refresh if expired
   - Learn: how python-garminconnect handles OAuth token persistence

3. SQLite cache layer
   - Single table: `cache(endpoint TEXT PRIMARY KEY, data TEXT, fetched_at INTEGER)`
   - On each API call: check cache first; return cached data if age < TTL (3600s)
   - On miss: fetch from Garmin, write to cache, return data
   - Learn: Python's built-in `sqlite3` module; no ORM needed here

4. Define API endpoints
   ```
   GET  /summary          - today's steps, calories, stress, body battery
   GET  /sleep-data       - last night's sleep score, stages, HRV
   GET  /heart-rate       - resting HR, daily HR graph data
   GET  /hrv              - HRV status and 5-day trend (Fenix 7 compatible)
   GET  /activities       - recent activities (last 7 days)
   GET  /training-status  - training load, training readiness
   POST /cache/clear      - bust the cache manually (dev utility)
   ```

5. Run and test with curl / browser

**Verify:** `curl http://localhost:8000/summary` returns real data. Second call returns same data instantly (from cache). `curl -X POST http://localhost:8000/cache/clear` resets it.

---

## Phase 2 - Browser Dashboard UI

**Goal:** A functional, readable dashboard with charts -- running in a plain browser tab.

FastAPI serves the frontend as static files (`StaticFiles` mount). Open `http://localhost:8000` in a browser.

### Steps

1. Mount static files in FastAPI
   - `app.mount("/", StaticFiles(directory="frontend", html=True))`
   - **Must be added last in `main.py`**, after all API routes -- the mount is greedy and will intercept API calls if placed first
   - Learn: how FastAPI serves static content alongside API routes

2. Layout (`index.html`)
   - CSS grid: top row = key stats cards (steps, sleep score, body battery, resting HR)
   - Middle row = charts (HR over day, sleep stages, HRV trend)
   - Bottom row = recent activities list
   - Bundle Chart.js locally (`frontend/chart.umd.min.js`) -- no CDN

3. Stats cards
   - Fetch `/summary`, `/sleep-data`, `/hrv`
   - Render as simple number + label cards

4. Charts (Chart.js)
   - Heart rate over the day (line chart) - from `/heart-rate`
   - Sleep stages (bar/timeline chart) - from `/sleep-data`
   - HRV trend (line chart, 5 days) - from `/hrv`
   - Learn: Chart.js basics -- datasets, scales, tooltips

5. Activities list
   - Fetch `/activities`
   - Render as a simple table: date, type, duration, distance

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
| 2 | StaticFiles in FastAPI, DOM manipulation from fetch data, Chart.js, CSS grid |
| 3 | Electron architecture (main/renderer split), child process management, IPC security model |
| 4 | Electron packaging, bundling a Python backend |

---

## Out of Scope (for now)

- Historical data beyond what the Garmin API returns directly
- Local database / GarminDB
- AI coaching suggestions
- Multi-user support
- Auto-start on login
