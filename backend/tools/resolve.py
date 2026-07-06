"""
Pure argument-resolution logic for probing garminconnect.Garmin get_* methods.

No network access and no Garmin instantiation happens here - only inspect.Signature
objects and previously harvested ids are consumed, which keeps this module unit-testable
without a live account.
"""

import inspect
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any, Literal

RANGE_DAYS = 7

Status = Literal["data", "empty", "404", "error", "skipped"]


@dataclass
class Record:
    """
    One probed (or skipped) get_* method, as persisted in snapshots/_manifest.json.

    :param method: method name, e.g. "get_stats"
    :param router: target router file from router_map.ROUTER_MAP, e.g. "wellness.py"
    :param status: "data" | "empty" | "404" | "error" | "skipped"
    :param args: kwargs actually passed to the method, empty when none
    :param error: exception message when status is "error"/"404", skip reason when "skipped"
    :param snapshot: filename under snapshots/ holding the raw JSON response, None when not written
    """

    method: str
    router: str
    status: Status
    args: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    snapshot: str | None = None


@dataclass
class Resolution:
    """Outcome of resolving one method's arguments: kwargs to call with, or a skip reason."""

    kwargs: dict[str, Any] | None
    reason: str | None = None


def yesterday() -> str:
    """Return yesterday's date, ISO format - used for all single-date params."""
    return (date.today() - timedelta(days=1)).isoformat()


def range_start() -> str:
    """Return the start of a RANGE_DAYS window ending yesterday, ISO format."""
    return (date.today() - timedelta(days=RANGE_DAYS)).isoformat()


# Exact-name buckets for date-like parameters.
_SINGLE_DATE_NAMES = {"cdate", "fordate"}
_RANGE_DATE_NAMES = {"startdate", "enddate"}

# get_race_predictions must be called with all of startdate/enddate/_type or none
# (it raises ValueError otherwise); every other method resolves correctly through
# the generic per-parameter rules below.
METHOD_OVERRIDES: dict[str, dict[str, Any]] = {
    "get_race_predictions": {},
}


@dataclass
class ProbeState:
    """
    Accumulates ids harvested from already-probed methods, for id-like params of
    methods probed later in the same run. Populated by harvest(), read by resolve_args().
    """

    activity_id: Any = None
    device_id: Any = None
    user_profile_number: Any = None
    gear_uuid: Any = None
    workout_id: Any = None
    scheduled_workout_id: Any = None
    plan_id: Any = None
    scorecard_id: Any = None
    missing_keys: dict[str, list[str]] = field(default_factory=dict)

    def resolvers(self) -> dict[str, Any]:
        """Return the id-like parameter name -> resolved value mapping for the current state."""
        return {
            "activity_id": self.activity_id,
            "device_id": self.device_id,
            "userProfileNumber": self.user_profile_number,
            "gearUUID": self.gear_uuid,
            "workout_id": self.workout_id,
            "scheduled_workout_id": self.scheduled_workout_id,
            "plan_id": self.plan_id,
            "scorecard_id": self.scorecard_id,
            "year": date.today().year,
            "month": date.today().month,
        }

    def skip_reason(self, pname: str) -> str:
        """
        Build a skip reason for an id-like parameter that has no resolved value yet.

        :param pname: the unresolved parameter name
        :return: human-readable reason, including observed parent-response keys when known
        """
        keys = self.missing_keys.get(pname)

        if keys:
            return f"could not find '{pname}' in parent response; top-level keys were {keys}"

        return f"parent call for '{pname}' has not produced a value yet (empty/missing/unprobed)"


def resolve_args(name: str, sig: inspect.Signature, state: ProbeState) -> Resolution:
    """
    Decide the kwargs to call Garmin.<name> with, or why it must be skipped.

    Classification is per-parameter and order-sensitive: id-like names are resolved
    from already-harvested state first, then exact date-name buckets, then
    type-disambiguated start/end/limit, then anything with a library default is
    simply omitted. A required parameter matching none of these rules is reported
    as skipped with an explicit reason.

    :param name: method name, e.g. "get_gear_stats"
    :param sig: inspect.signature(getattr(Garmin, name)), with self still present
    :param state: accumulated results from already-probed parent methods
    :return: Resolution with either kwargs or a skip reason
    """
    if name in METHOD_OVERRIDES:
        return Resolution(kwargs=dict(METHOD_OVERRIDES[name]))

    resolvers = state.resolvers()
    kwargs: dict[str, Any] = {}

    for pname, param in sig.parameters.items():
        if pname == "self":
            continue

        has_default = param.default is not inspect.Parameter.empty
        annotation = param.annotation

        if pname in resolvers:
            value = resolvers[pname]

            if value is None:
                return Resolution(kwargs=None, reason=state.skip_reason(pname))

            kwargs[pname] = value
            continue

        if pname in _SINGLE_DATE_NAMES:
            kwargs[pname] = yesterday()
            continue

        if pname in _RANGE_DATE_NAMES:
            kwargs[pname] = range_start() if pname == "startdate" else yesterday()
            continue

        if pname in ("start", "end") and annotation is str:
            kwargs[pname] = range_start() if pname == "start" else yesterday()
            continue

        if pname in ("start", "limit") and annotation is int:
            if has_default:
                continue

            kwargs[pname] = 1 if pname == "start" else 10
            continue

        if has_default:
            continue

        return Resolution(kwargs=None, reason=f"no resolution rule for required parameter '{pname}: {annotation}'")

    return Resolution(kwargs=kwargs)


def _first(items: Any) -> dict[str, Any] | None:
    """Return the first element of a non-empty list, else None."""
    if isinstance(items, list) and items:
        return items[0]

    return None


def harvest(method: str, data: Any, state: ProbeState) -> None:
    """
    Opportunistically fill ProbeState fields from a successful method's raw response.

    Only ever sets a field if it is still None (first writer wins), so a richer or
    earlier source is never clobbered by a later, sparser one.

    :param method: the probed method's name
    :param data: its raw JSON response
    :param state: accumulator to update in place
    """
    if method == "get_devices" and state.device_id is None:
        entry = _first(data)

        if entry and "deviceId" in entry:
            state.device_id = entry["deviceId"]
        elif isinstance(data, list) and data:
            state.missing_keys["device_id"] = sorted(data[0].keys())

    elif method == "get_activities" and state.activity_id is None:
        entry = _first(data) or (
            _first(data.get("activities")) if isinstance(data, dict) else None
        )

        if entry and "activityId" in entry:
            state.activity_id = entry["activityId"]

    elif method == "get_last_activity" and state.activity_id is None:
        if isinstance(data, dict) and "activityId" in data:
            state.activity_id = data["activityId"]

    elif method in ("get_user_profile", "get_userprofile_settings") and state.user_profile_number is None:
        if isinstance(data, dict):
            for key in ("userProfileNumber", "userProfilePK", "userProfileId", "profileId", "id"):
                if key in data:
                    state.user_profile_number = data[key]
                    break
            else:
                state.missing_keys["userProfileNumber"] = sorted(data.keys())

    elif method == "get_gear" and state.gear_uuid is None:
        entry = _first(data)

        if entry:
            for key in ("uuid", "gearUUID", "gearPk"):
                if key in entry:
                    state.gear_uuid = entry[key]
                    break
            else:
                state.missing_keys["gearUUID"] = sorted(entry.keys())

    elif method == "get_workouts" and state.workout_id is None:
        entry = _first(data)

        if entry and "workoutId" in entry:
            state.workout_id = entry["workoutId"]

    elif method == "get_training_plans" and state.plan_id is None:
        entry = _first(data.get("trainingPlanList")) if isinstance(data, dict) else _first(data)

        if entry and "trainingPlanId" in entry:
            state.plan_id = entry["trainingPlanId"]

    elif method == "get_golf_summary" and state.scorecard_id is None:
        entry = _first(data)

        if entry and "scorecardId" in entry:
            state.scorecard_id = entry["scorecardId"]

    elif method == "get_scheduled_workouts" and state.scheduled_workout_id is None:
        items = data.get("calendarItems") if isinstance(data, dict) else data
        workouts = [item for item in (items or []) if item.get("itemType") == "workout"]
        entry = _first(workouts)

        if entry and entry.get("id") is not None:
            state.scheduled_workout_id = entry["id"]
