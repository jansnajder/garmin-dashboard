from collections.abc import Callable
from datetime import date, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from garminconnect import (
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from cache import Cache
from garmin_client import get_client

app = FastAPI()
cache = Cache()


def today() -> str:
    """
    Return today's date as an ISO 8601 string (YYYY-MM-DD).

    :return: today's date string
    """
    return date.today().isoformat()


def fetch(key: str, fn: Callable[[], Any]) -> Any:
    """
    Return cached data for key, or call fn() to fetch it and populate the cache.

    :param key: cache key, should encode endpoint + date to avoid stale cross-day hits
    :param fn: callable that fetches fresh data from Garmin
    :return: data from cache or fresh fetch
    :raises HTTPException: 429 on rate limit, 401 on auth failure, 503 on connection or other error
    """
    found, hit = cache.get(key)

    if found:
        return hit

    try:
        data = fn()
    except GarminConnectTooManyRequestsError:
        raise HTTPException(429, "Garmin rate limit - wait a few minutes")
    except GarminConnectAuthenticationError:
        raise HTTPException(401, "Garmin auth failed")
    except GarminConnectConnectionError as e:
        raise HTTPException(503, str(e))
    except Exception as e:
        raise HTTPException(503, str(e))

    cache.set(key, data)

    return data


@app.get("/summary")
def summary(date_str: str = Query(default=None, alias="date")) -> Any:
    """
    Return today's steps, calories, stress and body battery.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :return: dict with 'stats' and 'body_battery' keys
    """
    d = date_str or today()

    return fetch(f"summary:{d}", lambda: {
        "stats": get_client().get_stats(d),
        "body_battery": get_client().get_body_battery(d),
    })


@app.get("/sleep-data")
def sleep_data(date_str: str = Query(default=None, alias="date")) -> Any:
    """
    Return sleep score and stage breakdown for the given date.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :return: Garmin sleep data dict
    """
    d = date_str or today()

    return fetch(f"sleep-data:{d}", lambda: get_client().get_sleep_data(d))


@app.get("/heart-rate")
def heart_rate(date_str: str = Query(default=None, alias="date")) -> Any:
    """
    Return resting heart rate and intraday HR data for the given date.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :return: Garmin heart rate data dict
    """
    d = date_str or today()

    return fetch(f"heart-rate:{d}", lambda: get_client().get_heart_rates(d))


@app.get("/hrv")
def hrv(date_str: str = Query(default=None, alias="date")) -> Any:
    """
    Return HRV status for the given date.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :return: Garmin HRV data dict
    """
    d = date_str or today()

    return fetch(f"hrv:{d}", lambda: get_client().get_hrv_data(d))


@app.get("/activities")
def activities(
    start: str = Query(default=None),
    end: str = Query(default=None),
) -> Any:
    """
    Return activities between start and end date (inclusive). Defaults to the last 7 days.

    :param start: ISO date string (YYYY-MM-DD), defaults to 7 days ago
    :param end: ISO date string (YYYY-MM-DD), defaults to today
    :return: list of Garmin activity dicts
    :raises HTTPException: 400 if start is after end
    """
    end = end or today()
    start = start or (date.today() - timedelta(days=7)).isoformat()

    if start > end:
        raise HTTPException(400, "start must not be after end")

    return fetch(f"activities:{start}:{end}", lambda: get_client().get_activities_by_date(start, end))


@app.get("/training-status")
def training_status(date_str: str = Query(default=None, alias="date")) -> Any:
    """
    Return training load status and readiness score for the given date.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :return: dict with 'status' and 'readiness' keys
    """
    d = date_str or today()

    return fetch(f"training-status:{d}", lambda: {
        "status": get_client().get_training_status(d),
        "readiness": get_client().get_training_readiness(d),
    })


@app.post("/cache/clear")
def clear_cache() -> dict[str, bool]:
    """
    Delete all SQLite cache entries.

    :return: confirmation dict
    """
    cache.clear()

    return {"cleared": True}
