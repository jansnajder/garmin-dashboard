# CLAUDE.md

## Project

Personal Garmin health dashboard. Electron desktop app wrapping a FastAPI backend that fetches and caches Garmin data.

See `PLAN.md` for the MVP architecture and phase breakdown. The completed PoC (Phases 1-4) is documented
in `docs/PLAN-POC.md`.

## Structure

```
backend/
    app/            FastAPI package: main.py (assembly), core/ (cache, paths, deps), routers/
    tools/          Phase 7 API inventory: probe.py (hits Garmin), report.py (offline docs/api-report.md
                    generator), resolve.py, router_map.py; tools/snapshots/ is gitignored (personal data)
    tests/          pytest suite (uv run pytest)
frontend/           React + Vite + TypeScript app (Phase 8); builds to frontend/dist, served by FastAPI
    src/
        api/            fetchJSON, queryClient (global 401 handler), auth mutations, query hooks, types
        auth/           AuthGate (top-level login-vs-shell check)
        charts/         useECharts hook, <Chart> wrapper, ECharts light/dark theme registration
        components/     Layout, Sidebar, Topbar (app shell)
        features/today/ Today view widgets (stat cards, HR/sleep/HRV charts, body battery gauge)
        hooks/          useRefresh (cache clear + invalidateQueries)
        pages/          LoginPage
        theme/          ThemeContext/ThemeProvider, useTheme, theme.css (light/dark CSS custom properties)
        routes.tsx      single source of truth for the sidebar nav and route table
main.js             Electron entry point
docs/               PoC plan archive, API inventory report (docs/api-report.md, Phase 7)
```

## Dev

```bash
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

# Tests
uv run --directory backend pytest

# Run all linters manually (also run automatically on every file edit via hooks)
uv run --directory backend pre-commit run --all-files
```

## Key constraints

- Python env managed by `uv` -- do not use pip directly
- Frontend stack: React + Vite + TypeScript + ECharts (Phase 8); the vanilla PoC frontend is gone
  (stays in git history)
- No CDN dependencies at runtime -- everything bundled/installed locally
- SQLite cache TTL is 3600s per endpoint; entries for days strictly older than yesterday are permanent
  (no TTL). `POST /api/cache/clear` drops volatile entries by default, `?scope=all` drops everything
- API routes live under `/api` (one router per domain in `app/routers/`); endpoints get the Garmin
  client via `Depends(get_garmin)` from `app/core/deps.py`
- Frontend served by `app.frontend("/", directory=frontend_dir(), check_dir=False)` in `app/main.py`
  (FastAPI built-in, not `StaticFiles`); `frontend_dir()` points at `frontend/dist` (the Vite build
  output), not the source tree. `check_dir=False` so the backend still starts before a first `vite build`
  has ever run (dev serves the frontend via the Vite dev server instead)
- Hooks in `.claude/settings.json` run ruff on `.py` edits and Prettier on `.js`/`.jsx`/`.ts`/`.tsx`/
  `.css`/`.html` edits automatically; `oxlint` (the frontend's linter, shipped by the Vite template)
  runs only at commit time via `pre-commit`, not on every edit

## Code style

### General

- Add empty line before every control statement, unless it is first line of deeper indent.
- Add empty line after every control statement.
- Do not be afraid to add empty line to ease up the readability.
- Every public method/function shall have a docstring.
- Private method/function with either complicated or crucial logic shall have a docstring.
- Every class shall have a docstring.

### Python
- Use type-hints, all functions/methods shall be type-annotated.
- Omit docstring for __init__, if there is anything notable, add it to the class docstring.
- Docstring format:

```python
"""
Brief explanation what the function does, side-effects and other important info.

:param arg_name: argument description
:param arg_name2: argument2 description
:return: return value/s description
:raises: in case the method/function raises any special exception
"""
```

### JavaScript

- `// @ts-check` at the top of every JS file -- enables TypeScript's checker without a compiler
- Use JSDoc for all public functions; format mirrors the Python docstring style:

```js
/**
 * Brief explanation.
 *
 * @param {string} arg - description
 * @returns {Promise<void>}
 * @throws {Error} when ...
 */
```

- Prettier handles formatting (single quotes, 120 char line width -- matches ruff)
- Browser globals from `<script>` tags (e.g. Chart.js) must be accessed via `(/** @type {any} */ (window)).Chart` to satisfy the type checker
- This convention applies only to plain-JS files outside `frontend/src/` (currently just `main.js`,
  the Electron entry point) -- see the TypeScript section below for `frontend/src/**`

### TypeScript

- `frontend/src/**/*.{ts,tsx}` uses real TypeScript types, not `@ts-check` + JSDoc -- that convention
  stays scoped to plain-JS files like `main.js`
- The `## General` rules above (blank lines around control statements, docstrings on public
  functions/classes) still apply
- Component-scoped styles use CSS Modules (`Component.module.css`, imported as `styles` and referenced
  via `styles.foo`), not global stylesheets per component; theme colors are still plain CSS custom
  properties (`frontend/src/theme/theme.css`) referenced with `var(--name)`
- Hand-written response types (`frontend/src/api/types.ts`) declare only the fields a view actually
  reads, all optional -- same "partial view into an untyped payload" philosophy as the backend's future
  `extra="allow"` Pydantic models (Phase 9); don't try to fully type raw Garmin shapes
- Prettier and `oxlint` (the linter the Vite template ships) handle formatting/linting; `oxlint` runs at
  commit time via `pre-commit`, not on every file edit

## Current phase

Phases 1-4 - PoC: backend, dashboard UI, Electron shell, installer (done, see `docs/PLAN-POC.md`)
Phase 5 - Backend restructure & test foundation (done)
Phase 6 - Authentication & account management (done)
Backlog: Auto-capture - background archival of finished days into the permanent cache (done)
Phase 7 - Garmin data inventory (done, see `docs/api-report.md`)
Phase 8 - Frontend rewrite: React + Vite scaffold, shell, theming, refresh (done)
Phase 9 - Dashboard views & view-driven API (next, see `PLAN.md`)
