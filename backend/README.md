# backend

FastAPI server that fetches Garmin health data and caches it locally in SQLite.

## Setup

1. Copy `.env` and fill in your Garmin credentials:
   ```
   GARMIN_EMAIL=your@email.com
   GARMIN_PASSWORD=yourpassword
   ```

2. Run:
   ```
   uv run uvicorn app.main:app --reload --port 8000
   ```

3. Test:
   ```
   uv run pytest
   ```

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/summary` | Steps, calories, stress, body battery |
| `GET /api/sleep-data` | Sleep score and stages |
| `GET /api/heart-rate` | Resting HR and daily HR data |
| `GET /api/hrv` | HRV status |
| `GET /api/activities` | Last 7 days of activities |
| `GET /api/training-status` | Training load and readiness |
| `POST /api/cache/clear` | Drop volatile cache entries (`?scope=all` drops everything) |

All GET endpoints accept an optional `?date=YYYY-MM-DD` query parameter (default: today).
Cache TTL is 3600s; entries for days strictly older than yesterday never expire.
