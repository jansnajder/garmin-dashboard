"""
Phase 7 inventory probe: calls every garminconnect.Garmin get_* method once and
dumps the raw JSON response to snapshots/, throttled to respect Garmin's rate limits.

Talks to the library directly - no FastAPI, no cache. Authenticates through the
existing Phase 6 AccountManager (remembered account or the legacy ~/.garminconnect
token), exactly like the app's own startup does.

Run with:
    uv run --directory backend python -m tools.probe

Then regenerate docs/api-report.md offline with:
    uv run --directory backend python -m tools.report
"""

import inspect
import json
import re
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from app.core.auth import manager
from tools import router_map
from tools.resolve import ProbeState, Record, Status, harvest, resolve_args

SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"
MANIFEST_PATH = SNAPSHOTS_DIR / "_manifest.json"

THROTTLE_SECONDS = 1.0
MAX_CONSECUTIVE_429 = 3

_STATUS_RE = re.compile(r"API Error (\d+)")

# Methods that populate ProbeState for others; everything else follows alphabetically.
PARENT_ORDER = [
    "get_user_profile",
    "get_userprofile_settings",
    "get_devices",
    "get_activities",
    "get_last_activity",
    "get_gear",
    "get_workouts",
    "get_training_plans",
    "get_golf_summary",
    "get_scheduled_workouts",
]


def call_order() -> list[str]:
    """
    Return every ROUTER_MAP method, id-source methods first so their ids are
    harvested before the methods that need them.

    :return: ordered method names
    """
    rest = sorted(set(router_map.ALL_METHODS) - set(PARENT_ORDER))

    return PARENT_ORDER + rest


def call_one(garmin: Garmin, method: str, kwargs: dict[str, Any]) -> tuple[Status, Any, str | None]:
    """
    Call one Garmin method with already-resolved kwargs and classify the outcome.

    GarminConnectAuthenticationError and GarminConnectTooManyRequestsError are not
    caught here - the caller decides whether to abort the whole run on those.

    :param garmin: authenticated Garmin client
    :param method: method name to call
    :param kwargs: resolved keyword arguments
    :return: (status, raw data or None, error message or None)
    :raises GarminConnectAuthenticationError: on auth failure
    :raises GarminConnectTooManyRequestsError: on rate limiting
    """
    try:
        data = getattr(garmin, method)(**kwargs)
    except (GarminConnectAuthenticationError, GarminConnectTooManyRequestsError):
        raise
    except GarminConnectConnectionError as e:
        match = _STATUS_RE.search(str(e))

        if match and match.group(1) == "404":
            return "404", None, str(e)

        return "error", None, str(e)
    except Exception as e:
        return "error", None, str(e)

    return ("empty" if not data else "data"), data, None


def write_manifest(records: list[Record]) -> None:
    """Persist the manifest after every call, so an interrupted run loses nothing already probed."""
    MANIFEST_PATH.write_text(
        json.dumps([asdict(r) for r in records], indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> None:
    """Authenticate, probe every method in order, and write snapshots + manifest incrementally."""
    manager.startup()
    garmin = manager.active()

    if garmin is None:
        print("No active Garmin account - log in first via /docs (POST /api/auth/login).", file=sys.stderr)
        sys.exit(1)

    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    state = ProbeState()
    records: list[Record] = []
    consecutive_429 = 0
    order = call_order()

    for i, method in enumerate(order, start=1):
        sig = inspect.signature(getattr(Garmin, method))
        resolution = resolve_args(method, sig, state)

        if resolution.kwargs is None:
            records.append(
                Record(method=method, router=router_map.ROUTER_MAP[method], status="skipped", error=resolution.reason)
            )
            write_manifest(records)
            print(f"[{i}/{len(order)}] {method}: skipped ({resolution.reason})")
            continue

        try:
            status, data, error = call_one(garmin, method, resolution.kwargs)
        except GarminConnectAuthenticationError as e:
            records.append(
                Record(
                    method=method,
                    router=router_map.ROUTER_MAP[method],
                    status="error",
                    args=resolution.kwargs,
                    error=str(e),
                )
            )
            write_manifest(records)
            print(f"Authentication failed on {method}, aborting run: {e}", file=sys.stderr)
            sys.exit(1)
        except GarminConnectTooManyRequestsError as e:
            consecutive_429 += 1
            records.append(
                Record(
                    method=method,
                    router=router_map.ROUTER_MAP[method],
                    status="error",
                    args=resolution.kwargs,
                    error=str(e),
                )
            )
            write_manifest(records)
            print(f"[{i}/{len(order)}] {method}: rate limited ({consecutive_429}/{MAX_CONSECUTIVE_429})")

            if consecutive_429 >= MAX_CONSECUTIVE_429:
                print("Rate limited too many times in a row - aborting, resume later.", file=sys.stderr)
                sys.exit(1)

            time.sleep(THROTTLE_SECONDS)
            continue

        consecutive_429 = 0
        snapshot_name = None

        if status == "data":
            harvest(method, data, state)
            snapshot_name = f"{method}.json"
            (SNAPSHOTS_DIR / snapshot_name).write_text(
                json.dumps(data, indent=2, default=str, ensure_ascii=False), encoding="utf-8"
            )

        records.append(
            Record(
                method=method,
                router=router_map.ROUTER_MAP[method],
                status=status,
                args=resolution.kwargs,
                error=error,
                snapshot=snapshot_name,
            )
        )
        write_manifest(records)
        print(f"[{i}/{len(order)}] {method}: {status}")
        time.sleep(THROTTLE_SECONDS)

    print(f"Done - {len(records)} methods recorded in {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
