# backend

FastAPI server that fetches Garmin health data and caches it locally in SQLite.

## Setup

1. Run:
   ```
   uv run uvicorn app.main:app --reload --port 8000
   ```

2. Log in once via Swagger UI at `http://localhost:8000/docs`: `POST /api/auth/login`
   (then `POST /api/auth/mfa` if prompted). The account is remembered via its Garmin
   token and auto-selected on the next start; passwords are never stored.

3. Test:
   ```
   uv run pytest
   ```

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/auth/status` | Active account email, or null |
| `GET /api/auth/accounts` | Remembered accounts |
| `POST /api/auth/login` | Credential login (`needs_mfa` means MFA must follow) |
| `POST /api/auth/mfa` | Complete a pending MFA login |
| `POST /api/auth/select` | Activate a remembered account |
| `POST /api/auth/logout` | Log out (`forget: true` also deletes the remembered account) |
| `GET /api/summary` | Steps, calories, stress, body battery |
| `GET /api/sleep-data` | Sleep score and stages |
| `GET /api/heart-rate` | Resting HR and daily HR data |
| `GET /api/hrv` | HRV status |
| `GET /api/activities` | Last 7 days of activities |
| `GET /api/training-status` | Training load and readiness |
| `POST /api/cache/clear` | Drop volatile cache entries (`?scope=all` drops everything) |

All GET endpoints accept an optional `?date=YYYY-MM-DD` query parameter (default: today).
Cache TTL is 3600s; entries for days strictly older than yesterday never expire.
