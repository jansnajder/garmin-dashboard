"""
Background auto-capture: archives every finished day into the permanent cache,
so history accumulates even for days and endpoints nobody opened in the UI.

Runs as a long-lived asyncio task started from the FastAPI lifespan context.
The blocking Garmin/cache work is offloaded to worker threads via
asyncio.to_thread(), so cancellation lands on the awaits between requests.
"""

import asyncio
import logging
from collections.abc import Callable
from datetime import date, timedelta
from functools import partial
from typing import Any

from fastapi import HTTPException
from garminconnect import Garmin

from app.core import auth, deps

logger = logging.getLogger(__name__)

# today-2 is the newest day fetch() archives permanently; yesterday sits in the
# grace window for late-settling data and stays volatile, so capturing it would
# be wasted API calls.
START_OFFSET = 2
MAX_DAYS = 30
THROTTLE_S = 1.0
DAY_S = 24 * 3600
IDLE_RECHECK_S = 15 * 60

ENDPOINTS: list[tuple[str, Callable[[Garmin, str], Any]]] = [
    ("summary", lambda c, d: {"stats": c.get_stats(d), "body_battery": c.get_body_battery(d)}),
    ("sleep-data", lambda c, d: c.get_sleep_data(d)),
    ("heart-rate", lambda c, d: c.get_heart_rates(d)),
    ("hrv", lambda c, d: c.get_hrv_data(d)),
    ("stress", lambda c, d: c.get_all_day_stress(d)),
    ("steps", lambda c, d: c.get_steps_data(d)),
]


async def run_once() -> None:
    """
    Archive finished days, walking backwards from today-2.

    Stops at the first fully cached day (everything older was archived by an
    earlier run), at the MAX_DAYS bound, when no account is active, or on the
    first fetch error (the next run resumes where this one stopped).
    """
    for offset in range(START_OFFSET, START_OFFSET + MAX_DAYS):
        client = auth.manager.active()

        if client is None:
            return

        d = (date.today() - timedelta(days=offset)).isoformat()
        missing = [(name, fn) for name, fn in ENDPOINTS if not deps.cached(f"{name}:{d}")]

        if not missing:
            return

        for name, fn in missing:
            try:
                await asyncio.to_thread(deps.fetch, f"{name}:{d}", partial(fn, client, d), last_date=d)
            except HTTPException as e:
                logger.warning("auto-capture ended at %s %s: %s %s", d, name, e.status_code, e.detail)

                return

            await asyncio.sleep(THROTTLE_S)


async def run_forever() -> None:
    """
    Daily capture loop, cancelled by the lifespan shutdown.

    While no account is active, re-checks every IDLE_RECHECK_S so a login later
    in the day still gets captured that day.
    """
    while True:
        if auth.manager.active() is None:
            await asyncio.sleep(IDLE_RECHECK_S)

            continue

        await run_once()
        await asyncio.sleep(DAY_S)
