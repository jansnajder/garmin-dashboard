"""Path resolution for dev (uv) and frozen (PyInstaller onedir)."""

import sys
from pathlib import Path

from platformdirs import user_data_dir


def is_frozen() -> bool:
    """
    Return whether the app is running from a PyInstaller bundle.

    :return: True when frozen, False in a normal Python/uv run
    """
    return getattr(sys, "frozen", False)


def frontend_dir() -> str:
    """
    Return the absolute path to the built frontend directory in either mode.

    Frozen builds unpack bundled data under sys._MEIPASS; dev runs read the
    Vite build output (frontend/dist) at the repo root, next to the backend
    project.

    :return: absolute path to the frontend directory
    """
    if is_frozen():
        return str(Path(sys._MEIPASS) / "frontend")

    return str(Path(__file__).resolve().parents[3] / "frontend" / "dist")


def data_dir() -> Path:
    """
    Return the per-user app data directory as a Path, creating it if needed.

    Resolved by platformdirs; on Windows this is %LOCALAPPDATA%\\GarminDashboard
    (appauthor=False keeps it flat, without an author subdirectory).

    :return: per-user app data directory
    """
    base = Path(user_data_dir("GarminDashboard", appauthor=False))
    base.mkdir(parents=True, exist_ok=True)

    return base


def cache_path() -> str:
    """
    Return a writable path for the SQLite cache, creating the directory if needed.

    The install directory may be read-only, so the cache lives under the
    user's local app data.

    :return: absolute path to the cache database file
    """
    return str(data_dir() / "cache.db")
