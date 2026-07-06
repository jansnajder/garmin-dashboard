import inspect

from garminconnect import Garmin

from tools import router_map
from tools.resolve import ProbeState, resolve_args


def test_router_map_covers_every_installed_get_method() -> None:
    installed = {name for name in dir(Garmin) if name.startswith("get_")}
    assert set(router_map.ALL_METHODS) == installed


def test_single_date_param_resolves_to_yesterday() -> None:
    sig = inspect.signature(Garmin.get_stats)
    resolution = resolve_args("get_stats", sig, ProbeState())

    assert resolution.kwargs is not None
    assert "cdate" in resolution.kwargs


def test_required_pagination_gets_explicit_values() -> None:
    sig = inspect.signature(Garmin.get_adhoc_challenges)
    resolution = resolve_args("get_adhoc_challenges", sig, ProbeState())

    assert resolution.kwargs == {"start": 1, "limit": 10}


def test_race_predictions_override_has_no_args() -> None:
    sig = inspect.signature(Garmin.get_race_predictions)
    resolution = resolve_args("get_race_predictions", sig, ProbeState())

    assert resolution.kwargs == {}


def test_str_typed_range_resolves_to_dates() -> None:
    sig = inspect.signature(Garmin.get_daily_steps)
    resolution = resolve_args("get_daily_steps", sig, ProbeState())

    assert resolution.kwargs is not None
    assert set(resolution.kwargs) == {"start", "end"}


def test_scheduled_workouts_resolves_year_and_month() -> None:
    sig = inspect.signature(Garmin.get_scheduled_workouts)
    resolution = resolve_args("get_scheduled_workouts", sig, ProbeState())

    assert resolution.kwargs is not None
    assert set(resolution.kwargs) == {"year", "month"}


def test_id_like_param_skips_with_reason_when_unresolved() -> None:
    sig = inspect.signature(Garmin.get_activity)
    resolution = resolve_args("get_activity", sig, ProbeState())

    assert resolution.kwargs is None
    assert "activity_id" in resolution.reason


def test_id_like_param_resolves_once_harvested() -> None:
    sig = inspect.signature(Garmin.get_activity)
    state = ProbeState(activity_id=12345)
    resolution = resolve_args("get_activity", sig, state)

    assert resolution.kwargs == {"activity_id": 12345}
