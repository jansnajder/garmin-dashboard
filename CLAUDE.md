# CLAUDE.md

## Project

Personal Garmin health dashboard. Electron desktop app wrapping a FastAPI backend that fetches and caches Garmin data.

See `PLAN.md` for the MVP architecture and phase breakdown. The completed PoC (Phases 1-4) is documented
in `docs/PLAN-POC.md`.

## Structure

```
backend/
    app/            FastAPI package: main.py (assembly), core/ (cache, paths, deps), routers/
    tests/          pytest suite (uv run pytest)
frontend/           Legacy static HTML/CSS/JS from the PoC; becomes a React + Vite + TS app in Phase 8
main.js             Electron entry point
docs/               PoC plan archive, API report (Phase 7+)
```

## Dev

```bash
# Backend + frontend
cd backend
uv run uvicorn app.main:app --reload --port 8000
# Open http://localhost:8000

# Tests
uv run --directory backend pytest

# Run all linters manually (also run automatically on every file edit via hooks)
uv run --directory backend pre-commit run --all-files
```

## Key constraints

- Python env managed by `uv` -- do not use pip directly
- Frontend target stack (Phase 8+): React + Vite + TypeScript + ECharts; until then the legacy PoC
  frontend is plain HTML/CSS/JS with locally bundled Chart.js -- keep it working, don't extend it
- No CDN dependencies at runtime -- everything bundled/installed locally
- SQLite cache TTL is 3600s per endpoint; entries for days strictly older than yesterday are permanent
  (no TTL). `POST /api/cache/clear` drops volatile entries by default, `?scope=all` drops everything
- API routes live under `/api` (one router per domain in `app/routers/`); endpoints get the Garmin
  client via `Depends(get_garmin)` from `app/core/deps.py`
- Frontend served by `app.frontend("/", directory=...)` in `app/main.py` (FastAPI built-in, not `StaticFiles`)
- Hooks in `.claude/settings.json` run ruff on `.py` edits and Prettier on `.js`/`.css`/`.html` edits automatically

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

## Current phase

Phases 1-4 - PoC: backend, dashboard UI, Electron shell, installer (done, see `docs/PLAN-POC.md`)
Phase 5 - Backend restructure & test foundation (done)
Phase 6 - Authentication & account management (done)
Phase 7 - Garmin data inventory (next, see `PLAN.md`)
