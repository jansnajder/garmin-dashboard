# Garmin Dashboard - MVP Plan

## Goal

Turn the validated PoC (see `docs/PLAN-POC.md`, Phases 1-4) into an MVP that replaces Garmin Connect for
personal use:

1. A complete inventory of what `python-garminconnect` returns for the real watches, documented in
   `docs/api-report.md`
2. Backend API endpoints built view-by-view on top of that inventory, each with a typed response
   shared with the frontend
3. Login screen with remembered accounts (token-based, no stored passwords)
4. Switchable dark/light theme
5. Refresh button that clears the cache and reloads all data
6. App shell: left menu, top-right refresh/theme controls, content area with graphs and widgets
   (detailed view specs will follow later)

Phase numbering continues from the PoC: Phases 1-4 are done, the MVP is Phases 5-10.

## Assumptions

Decisions taken while drafting this plan -- flag any you disagree with before the affected phase starts:

- **Inventory first, endpoints on demand** (decided 2026-07-04, supersedes "wrap all 90+ `get_*` methods
  as HTTP endpoints"). The full read surface of the library is probed and documented at the library level
  (Phase 7); HTTP endpoints are added only when a view needs them, each with a typed response model.
  Write operations (`add_weigh_in`, `set_blood_pressure`, workout upload, ...) stay out of MVP scope and
  are listed at the end as a candidate follow-up.
- **One active account at a time, many remembered.** The dashboard shows one user's data; the login screen
  lists remembered accounts and switching re-authenticates from the stored token.
- **Env-var credentials are removed.** `GARMIN_EMAIL`/`GARMIN_PASSWORD` and `.env` go away; the login screen
  is the only entry point. The existing `~/.garminconnect` token is imported on first run so no re-login is
  needed.
- **Frontend stack: React + Vite + TypeScript + ECharts** (decided 2026-07-03). The PoC's no-build-tooling
  constraint is dropped and Chart.js is replaced by Apache ECharts for rich interactivity (zoom/brush,
  gauges, heatmaps, linked charts). The vanilla PoC frontend lives on unchanged until Phase 8 rewrites it.
- **Past days are cached permanently** (decided 2026-07-04). Garmin data for finished days is (almost)
  immutable, so the TTL is the wrong invalidation model for it: the cache keeps such entries forever and
  applies the TTL only to today's/undated data. The cache thereby accumulates history passively, which is
  what makes future trend views possible despite Garmin's rate limits.
- **Remaining PoC constraints stay.** FastAPI serves the (built) frontend in production, SQLite cache,
  `uv` for Python, no CDN dependencies at runtime.

## Architecture

```
Electron (renderer)  <-->  FastAPI /api/*  <-->  AccountManager  <-->  python-garminconnect  <-->  Garmin
   React SPA                    |                    |
   (Vite + TS + ECharts,     SQLite            token store per account
   TanStack Query,        (TTL for today,      %LOCALAPPDATA%\GarminDashboard\accounts\<slug>\
   theme via CSS vars)     permanent for
                           past days, keys
                           scoped by account)
```

Changes vs the PoC:

- Backend grows from 4 flat modules into a package (`app/`) with one router per Garmin domain,
  everything under an `/api` prefix so API routes and static frontend files cannot collide; routers
  grow view-by-view instead of mirroring the whole library
- The `get_client()` singleton is replaced by an `AccountManager` that owns login, MFA, token
  persistence and the active client; endpoints receive the client via FastAPI dependency injection
- Cache keys gain an account prefix so switching accounts cannot serve another account's data
- The cache becomes a passive history store: entries for finished days never expire, only today's
  data lives under the TTL (see Phase 5)
- Endpoints consumed by views carry partial Pydantic response models (`extra="allow"`), so the OpenAPI
  schema describes real shapes and the frontend generates its TypeScript types from it instead of
  hand-writing them
- Frontend is rewritten as a React + TypeScript SPA built by Vite; in dev the Vite server proxies
  `/api` to FastAPI, in production FastAPI serves the static `frontend/dist` build (so the Electron
  and packaging story from the PoC is unchanged)

---

## Phase 5 - Backend Restructure & Test Foundation

**Goal:** A package layout ready for domain routers and an auth subsystem, a pytest harness, and the
cache retention policy that turns the cache into a passive history store. No visible change in the UI.

### Steps

1. Restructure `garmin-backend/` into a package:

   ```
   garmin-backend/
       app/
           __init__.py
           main.py            app assembly: create FastAPI app, include routers, mount frontend
           core/
               cache.py       moved, unchanged
               paths.py       moved; add accounts_dir() for Phase 6
               deps.py        fetch() helper + get_garmin() dependency
           routers/
               dashboard.py   the six existing PoC endpoints, now under /api
               cache.py       POST /api/cache/clear
       tests/
           conftest.py        TestClient + fake Garmin client fixture
           test_cache.py
           test_fetch.py
       run_server.py          updated import: from app.main import app
       garmin_backend.spec    updated for the package layout
   ```

2. Introduce dependency injection: endpoints declare `client: Garmin = Depends(get_garmin)` instead of
   calling the `get_client()` singleton inside lambdas. This is the standard FastAPI pattern and is what
   makes the test harness possible (`app.dependency_overrides[get_garmin] = fake`).
   Learn: FastAPI `Depends`, `dependency_overrides`.

3. Move all routes under `/api` (e.g. `/summary` -> `/api/summary`) and update `frontend/app.js`
   fetch calls accordingly.

4. Cache retention policy -- past days never expire:
   - The cache table gains a `permanent` flag; `Cache.get()` skips the TTL check for permanent rows
   - `fetch()` decides permanence from the request's date(s): strictly older than yesterday -> permanent
     (the one-day grace window covers data that settles late, e.g. sleep finalizing in the morning or a
     watch synced the next day); today, yesterday, undated, or open-ended ranges stay TTL-governed
   - `POST /api/cache/clear` gains a scope: `volatile` (default -- drops only TTL-governed rows, this is
     what the refresh button will call) and `all` (the escape hatch for when late-synced history landed
     wrong and a permanent row is stale)

5. Add `pytest` (dev dependency group in `pyproject.toml`, run via `uv run pytest`):
   - `test_cache.py` -- TTL expiry, clear, cross-key isolation; permanent rows survive TTL expiry and
     `clear(scope="volatile")`, and are gone after `clear(scope="all")`
   - `test_fetch.py` -- cache-or-call behavior, exception -> HTTP status mapping (429/401/503),
     permanence decision from request dates; per-key locking is not re-tested (PoC-proven), just
     not broken

6. Smoke-check packaging still works: `npm run freeze` produces a runnable
   `garmin-backend/dist/garmin-backend/garmin-backend.exe`.

**Verify:** `uv run pytest` green; dashboard at `http://localhost:8000` looks and behaves exactly as before;
requesting a past date twice across a TTL boundary hits the cache the second time; frozen exe starts and
serves `/api/summary`.

---

## Phase 6 - Authentication & Account Management

**Goal:** Login/logout/MFA endpoints; accounts remembered via persisted Garmin tokens; no credentials on
disk or in env vars.

### Backend design

`app/core/auth.py` -- `AccountManager`:

- Storage under `%LOCALAPPDATA%\GarminDashboard\`:
  - `accounts.json` -- `[{ "slug", "email", "display_name", "last_used" }]`
  - `accounts/<slug>/tokens/` -- garth OAuth token files for that account (dumped after successful login,
    loaded on account selection). Passwords are never written anywhere.
- API (all state guarded by one lock; a desktop app has no concurrency to speak of):
  - `list_accounts()` -- remembered accounts from `accounts.json`
  - `start_login(email, password)` -- `Garmin(email, password, return_on_mfa=True).login()`;
    returns `"ok"` or `"needs_mfa"`. The MFA session lives on the `Garmin` instance itself (verified in
    0.3.6: the `client_state` arg of `resume_login` is ignored), so on `needs_mfa` the manager keeps the
    pending instance in memory
  - `submit_mfa(code)` -- `pending.resume_login({}, code)` on that same instance, then the same
    post-login path as `start_login`
  - post-login: `get_full_name()` for display name, persist tokens via `client.dump(account_dir)`,
    update `accounts.json`, set active client
  - `select(slug)` -- load tokens via `Garmin().login(tokenstore)`; verify with a cheap call;
    on failure report that a fresh login is needed
  - `logout(forget: bool)` -- drop active client; when `forget`, also delete the token dir and the
    `accounts.json` entry
  - `active()` -- the active `Garmin` client or `None`; this backs `get_garmin()`, which raises
    `HTTPException(401)` when no account is active
- On startup, auto-`select()` the `last_used` account when its token still works -- "remember logged
  users" means the app opens straight into the dashboard; the login screen appears only when there is
  no usable account
- First-run migration: if `~/.garminconnect` holds a valid token and `accounts.json` does not exist,
  import it as the first remembered account.

`app/routers/auth.py`:

```
GET  /api/auth/status     -> { "active": "<email>" | null }
GET  /api/auth/accounts   -> [ { "slug", "email", "display_name", "last_used" } ]
POST /api/auth/login      { email, password } -> { "status": "ok" | "needs_mfa" }
POST /api/auth/mfa        { code }            -> { "status": "ok" }
POST /api/auth/select     { slug }            -> { "status": "ok" | "needs_login" }
POST /api/auth/logout     { forget: bool }    -> { "status": "ok" }
```

- Credentials travel browser -> localhost over loopback HTTP only; acceptable for a local personal app.
- `fetch()` cache keys get the active account slug as prefix: `"<slug>:summary:2026-07-03"`.
- On `GarminConnectAuthenticationError` mid-session the manager drops the active client so the frontend
  lands back on the login screen.

### Frontend

None in this phase -- the login UI is built in Phase 8 as part of the React rewrite (no point building a
throwaway vanilla version). The auth endpoints are exercised through Swagger UI at `/docs`, and the
startup auto-select keeps the legacy PoC frontend fully functional in the meantime.

### Tests

Fake `Garmin` construction in `AccountManager` (constructor injection of a factory) -- cover: clean login,
MFA path, remembered-account selection, token-expired selection, logout with and without forget,
cache-key prefixing.

**Verify:** fresh machine simulation (rename `%LOCALAPPDATA%\GarminDashboard`, hide `~/.garminconnect`):
data endpoints return 401, login + MFA via `/docs` works against the real account, server restart
auto-selects the remembered account, logout+forget wipes tokens and returns to the 401 state.

---

## Phase 7 - Garmin Data Inventory

**Goal:** Know what every `get_*` method of `garminconnect.Garmin` (0.3.6: 96 methods) actually returns
for the real watches, without wrapping anything in HTTP. The report is the input for deciding what the
dashboard shows and which endpoints get built.

### Steps

1. `garmin-backend/tools/probe.py` -- talks to the library directly, FastAPI not involved:
   - Client authenticated from the Phase 6 token store (fallback: `~/.garminconnect`)
   - Discover methods by introspection (`get_*` on `Garmin`); resolve arguments from each signature:
     date-like params get today/yesterday, ranges the last 7 days, id-like params resolved from parent
     calls (latest activity id from `get_activities`, device id from `get_devices`, gear uuid from
     `get_gear`); methods whose required args cannot be resolved are recorded as skipped, with the reason
   - Throttle ~1 request/s (Garmin rate limits are real) and dump each raw response as JSON into
     `tools/snapshots/` -- gitignored, it contains personal health data -- so the report can be
     regenerated offline without re-hitting Garmin

2. Generate `docs/api-report.md` from the snapshots: one section per domain (see the router map in
   Phase 9); per method the status (data / empty / 404 not supported by this watch / error / skipped),
   a shape sketch (top-level keys with value types) and truncated sample values

3. Read the report and pick what the dashboard should show -- it feeds directly into the Phase 9
   view specs

**Verify:** `docs/api-report.md` committed with a status for all 96 methods; regenerating the report
works offline from the snapshots.

---

## Phase 8 - Frontend Rewrite: React + Vite Scaffold, Shell, Theming, Refresh

**Goal:** Replace the vanilla PoC frontend with a React + TypeScript app implementing the MVP shell:
login screen, left menu, top-right refresh/theme controls, and the PoC dashboard ported to ECharts as
the first view.

### Stack decisions

- **Vite (`react-ts` template)** -- dev server with HMR, TypeScript, production build to `frontend/dist`.
  TypeScript replaces the `@ts-check` + JSDoc convention for frontend code (`main.js` for Electron stays
  plain JS with `@ts-check`).
- **React Router** for views -- one route per menu entry.
- **TanStack Query** for all server data -- every widget's fetch is a query with the endpoint as its key.
  This makes the refresh button trivial (see step 6) and centralizes 401 handling (a global query error
  handler routes to the login screen).
- **ECharts via npm** with a small handwritten wrapper (`useECharts` hook + `<Chart option={...} />`):
  the popular `echarts-for-react` wrapper is poorly maintained, and writing the hook teaches the
  init/resize/dispose lifecycle. Learn: `useRef` + `useEffect` around an imperative library.
- **Two `package.json` files** -- `frontend/package.json` (React, Vite, ECharts, dev server) and the
  existing root one (Electron, electron-builder). No npm workspaces; two independent installs are
  simpler to reason about.

### Steps

1. Scaffold: delete the vanilla `frontend/` (it stays in git history) and recreate it with
   `npm create vite@latest frontend -- --template react-ts`. Configure `server.proxy` so `/api/*`
   forwards to `http://localhost:8000` in dev; `vite build` outputs `frontend/dist/`.

2. Wire serving and dev workflow:
   - `paths.py` `frontend_dir()` now points to `frontend/dist` (dev and frozen alike); FastAPI serves
     only the built app -- live frontend dev happens on the Vite server at `http://localhost:5173`
   - `main.js`: in dev load the Vite URL, packaged load `http://localhost:8000` as today
   - Root `npm run dev` starts uvicorn + Vite + Electron together (`concurrently`); plain-browser dev
     stays possible with uvicorn + `npm run dev` inside `frontend/`

3. App shell layout (components `Layout`, `Sidebar`, `Topbar`):

   ```
   +--------------------------------------------------+
   | logo/user        [refresh] [theme]  <- topbar    |
   +----------+---------------------------------------+
   |  menu    |                                       |
   |  Today   |     view content                      |
   |  Sleep   |     (graphs / widgets)                |
   |  ...     |                                       |
   +----------+---------------------------------------+
   ```

   CSS grid: `grid-template-areas: "topbar topbar" "nav content"`. Menu entries come from the route
   config; active item highlighted via `NavLink`.

4. Theme system:
   - Colors as CSS custom properties under `:root[data-theme='dark']` / `[data-theme='light']`
     (the PoC dark palette becomes the dark theme)
   - `ThemeContext` + toggle button: swaps `data-theme` on `<html>`, persists to `localStorage`,
     initial value from `prefers-color-scheme`
   - Register a light and a dark ECharts theme built from the same palette; charts re-init on theme
     change (ECharts themes are fixed at init time)

5. Auth UI: full-window login route, guarded app routes (`/api/auth/status` decides). Remembered-accounts
   list (click = select), email/password form, MFA code step shown only on `needs_mfa`; logout (and
   logout+forget) in the topbar user menu.

6. Refresh button: `POST /api/cache/clear` with scope `volatile` (permanent history rows stay), then
   `queryClient.invalidateQueries()` -- every mounted widget refetches; button shows a spinner via
   `useIsFetching`.

7. Port the Today view to ECharts at feature parity: intraday HR line with a `dataZoom` slider,
   sleep-stage stacked bar, HRV trend line, stat cards; body battery becomes a gauge. It keeps using
   the untyped PoC composite endpoints for now; typing arrives with the Phase 9 Today slice.

8. Tooling: keep Prettier (extend the `.claude/settings.json` hook to `.ts`/`.tsx`), adopt the ESLint
   setup the Vite template ships; update `CLAUDE.md` code-style section for TypeScript.

**Verify:** `npm run dev` opens Electron with HMR; login screen -> MFA -> dashboard on a token-less
machine; theme toggles, restyles charts, and survives restart; refresh visibly refetches everything;
`vite build` + uvicorn alone serves the identical app at `http://localhost:8000`.

---

## Phase 9 - Dashboard Views & View-Driven API

**Goal:** Fill the shell with the actual Garmin Connect replacement views, growing the backend API
view-by-view.

**Blocked on:** detailed frontend specs (to be provided) and the Phase 7 inventory report (what the
watches really deliver).

### The per-view workflow

Each view lands as one vertical slice, backend to chart:

1. Pick the library methods the view needs, using the inventory report
2. Add the endpoints to the matching domain router (map below), each a one-liner through `fetch()`.
   Conventions: `?date=` defaulting to today, ranges `?start=&end=`, entity ids as path params
   (`/api/activities/{activity_id}/splits`), cache key `<account>:<router>:<endpoint>:<params>`,
   TTL stays the global 3600 s (past-day permanence is decided centrally by `fetch()`, not per endpoint)
3. Give each endpoint a partial Pydantic response model: declare only the fields the view consumes,
   with `model_config = ConfigDict(extra="allow")` so undeclared fields pass through untouched.
   Garmin schema drift then fails loudly as a validation error instead of a blank widget, and the
   OpenAPI schema carries real shapes. Learn: Pydantic v2 models, FastAPI `response_model`.
4. Regenerate the frontend types: `openapi-typescript` reads `http://localhost:8000/openapi.json` and
   writes `frontend/src/api/types.ts` (npm script `generate:api`). The backend OpenAPI schema is the
   single source of truth for the contract; no hand-written response interfaces.
5. Wiring test per endpoint (fake client: right `Garmin` method, right args, response passthrough,
   model validates the recorded snapshot from Phase 7), then build the view with TanStack Query
   and ECharts

### Error mapping refinement (part of the first slice)

`fetch()` currently folds every non-auth error into 503. Garmin returns real 404s for features a watch
does not support; map upstream HTTP errors (garth raises them with a response status) to the same
status code so the frontend can tell "not supported" from "backend broken".

### Domain router map

When a view needs a method, its endpoint goes into:

| Router | Methods |
|---|---|
| `wellness.py` | get_stats, get_user_summary, get_stats_and_body, get_body_battery, get_body_battery_events, get_all_day_stress, get_stress_data, get_heart_rates, get_rhr_day, get_respiration_data, get_spo2_data, get_hydration_data, get_floors, get_intensity_minutes_data, get_daily_steps, get_steps_data, get_weekly_steps, get_weekly_stress, get_weekly_intensity_minutes, get_all_day_events, get_lifestyle_logging_data |
| `sleep.py` | get_sleep_data, get_hrv_data |
| `body.py` | get_body_composition, get_weigh_ins, get_daily_weigh_ins, get_blood_pressure, get_fitnessage_data |
| `activities.py` | get_activities, get_activities_by_date, get_activities_fordate, get_last_activity, get_activity, get_activity_details, get_activity_splits, get_activity_typed_splits, get_activity_split_summaries, get_activity_exercise_sets, get_activity_gear, get_activity_hr_in_timezones, get_activity_power_in_timezones, get_activity_weather, get_activity_types, get_progress_summary_between_dates |
| `training.py` | get_training_status, get_training_readiness, get_morning_training_readiness, get_max_metrics, get_endurance_score, get_hill_score, get_race_predictions, get_lactate_threshold, get_cycling_ftp, get_running_tolerance, get_training_plans, get_training_plan_by_id, get_adaptive_training_plan_by_id, get_workouts, get_workout_by_id, get_scheduled_workouts, get_scheduled_workout_by_id, get_personal_record, get_goals |
| `devices.py` | get_devices, get_device_last_used, get_device_settings, get_device_alarms, get_device_solar_data, get_primary_training_device, get_unit_system |
| `gear.py` | get_gear, get_gear_defaults, get_gear_stats, get_gear_activities |
| `profile.py` | get_full_name, get_user_profile, get_userprofile_settings |
| `badges.py` | get_earned_badges, get_available_badges, get_in_progress_badges, get_badge_challenges, get_available_badge_challenges, get_non_completed_badge_challenges, get_adhoc_challenges, get_inprogress_virtual_challenges |
| `nutrition.py` | get_nutrition_daily_food_log, get_nutrition_daily_meals, get_nutrition_daily_settings |
| `golf.py` | get_golf_summary, get_golf_scorecard, get_golf_shot_data |
| `womens_health.py` | get_menstrual_data_for_date, get_menstrual_calendar_data, get_pregnancy_summary |

The PoC composite endpoints (`/api/summary`, `/api/training-status`) stay in `dashboard.py` untyped
until the Today view slice retypes or replaces them.

### Expected views

One route/view each: Today (ported in Phase 8), Sleep, HRV & Training, Activities (list + detail),
Body & Weight, Devices. Each view fetches only its own endpoints via TanStack Query; widgets shared
across views (stat card, time-series chart) get extracted into shared components only when the second
user of them appears, not before.

This phase will be broken into per-view sub-phases once the specs exist.

---

## Phase 10 - Packaging & Release

**Goal:** The MVP ships as the same one-exe NSIS installer the PoC produced.

### Steps

1. Build pipeline becomes three stages: `vite build` (frontend) -> PyInstaller freeze (bundles
   `frontend/dist` as `datas` instead of the raw `frontend/`) -> `electron-builder`; update the root
   `package.json` scripts and `garmin_backend.spec` accordingly (the `app/` package, `tools/` excluded)
2. Re-verify the frozen backend end-to-end: login flow (token dirs under `%LOCALAPPDATA%` must work
   frozen -- `paths.py` already targets it), all routers, cache
3. `npm run dist`; install on a machine without Python/Node/tokens: login screen -> MFA -> dashboard
4. Bump version in `package.json` and `pyproject.toml`

**Verify:** clean-machine install reaches a fully working themed dashboard through the login screen alone.

---

## Phase Dependencies

```
5 -> 6 -> 7 ---+
       \       +--> 9 -> 10
        +> 8 --+
```

After Phase 6, the data inventory (7) and the React rewrite (8) are independent tracks; Phase 9 needs
both (the shell to render into, the report to know what to render).

## Backlog

Accepted features outside the phase sequence, ordered by priority. Pull one in when its slot opens.

### Auto-capture (priority: high) -- slot: with Phase 6 or immediately after it

A background job that archives every finished day into the permanent cache, so history accumulates
even for days and endpoints nobody opened in the UI. Turns future trend views into instant local
reads and makes the archive survive a Garmin API break or account loss.

- `app/core/capture.py`, started from the FastAPI `lifespan` context as a long-lived asyncio task;
  runs on startup and then once per day, only while an account is active.
  Learn: `lifespan`, background tasks, graceful shutdown -- no planned phase covers these otherwise.
- Captures a fixed list of core daily endpoints (stats, sleep, heart rates, HRV, body battery,
  stress, steps) through the regular `fetch()` path, so account scoping and permanence apply unchanged
- Catch-up: walks backwards from yesterday until it hits a day already in the cache, bounded
  (e.g. max 30 days per run) and throttled ~1 request/s to respect rate limits
- Failure-tolerant by design: a 429 or network error just ends the run; the next run resumes where
  it stopped. No retry logic, no alerting.
- Tests: fake client + preseeded cache -- catch-up stops at the first known day, respects the bound,
  does nothing without an active account

### GPX course upload (priority: medium) -- slot: post-MVP, first write operation

"Drop a GPX on the app, it lands as a course in Garmin Connect" -- the watch then picks it up on its
normal sync. Collapses the mapy.com course-planning workflow to: plan on desktop, export GPX, drop it
on the dashboard.

- `python-garminconnect` has no course methods; the unofficial `course-service` endpoint is reached
  through the library's raw authenticated session (`client.post("connectapi", ...)`), same tokens as
  Phase 6. The official Courses API requires Garmin Developer Program approval -- not viable for a
  personal app.
- Step 1 is recon, no code: import a GPX course in Garmin Connect web with DevTools open and capture
  the request. If the web client parses the GPX in the browser and posts computed course JSON
  (points, distance, elevation), replicate that parsing with `gpxpy`.
- Backend: `POST /api/courses/import` accepting a GPX upload; frontend: drag-and-drop target in the
  shell.
- The mapy.com side stays manual by design: My Mapy has no public API, and desktop mapy.com already
  exports GPX directly.

### Embedded mapy.com course planning (priority: medium) -- slot: post-MVP, after GPX course upload

A "Course planning" sidebar entry hosting mapy.com in an Electron `WebContentsView`, closing the loop:
plan the course in-app, click Export -> GPX, the app catches the download and feeds it to
`POST /api/courses/import` -- the full plan-to-watch flow in one window.

- Embedding, not integration: the planner stays a website driven by hand; the app hosts it and
  catches the output. No Mapy REST API work.
- `WebContentsView` in the Electron main process (`main.js`), persistent session partition
  (`persist:mapy`) so the mapy.com login survives restarts
- GPX capture via `session.on('will-download')` -> hand the file to the course-upload endpoint
  instead of the Downloads folder
- MapyClimbs loaded via `session.extensions.loadExtension()` (content-script extensions are the
  category that tends to work). Spike first: load the unpacked extension, check the climb panel
  appears. The extension author is a friend and can adjust from their side if Electron needs it
  (e.g. dropping an unsupported `chrome.*` API or providing the analyzer as a plain injectable
  script), so this risk is low. Updates of the unpacked copy stay manual.
- Learning value: WebContentsView, session partitions, download interception, extension loading --
  Electron main-process features no other phase touches

### Personal day-journal (priority: low) -- slot: after the first Phase 9 trend views exist

Day-keyed personal annotations ("started new training block", "caught a cold") overlaid as markers
on the time-series charts -- the one feature Garmin Connect itself lacks, and what makes trends
interpretable in hindsight.

- Local-only user data, strictly separate from the cache: own SQLite file per account
  (`accounts/<slug>/journal.db`) so no cache-clear scope can ever touch it. It is the only
  irreplaceable data in the app (Garmin data can be re-fetched, journal entries cannot).
- CRUD under `/api/journal` with typed models (date, text, optional tags), wired into the
  `openapi-typescript` flow like any view endpoint
- UI: entry editor plus `markLine`/`markPoint` overlays on ECharts time axes; a marker on any chart
  links back to the entry

## Out of Scope (MVP)

- HTTP mirroring of the full library surface -- dropped 2026-07-04 in favor of view-driven endpoints;
  the Phase 7 inventory report covers discovery instead
- Write operations: add_weigh_in, set_blood_pressure, add/edit workouts, hydration logging,
  activity upload, `request_reload` -- natural first post-MVP milestone
- `query_garmin_graphql` passthrough
- Deep-history backfill (GarminDB-style, months/years before the app existed) -- distinct from the
  backlog's auto-capture, which only archives days going forward plus a bounded catch-up window
- Auto-update of the installed app
- AI coaching, multi-window, auto-start on login
