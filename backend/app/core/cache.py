import json
import sqlite3
import threading
import time
from typing import Any

TTL = 3600


class Cache:
    """
    SQLite-backed TTL cache. Stores JSON-serialized data keyed by a string.
    The database file is created at the given path on first use; databases
    from the pre-permanence schema are migrated by adding the column.

    Entries marked permanent never expire; the TTL applies only to volatile ones.

    All methods are thread-safe; a single lock serializes all SQLite operations.

    :param path: path to the SQLite database file
    """

    def __init__(self, path: str = "cache.db") -> None:
        self._lock = threading.Lock()
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS cache "
            "(key TEXT PRIMARY KEY, data TEXT, fetched_at INTEGER, permanent INTEGER DEFAULT 0)"
        )
        cols = [row[1] for row in self._db.execute("PRAGMA table_info(cache)")]

        if "permanent" not in cols:
            self._db.execute("ALTER TABLE cache ADD COLUMN permanent INTEGER DEFAULT 0")

    def get(self, key: str) -> tuple[bool, Any]:
        """
        Return whether key exists in cache and its data. Permanent entries are
        always fresh; volatile ones only within the TTL.

        :param key: cache key to look up
        :return: (True, data) if found and fresh, (False, None) if missing or expired
        """
        with self._lock:
            row = self._db.execute(
                "SELECT data, fetched_at, permanent FROM cache WHERE key = ?", (key,)
            ).fetchone()

        if row and (row[2] or (time.time() - row[1]) < TTL):
            return True, json.loads(row[0])

        return False, None

    def set(self, key: str, data: Any, permanent: bool = False) -> None:
        """
        Write data to the cache under key, overwriting any existing entry.

        :param key: cache key
        :param data: data to cache (must be JSON-serializable)
        :param permanent: when True the entry never expires
        """
        with self._lock:
            self._db.execute(
                "INSERT OR REPLACE INTO cache VALUES (?, ?, ?, ?)",
                (key, json.dumps(data), int(time.time()), int(permanent)),
            )
            self._db.commit()

    def clear(self, scope: str = "volatile") -> None:
        """
        Delete entries from the cache.

        :param scope: 'volatile' deletes only TTL-governed entries, 'all' deletes everything
        """
        with self._lock:
            if scope == "all":
                self._db.execute("DELETE FROM cache")
            else:
                self._db.execute("DELETE FROM cache WHERE permanent = 0")

            self._db.commit()
