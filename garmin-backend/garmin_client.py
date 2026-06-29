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

    :return: authenticated Garmin client instance
    :raises KeyError: if GARMIN_EMAIL or GARMIN_PASSWORD are not set in the environment
    """
    global _client

    with _lock:
        if _client is None:
            client = Garmin(
                email=os.environ["GARMIN_EMAIL"],
                password=os.environ["GARMIN_PASSWORD"],
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
