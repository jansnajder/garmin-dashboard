import os
import threading
from pathlib import Path

from dotenv import load_dotenv
from garminconnect import Garmin

load_dotenv()

_client: Garmin | None = None
_lock = threading.Lock()
TOKEN_PATH = str(Path.home() / ".garminconnect")


def get_client() -> Garmin:
    """
    Return the shared Garmin client, initializing and logging in on first call.

    Tokens are persisted to TOKEN_PATH so subsequent runs skip full re-authentication.
    Credentials are read from the environment; when absent (e.g. a packaged build),
    login falls back to the persisted token at TOKEN_PATH.

    :return: authenticated Garmin client instance
    :raises GarminConnectAuthenticationError: if no valid token exists and no credentials are set
    """
    global _client

    with _lock:
        if _client is None:
            client = Garmin(
                email=os.environ.get("GARMIN_EMAIL"),
                password=os.environ.get("GARMIN_PASSWORD"),
            )
            client.login(TOKEN_PATH)
            _client = client

    return _client


def reset_client() -> None:
    """
    Force re-authentication on the next get_client() call.

    Call this after a GarminConnectAuthenticationError to recover without a process restart.
    """
    global _client

    with _lock:
        _client = None
