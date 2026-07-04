import sqlite3

from app.core.cache import Cache


def test_get_missing_key(cache):
    """A key that was never set reports a miss."""
    assert cache.get("missing") == (False, None)


def test_set_then_get(cache):
    """Data round-trips through the cache unchanged."""
    data = {"steps": 1234, "nested": [1, 2, 3]}

    cache.set("k", data)

    assert cache.get("k") == (True, data)


def test_cross_key_isolation(cache):
    """Writing one key neither creates nor mutates another."""
    cache.set("k1", "one")

    assert cache.get("k2") == (False, None)

    cache.set("k1", "changed")
    cache.set("k2", "two")

    assert cache.get("k1") == (True, "changed")
    assert cache.get("k2") == (True, "two")


def test_ttl_expiry(cache, monkeypatch):
    """A volatile entry expires once the TTL has passed."""
    cache.set("k", "data")

    monkeypatch.setattr("app.core.cache.TTL", 0)

    assert cache.get("k") == (False, None)


def test_permanent_survives_ttl(cache, monkeypatch):
    """A permanent entry ignores the TTL entirely."""
    cache.set("k", "data", permanent=True)

    monkeypatch.setattr("app.core.cache.TTL", 0)

    assert cache.get("k") == (True, "data")


def test_clear_volatile_keeps_permanent(cache):
    """The default clear scope drops only TTL-governed entries."""
    cache.set("v", "volatile")
    cache.set("p", "permanent", permanent=True)

    cache.clear()

    assert cache.get("v") == (False, None)
    assert cache.get("p") == (True, "permanent")


def test_clear_all(cache):
    """The 'all' scope drops permanent entries too."""
    cache.set("v", "volatile")
    cache.set("p", "permanent", permanent=True)

    cache.clear("all")

    assert cache.get("v") == (False, None)
    assert cache.get("p") == (False, None)


def test_permanent_column_migration(tmp_path, monkeypatch):
    """A database from the pre-permanence schema is migrated; its rows behave as volatile."""
    path = str(tmp_path / "old.db")
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE cache (key TEXT PRIMARY KEY, data TEXT, fetched_at INTEGER)")
    db.execute("INSERT INTO cache VALUES ('k', '\"old\"', strftime('%s', 'now'))")
    db.commit()
    db.close()

    cache = Cache(path)

    assert cache.get("k") == (True, "old")

    monkeypatch.setattr("app.core.cache.TTL", 0)

    assert cache.get("k") == (False, None)
