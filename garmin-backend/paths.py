"""Path resolution for dev (uv) and frozen (PyInstaller onedir)."""

import sys
from pathlib import Path


def is_frozen() -> bool:
    """
    Return whether the app is running from a PyInstaller bundle.

    :return: True when frozen, False in a normal Python/uv run
    """
    return getattr(sys, "frozen", False)


def frontend_dir() -> str:
    """
    Return the absolute path to the frontend directory in either mode.

    Frozen builds unpack bundled data under sys._MEIPASS; dev runs read the
    sibling frontend/ folder next to the backend package.

    :return: absolute path to the frontend directory
    """
    if is_frozen():
        return str(Path(sys._MEIPASS) / "frontend")

    return str(Path(__file__).resolve().parent.parent / "frontend")


def cache_path() -> str:
    """
    Return a writable path for the SQLite cache, creating the directory if needed.

    The install directory may be read-only, so the cache lives under the
    user's local app data.

    :return: absolute path to the cache database file
    """
    base = Path.home() / "AppData" / "Local" / "GarminDashboard"
    base.mkdir(parents=True, exist_ok=True)

    return str(base / "cache.db")
