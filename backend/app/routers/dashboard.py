from datetime import date, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from garminconnect import Garmin

from app.core.deps import fetch, get_garmin, today

router = APIRouter(prefix="/api")


@router.get("/summary")
def summary(date_str: str = Query(default=None, alias="date"), client: Garmin = Depends(get_garmin)) -> Any:
    """
    Return today's steps, calories, stress and body battery.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :param client: injected authenticated Garmin client
    :return: dict with 'stats' and 'body_battery' keys
    """
    d = date_str or today()

    return fetch(f"summary:{d}", lambda: {
        "stats": client.get_stats(d),
        "body_battery": client.get_body_battery(d),
    }, last_date=d)


@router.get("/sleep-data")
def sleep_data(date_str: str = Query(default=None, alias="date"), client: Garmin = Depends(get_garmin)) -> Any:
    """
    Return sleep score and stage breakdown for the given date.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :param client: injected authenticated Garmin client
    :return: Garmin sleep data dict
    """
    d = date_str or today()

    return fetch(f"sleep-data:{d}", lambda: client.get_sleep_data(d), last_date=d)


@router.get("/heart-rate")
def heart_rate(date_str: str = Query(default=None, alias="date"), client: Garmin = Depends(get_garmin)) -> Any:
    """
    Return resting heart rate and intraday HR data for the given date.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :param client: injected authenticated Garmin client
    :return: Garmin heart rate data dict
    """
    d = date_str or today()

    return fetch(f"heart-rate:{d}", lambda: client.get_heart_rates(d), last_date=d)


@router.get("/hrv")
def hrv(date_str: str = Query(default=None, alias="date"), client: Garmin = Depends(get_garmin)) -> Any:
    """
    Return HRV status for the given date.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :param client: injected authenticated Garmin client
    :return: Garmin HRV data dict
    """
    d = date_str or today()

    return fetch(f"hrv:{d}", lambda: client.get_hrv_data(d), last_date=d)


@router.get("/activities")
def activities(
    start: str = Query(default=None),
    end: str = Query(default=None),
    client: Garmin = Depends(get_garmin),
) -> Any:
    """
    Return activities between start and end date (inclusive). Defaults to the last 7 days.

    :param start: ISO date string (YYYY-MM-DD), defaults to 7 days ago
    :param end: ISO date string (YYYY-MM-DD), defaults to today
    :param client: injected authenticated Garmin client
    :return: list of Garmin activity dicts
    :raises HTTPException: 400 if start is after end
    """
    _today = today()
    end = end or _today
    start = start or (date.fromisoformat(_today) - timedelta(days=7)).isoformat()

    if start > end:
        raise HTTPException(400, "start must not be after end")

    return fetch(f"activities:{start}:{end}", lambda: client.get_activities_by_date(start, end), last_date=end)


@router.get("/training-status")
def training_status(date_str: str = Query(default=None, alias="date"), client: Garmin = Depends(get_garmin)) -> Any:
    """
    Return training load status and readiness score for the given date.

    :param date_str: ISO date string (YYYY-MM-DD), defaults to today
    :param client: injected authenticated Garmin client
    :return: dict with 'status' and 'readiness' keys
    """
    d = date_str or today()

    return fetch(f"training-status:{d}", lambda: {
        "status": client.get_training_status(d),
        "readiness": client.get_training_readiness(d),
    }, last_date=d)
