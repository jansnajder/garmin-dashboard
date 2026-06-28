import json
import sqlite3
import time
from typing import Any

TTL = 3600


class Cache:
    """
    SQLite-backed TTL cache. Stores JSON-serialized data keyed by a string.
    The database file is created at the given path on first use.

    :param path: path to the SQLite database file
    """

    def __init__(self, path: str = "cache.db") -> None:
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS cache "
            "(key TEXT PRIMARY KEY, data TEXT, fetched_at INTEGER)"
        )

    def get(self, key: str) -> tuple[bool, Any]:
        """
        Return whether key exists in cache within TTL and its data.

        :param key: cache key to look up
        :return: (True, data) if found and fresh, (False, None) if missing or expired
        """
        row = self._db.execute(
            "SELECT data, fetched_at FROM cache WHERE key = ?", (key,)
        ).fetchone()

        if row and (time.time() - row[1]) < TTL:
            return True, json.loads(row[0])

        return False, None

    def set(self, key: str, data: Any) -> None:
        """
        Write data to the cache under key, overwriting any existing entry.

        :param key: cache key
        :param data: data to cache (must be JSON-serializable)
        """
        self._db.execute(
            "INSERT OR REPLACE INTO cache VALUES (?, ?, ?)",
            (key, json.dumps(data), int(time.time())),
        )
        self._db.commit()

    def clear(self) -> None:
        """
        Delete all entries from the cache.
        """
        self._db.execute("DELETE FROM cache")
        self._db.commit()
