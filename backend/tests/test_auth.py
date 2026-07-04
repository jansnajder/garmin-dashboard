import json
from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.core import auth, deps
from app.main import app

EMAIL = "john.doe@example.com"
SLUG = "john-doe-example-com"


def _accounts(manager) -> list[dict]:
    """Read accounts.json through the manager's own storage."""
    return json.loads((manager._data_dir() / "accounts.json").read_text())


def _token_file(manager, slug: str):
    """Return the Path of a slug's persisted token file."""
    return manager._data_dir() / "accounts" / slug / "tokens" / "garmin_tokens.json"


def test_clean_login(manager, factory):
    """A credential login persists tokens, remembers the account and sets it active."""
    assert manager.start_login(EMAIL, "secret") == "ok"

    assert factory.calls == [{"email": EMAIL, "password": "secret", "return_on_mfa": True}]
    assert manager.active() is factory.instances[0]
    assert manager.active_slug() == SLUG
    assert _token_file(manager, SLUG).exists()

    (entry,) = _accounts(manager)

    assert entry["slug"] == SLUG
    assert entry["email"] == EMAIL
    assert entry["display_name"] == "Test User"
    assert entry["last_used"]

    for file in manager._data_dir().rglob("*"):
        if file.is_file():
            assert "secret" not in file.read_text()


def test_slug_from_email(manager):
    """Slugs are derived from the full email, so distinct emails get distinct slugs."""
    manager.start_login(EMAIL, "pw")
    manager.start_login("jane+garmin@test.org", "pw")

    slugs = {a["slug"] for a in manager.list_accounts()}

    assert slugs == {SLUG, "jane-garmin-test-org"}


def test_mfa_path(manager, factory):
    """An MFA login is completed on the pending instance; tokens are dumped only after the code."""
    factory.mfa = True

    assert manager.start_login(EMAIL, "pw") == "needs_mfa"
    assert manager.active() is None
    assert not _token_file(manager, SLUG).exists()

    assert manager.submit_mfa("123456") == "ok"

    assert manager.active() is factory.instances[0]
    assert factory.instances[0].mfa_code == "123456"
    assert _token_file(manager, SLUG).exists()


def test_mfa_without_pending(manager):
    """Submitting an MFA code with no login pending raises LookupError."""
    with pytest.raises(LookupError):
        manager.submit_mfa("123456")


def test_select_remembered(manager, factory):
    """Selecting a remembered account logs in from tokens only, re-dumps them and bumps last_used."""
    manager.start_login(EMAIL, "pw")
    manager.logout()

    accounts = _accounts(manager)
    accounts[0]["last_used"] = "2000-01-01T00:00:00"
    manager._save_accounts(accounts)
    _token_file(manager, SLUG).write_text("stale")

    assert manager.select(SLUG) == "ok"

    assert factory.calls[-1] == {}
    assert manager.active() is factory.instances[-1]
    assert _accounts(manager)[0]["last_used"] != "2000-01-01T00:00:00"
    assert _token_file(manager, SLUG).read_text() != "stale"


def test_select_expired_token(manager, factory):
    """A dead token turns select into needs_login and leaves nobody active."""
    manager.start_login(EMAIL, "pw")
    manager.logout()
    factory.fail_token_login = True

    assert manager.select(SLUG) == "needs_login"
    assert manager.active() is None


def test_select_unknown_slug(manager):
    """An unknown slug turns select into needs_login."""
    assert manager.select("nobody") == "needs_login"


def test_logout_keeps_account(manager):
    """A plain logout drops the client but keeps the remembered account and its tokens."""
    manager.start_login(EMAIL, "pw")
    manager.logout()

    assert manager.active() is None
    assert manager.active_slug() is None
    assert len(manager.list_accounts()) == 1
    assert _token_file(manager, SLUG).exists()


def test_logout_forget(manager):
    """Logout with forget removes the accounts.json entry and the token directory."""
    manager.start_login(EMAIL, "pw")
    manager.logout(forget=True)

    assert manager.list_accounts() == []
    assert not (manager._data_dir() / "accounts" / SLUG).exists()


def test_cache_key_prefix(client, cache, manager):
    """Data fetched while logged in lands in the cache under the account-slug prefix."""
    manager.start_login(EMAIL, "pw")

    assert client.get("/api/summary").status_code == 200

    found, _ = cache.get(f"{SLUG}:summary:{date.today().isoformat()}")

    assert found


def test_no_account_gives_401(cache, manager, monkeypatch):
    """Without an active account, data endpoints return 401."""
    monkeypatch.setattr(deps, "cache", cache)
    monkeypatch.setattr(auth, "manager", manager)

    resp = TestClient(app).get("/api/summary")

    assert resp.status_code == 401


def test_startup_migration(manager, tmp_path, monkeypatch):
    """A ~/.garminconnect token is imported as the "legacy" account when no accounts exist yet."""
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    (legacy / "garmin_tokens.json").write_text('{"di_token": "old"}')
    monkeypatch.setattr(auth, "LEGACY_TOKEN_DIR", legacy)

    manager.startup()

    (entry,) = manager.list_accounts()

    assert entry["slug"] == "legacy"
    assert entry["email"] == ""
    assert manager.active_slug() == "legacy"
    assert manager.active_email() == "Test User"
    assert _token_file(manager, "legacy").exists()


def test_startup_no_legacy_token(manager, tmp_path, monkeypatch):
    """A first run without a legacy token leaves no accounts and nobody active."""
    monkeypatch.setattr(auth, "LEGACY_TOKEN_DIR", tmp_path / "missing")

    manager.startup()

    assert manager.list_accounts() == []
    assert manager.active() is None


def test_startup_auto_selects_last_used(manager):
    """Startup activates the most recently used remembered account."""
    manager.start_login(EMAIL, "pw")
    manager.start_login("jane+garmin@test.org", "pw")
    manager.logout()

    accounts = _accounts(manager)

    for entry in accounts:
        entry["last_used"] = "2020-01-01T00:00:00" if entry["slug"] == SLUG else "2010-01-01T00:00:00"

    manager._save_accounts(accounts)

    manager.startup()

    assert manager.active_slug() == SLUG


def test_startup_survives_dead_token(manager, factory):
    """A failing token login during startup leaves nobody active without raising."""
    manager.start_login(EMAIL, "pw")
    manager.logout()
    factory.fail_token_login = True

    manager.startup()

    assert manager.active() is None


def test_auth_endpoints(client, manager):
    """The auth endpoints drive the manager through a full login/select/logout round trip."""
    assert client.get("/api/auth/status").json() == {"active": None}
    assert client.get("/api/auth/accounts").json() == []

    resp = client.post("/api/auth/login", json={"email": EMAIL, "password": "pw"})

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
    assert client.get("/api/auth/status").json() == {"active": EMAIL}

    (entry,) = client.get("/api/auth/accounts").json()

    assert entry["slug"] == SLUG

    assert client.post("/api/auth/mfa", json={"code": "123456"}).status_code == 409

    assert client.post("/api/auth/logout", json={"forget": False}).json() == {"status": "ok"}
    assert client.get("/api/auth/status").json() == {"active": None}

    assert client.post("/api/auth/select", json={"slug": SLUG}).json() == {"status": "ok"}
    assert client.get("/api/auth/status").json() == {"active": EMAIL}

    assert client.post("/api/auth/select", json={"slug": "nobody"}).json() == {"status": "needs_login"}
