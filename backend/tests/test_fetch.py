from datetime import date, timedelta

import pytest
from fastapi import HTTPException
from garminconnect import (
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)

from app.core import deps


@pytest.fixture
def fetch_cache(cache, monkeypatch):
    """Swap the module-level cache for a temp one so deps.fetch() can be called directly."""
    monkeypatch.setattr(deps, "cache", cache)

    return cache


def test_miss_calls_fn_and_caches(fetch_cache):
    """A cold key calls fn exactly once; the second fetch is served from cache."""
    calls = []

    def fn():
        calls.append(1)

        return {"data": 42}

    first = deps.fetch("k", fn)
    second = deps.fetch("k", fn)

    assert first == second == {"data": 42}
    assert len(calls) == 1


def test_hit_skips_fn(fetch_cache):
    """A pre-seeded key never invokes fn."""
    fetch_cache.set("k", "cached")

    def fn():
        raise AssertionError("fn must not be called on a cache hit")

    assert deps.fetch("k", fn) == "cached"


def test_rate_limit_maps_to_429(fetch_cache):
    """Garmin rate limiting surfaces as HTTP 429."""

    def fn():
        raise GarminConnectTooManyRequestsError("slow down")

    with pytest.raises(HTTPException) as exc:
        deps.fetch("k", fn)

    assert exc.value.status_code == 429


def test_auth_error_maps_to_401_and_resets_client(fetch_cache, monkeypatch):
    """Auth failure surfaces as HTTP 401 and drops the client singleton."""
    monkeypatch.setattr(deps, "_client", object())

    def fn():
        raise GarminConnectAuthenticationError("expired")

    with pytest.raises(HTTPException) as exc:
        deps.fetch("k", fn)

    assert exc.value.status_code == 401
    assert deps._client is None


def test_other_error_maps_to_503(fetch_cache):
    """Any unexpected error surfaces as HTTP 503."""

    def fn():
        raise RuntimeError("connection lost")

    with pytest.raises(HTTPException) as exc:
        deps.fetch("k", fn)

    assert exc.value.status_code == 503


@pytest.mark.parametrize(
    ("last_date", "permanent"),
    [
        ((date.today() - timedelta(days=2)).isoformat(), True),
        ((date.today() - timedelta(days=1)).isoformat(), False),
        (date.today().isoformat(), False),
        (None, False),
        ("garbage", False),
    ],
)
def test_permanence_from_last_date(fetch_cache, monkeypatch, last_date, permanent):
    """Only data strictly older than yesterday is cached permanently."""
    deps.fetch("k", lambda: "data", last_date=last_date)

    monkeypatch.setattr("app.core.cache.TTL", 0)

    assert fetch_cache.get("k") == ((True, "data") if permanent else (False, None))


def test_endpoint_wiring(client, fake_garmin):
    """/api/summary reaches the injected client with today's date and caches the composite."""
    today = date.today().isoformat()

    resp = client.get("/api/summary")

    assert resp.status_code == 200
    assert resp.json() == {
        "stats": {"method": "get_stats", "args": [today]},
        "body_battery": {"method": "get_body_battery", "args": [today]},
    }
    assert ("get_stats", (today,)) in fake_garmin.calls
    assert ("get_body_battery", (today,)) in fake_garmin.calls

    client.get("/api/summary")

    assert len(fake_garmin.calls) == 2


def test_activities_past_range_is_permanent(client, cache, monkeypatch):
    """A range ending before yesterday lands in the cache as a permanent row."""
    start = (date.today() - timedelta(days=5)).isoformat()
    end = (date.today() - timedelta(days=3)).isoformat()

    resp = client.get(f"/api/activities?start={start}&end={end}")

    assert resp.status_code == 200

    monkeypatch.setattr("app.core.cache.TTL", 0)
    found, _ = cache.get(f"activities:{start}:{end}")

    assert found


def test_clear_endpoint_scopes(client, cache):
    """The clear endpoint honors the volatile default, the all scope, and rejects garbage."""
    cache.set("v", "volatile")
    cache.set("p", "permanent", permanent=True)

    assert client.post("/api/cache/clear").status_code == 200
    assert cache.get("v") == (False, None)
    assert cache.get("p") == (True, "permanent")

    assert client.post("/api/cache/clear?scope=all").status_code == 200
    assert cache.get("p") == (False, None)

    assert client.post("/api/cache/clear?scope=bogus").status_code == 422
