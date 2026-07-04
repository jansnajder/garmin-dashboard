import pytest
from fastapi.testclient import TestClient

from app.core import deps
from app.core.cache import Cache
from app.core.deps import get_garmin
from app.main import app


class FakeGarmin:
    """
    Stands in for garminconnect.Garmin in tests.

    Any get_* method call is recorded in self.calls and returns a canned
    dict identifying the method and its arguments.
    """

    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple]] = []

    def __getattr__(self, name: str):
        def method(*args):
            self.calls.append((name, args))

            return {"method": name, "args": list(args)}

        return method


@pytest.fixture
def cache(tmp_path) -> Cache:
    """A Cache backed by a throwaway SQLite file."""
    return Cache(str(tmp_path / "cache.db"))


@pytest.fixture
def fake_garmin() -> FakeGarmin:
    """A recording fake Garmin client."""
    return FakeGarmin()


@pytest.fixture
def client(cache, fake_garmin, monkeypatch) -> TestClient:
    """TestClient with the real cache swapped for a temp one and the Garmin dependency overridden."""
    monkeypatch.setattr(deps, "cache", cache)
    app.dependency_overrides[get_garmin] = lambda: fake_garmin

    yield TestClient(app)

    app.dependency_overrides.clear()
