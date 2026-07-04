import asyncio
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from garminconnect import GarminConnectTooManyRequestsError

from app.core import auth, capture, deps
from app.main import app

EMAIL = "john.doe@example.com"
SLUG = "john-doe-example-com"


def day(offset: int) -> str:
    """Return the ISO date `offset` days before today."""
    return (date.today() - timedelta(days=offset)).isoformat()


def seed_day(cache, offset: int, skip: str | None = None) -> None:
    """Preseed all capture keys for the day at `offset` as permanent rows, optionally skipping one endpoint."""
    for name, _ in capture.ENDPOINTS:
        if name != skip:
            cache.set(f"{SLUG}:{name}:{day(offset)}", "seeded", permanent=True)


def captured_days(fake_garmin) -> set[str]:
    """Return the set of dates the fake client was called with."""
    return {args[0] for _, args in fake_garmin.calls}


@pytest.fixture
def capture_env(cache, manager, monkeypatch):
    """Swap the module singletons for temp ones and zero the throttle so run_once() can be driven directly."""
    monkeypatch.setattr(deps, "cache", cache)
    monkeypatch.setattr(auth, "manager", manager)
    monkeypatch.setattr(capture, "THROTTLE_S", 0)

    return manager


def test_no_active_account_does_nothing(capture_env, factory, cache):
    """Without a login the run issues no Garmin calls and caches nothing."""
    asyncio.run(capture.run_once())

    assert factory.instances == []
    assert cache.get(f"{SLUG}:summary:{day(2)}") == (False, None)


def test_stops_at_first_fully_cached_day(capture_env, factory, cache):
    """The walk captures missing days and stops at the first day already fully in the cache."""
    seed_day(cache, 4)
    capture_env.start_login(EMAIL, "pw")

    asyncio.run(capture.run_once())

    fake = factory.instances[-1]

    for name, _ in capture.ENDPOINTS:
        assert cache.get(f"{SLUG}:{name}:{day(2)}")[0]
        assert cache.get(f"{SLUG}:{name}:{day(3)}")[0]

    assert captured_days(fake) == {day(2), day(3)}


def test_respects_max_days_bound(capture_env, factory, cache, monkeypatch):
    """With an empty cache the walk stops after MAX_DAYS days."""
    monkeypatch.setattr(capture, "MAX_DAYS", 3)
    capture_env.start_login(EMAIL, "pw")

    asyncio.run(capture.run_once())

    assert captured_days(factory.instances[-1]) == {day(2), day(3), day(4)}


def test_partially_cached_day_is_not_a_stop_day(capture_env, factory, cache, monkeypatch):
    """A day with some keys cached gets only the missing ones fetched and does not end the walk."""
    monkeypatch.setattr(capture, "MAX_DAYS", 2)
    seed_day(cache, 2, skip="hrv")
    capture_env.start_login(EMAIL, "pw")

    asyncio.run(capture.run_once())

    fake = factory.instances[-1]
    day2_calls = [name for name, args in fake.calls if args[0] == day(2)]

    assert day2_calls == ["get_hrv_data"]
    assert day(3) in captured_days(fake)


def test_fetch_error_ends_run(capture_env, factory, cache):
    """A rate-limited fetch ends the run quietly; earlier fetches of the same run stay cached."""
    capture_env.start_login(EMAIL, "pw")

    def boom(*args):
        raise GarminConnectTooManyRequestsError("429")

    factory.instances[-1].get_sleep_data = boom

    asyncio.run(capture.run_once())

    assert cache.get(f"{SLUG}:summary:{day(2)}")[0]
    assert cache.get(f"{SLUG}:heart-rate:{day(2)}") == (False, None)
    assert cache.get(f"{SLUG}:summary:{day(3)}") == (False, None)


def test_lifespan_starts_and_cancels_capture(capture_env, monkeypatch):
    """The lifespan starts the capture task on startup and cancels it cleanly on shutdown."""
    started = asyncio.Event()

    async def fake_run_forever():
        started.set()
        await asyncio.Event().wait()

    monkeypatch.setattr(capture, "run_forever", fake_run_forever)

    with TestClient(app):
        pass

    assert started.is_set()
