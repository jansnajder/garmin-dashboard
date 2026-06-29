# garmin-backend

FastAPI server that fetches Garmin health data and caches it locally in SQLite.

## Setup

1. Copy `.env` and fill in your Garmin credentials:
   ```
   GARMIN_EMAIL=your@email.com
   GARMIN_PASSWORD=yourpassword
   ```

2. Run:
   ```
   uv run uvicorn main:app --reload --port 8000
   ```

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /summary` | Steps, calories, stress, body battery |
| `GET /sleep-data` | Sleep score and stages |
| `GET /heart-rate` | Resting HR and daily HR data |
| `GET /hrv` | HRV status |
| `GET /activities` | Last 7 days of activities |
| `GET /training-status` | Training load and readiness |
| `POST /cache/clear` | Bust the SQLite cache |

All endpoints accept an optional `?date=YYYY-MM-DD` query parameter (default: today).
Cache TTL is 3600s.
