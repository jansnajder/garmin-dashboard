import os
import threading
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import HTTPException
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)

from app.core.cache import Cache
from app.core.paths import cache_path

load_dotenv()

_client: Garmin | None = None
_lock = threading.Lock()
TOKEN_PATH = str(Path.home() / ".garminconnect")

cache = Cache(cache_path())

_key_locks: dict[str, threading.Lock] = {}
_key_locks_guard = threading.Lock()


def get_client() -> Garmin:
    """
    Return the shared Garmin client, initializing and logging in on first call.

    Tokens are persisted to TOKEN_PATH so subsequent runs skip full re-authentication.
    Credentials are read from the environment; when absent (e.g. a packaged build),
    login falls back to the persisted token at TOKEN_PATH.

    :return: authenticated Garmin client instance
    :raises GarminConnectAuthenticationError: if no valid token exists and no credentials are set
    """
    global _client

    with _lock:
        if _client is None:
            client = Garmin(
                email=os.environ.get("GARMIN_EMAIL"),
                password=os.environ.get("GARMIN_PASSWORD"),
            )
            client.login(TOKEN_PATH)
            _client = client

    return _client


def reset_client() -> None:
    """
    Force re-authentication on the next get_client() call.

    Call this after a GarminConnectAuthenticationError to recover without a process restart.
    """
    global _client

    with _lock:
        _client = None


def get_garmin() -> Garmin:
    """
    FastAPI dependency returning the shared authenticated Garmin client.

    Lazy login happens here, during dependency resolution, so a login failure
    must be mapped to 401 in this wrapper - it never reaches fetch()'s handlers.

    :return: authenticated Garmin client instance
    :raises HTTPException: 401 when Garmin authentication fails
    """
    try:
        return get_client()
    except GarminConnectAuthenticationError:
        reset_client()

        raise HTTPException(401, "Garmin auth failed")


def _key_lock(key: str) -> threading.Lock:
    """Return a per-key lock, creating it on first use."""
    with _key_locks_guard:
        if key not in _key_locks:
            _key_locks[key] = threading.Lock()

        return _key_locks[key]


def today() -> str:
    """
    Return today's date as an ISO 8601 string (YYYY-MM-DD).

    :return: today's date string
    """
    return date.today().isoformat()


def _is_permanent(last_date: str | None) -> bool:
    """
    Decide whether data covering last_date is finished and may be cached forever.

    Strictly older than yesterday counts as permanent; the one-day grace window
    covers data that settles late (sleep finalizing, next-day watch sync).
    Unparseable dates degrade to volatile - the date is a user-supplied query
    param that was never validated.

    :param last_date: latest ISO date the data covers, None for undated data
    :return: True when the entry should never expire
    """
    if last_date is None:
        return False

    try:
        parsed = date.fromisoformat(last_date)
    except ValueError:
        return False

    return parsed < date.today() - timedelta(days=1)


def fetch(key: str, fn: Callable[[], Any], *, last_date: str | None = None) -> Any:
    """
    Return cached data for key, or call fn() to fetch it and populate the cache.

    Uses per-key locking with double-checked caching to prevent concurrent cold-cache
    requests from issuing duplicate Garmin API calls. Data covering only days strictly
    older than yesterday is cached permanently; everything else falls under the TTL.

    :param key: cache key, should encode endpoint + date to avoid stale cross-day hits
    :param fn: callable that fetches fresh data from Garmin
    :param last_date: latest ISO date the data covers (end date for ranges), None for undated data
    :return: data from cache or fresh fetch
    :raises HTTPException: 429 on rate limit, 401 on auth failure, 503 on connection or other error
    """
    found, hit = cache.get(key)

    if found:
        return hit

    with _key_lock(key):
        found, hit = cache.get(key)

        if found:
            return hit

        try:
            data = fn()
        except GarminConnectTooManyRequestsError:
            raise HTTPException(429, "Garmin rate limit - wait a few minutes")
        except GarminConnectAuthenticationError:
            reset_client()
            raise HTTPException(401, "Garmin auth failed")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(503, str(e))

        cache.set(key, data, permanent=_is_permanent(last_date))

        return data
