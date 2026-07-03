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
# Backend + frontend
cd garmin-backend
uv run uvicorn main:app --reload --port 8000
# Open http://localhost:8000

# Run all linters manually (also run automatically on every file edit via hooks)
uv run --directory garmin-backend pre-commit run --all-files
```

## Key constraints

- Python env managed by `uv` -- do not use pip directly
- No JS build tooling -- plain HTML/CSS/JS only, no npm bundler, no JSX
- Chart.js and chartjs-adapter-date-fns bundled locally in `frontend/` -- no CDN
- SQLite cache TTL is 3600s per endpoint; `POST /cache/clear` busts it
- Frontend served by `app.frontend("/", directory="../frontend")` in `main.py` (FastAPI built-in, not `StaticFiles`)
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

Phase 1 - FastAPI backend (done)
Phase 2 - Browser Dashboard UI (done)
Phase 3 - Electron shell (done)
Phase 4 - Packaging: PyInstaller + electron-builder NSIS installer (done)
