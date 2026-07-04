from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from garminconnect import GarminConnectAuthenticationError

from app.core import auth, deps
from app.core.auth import AccountManager
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


class _FakeTokenClient:
    """Mimics garmin.client just enough to persist a token file like the real dump() does."""

    def dump(self, path: str) -> None:
        directory = Path(path)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "garmin_tokens.json").write_text('{"di_token": "fake"}')


class FakeAuthGarmin(FakeGarmin):
    """
    FakeGarmin extended with the auth surface AccountManager uses.

    Behavior is steered by flags on the owning FakeGarminFactory: mfa makes
    credential logins demand MFA, fail_token_login makes token logins fail.
    Token logins also fail when the token file is missing, matching the real
    library. self.client.dump() really writes garmin_tokens.json so tests can
    assert on persistence.
    """

    def __init__(
        self,
        factory: "FakeGarminFactory",
        email: str | None = None,
        password: str | None = None,
        return_on_mfa: bool = False,
    ) -> None:
        super().__init__()
        self._factory = factory
        self.email = email
        self.password = password
        self.return_on_mfa = return_on_mfa
        self.mfa_code: str | None = None
        self.client = _FakeTokenClient()

    def login(self, tokenstore: str | None = None) -> tuple[str | None, str | None]:
        if tokenstore is not None:
            if self._factory.fail_token_login or not (Path(tokenstore) / "garmin_tokens.json").exists():
                raise GarminConnectAuthenticationError("token rejected")

            return (None, None)

        if self.email is None or self.password is None:
            raise GarminConnectAuthenticationError("Username and password are required")

        if self._factory.mfa:
            return ("needs_mfa", None)

        return (None, None)

    def resume_login(self, client_state: dict, mfa_code: str) -> tuple[str | None, str | None]:
        self.mfa_code = mfa_code

        return (None, None)

    def get_full_name(self) -> str:
        return "Test User"


class FakeGarminFactory:
    """
    Callable standing in for the Garmin class; records every construction.

    Flip mfa / fail_token_login on the instance to steer the fakes it produces.
    """

    def __init__(self) -> None:
        self.mfa = False
        self.fail_token_login = False
        self.calls: list[dict] = []
        self.instances: list[FakeAuthGarmin] = []

    def __call__(self, **kwargs) -> FakeAuthGarmin:
        self.calls.append(kwargs)
        garmin = FakeAuthGarmin(self, **kwargs)
        self.instances.append(garmin)

        return garmin


@pytest.fixture
def cache(tmp_path) -> Cache:
    """A Cache backed by a throwaway SQLite file."""
    return Cache(str(tmp_path / "cache.db"))


@pytest.fixture
def fake_garmin() -> FakeGarmin:
    """A recording fake Garmin client."""
    return FakeGarmin()


@pytest.fixture
def factory() -> FakeGarminFactory:
    """A recording fake Garmin factory for AccountManager tests."""
    return FakeGarminFactory()


@pytest.fixture
def manager(tmp_path, factory) -> AccountManager:
    """An AccountManager with a fake Garmin factory and throwaway storage."""
    return AccountManager(garmin_factory=factory, data_dir=tmp_path / "data")


@pytest.fixture
def client(cache, fake_garmin, manager, monkeypatch) -> TestClient:
    """TestClient with temp cache, a throwaway account manager and the Garmin dependency overridden."""
    monkeypatch.setattr(deps, "cache", cache)
    monkeypatch.setattr(auth, "manager", manager)
    app.dependency_overrides[get_garmin] = lambda: fake_garmin

    yield TestClient(app)

    app.dependency_overrides.clear()
