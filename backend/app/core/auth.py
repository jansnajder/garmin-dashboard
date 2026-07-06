import json
import re
import shutil
import threading
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from garminconnect import Garmin, GarminConnectAuthenticationError

from app.core import paths

# Where the PoC persisted its token; only read by the first-run migration.
LEGACY_TOKEN_DIR = Path.home() / ".garminconnect"


class AccountManager:
    """
    Owns Garmin login, MFA, token persistence and the active client.

    Accounts are remembered in <data_dir>/accounts.json as
    {slug, email, display_name, last_used}; each account's OAuth tokens live in
    <data_dir>/accounts/<slug>/tokens/. Passwords are never written anywhere.

    A pending MFA login must be completed on the same Garmin instance
    (the library keeps the MFA session on the client object), so it is held
    in memory between start_login() and submit_mfa().

    The garmin_factory constructor argument exists for tests, which inject a
    fake Garmin class. One re-entrant lock guards all state; a desktop app has
    no concurrency to speak of, so network calls under it are acceptable.
    The constructor does no I/O.

    :param garmin_factory: callable producing Garmin instances
    :param data_dir: storage root, defaults to the per-user app data directory
    """

    def __init__(self, garmin_factory: Callable[..., Garmin] = Garmin, data_dir: Path | None = None) -> None:
        self._factory = garmin_factory
        self._dir = data_dir
        self._lock = threading.RLock()
        self._active: Garmin | None = None
        self._active_slug: str | None = None
        self._pending: Garmin | None = None
        self._pending_email: str | None = None

    def list_accounts(self) -> list[dict[str, str | None]]:
        """
        Return the remembered accounts from accounts.json.

        :return: account entries, empty list when none are remembered yet
        """
        with self._lock:
            return self._load_accounts()

    def start_login(self, email: str, password: str) -> str:
        """
        Start a credential login; on success the account becomes active and is remembered.

        :param email: Garmin account email
        :param password: Garmin account password, kept only for the duration of the call
        :return: "ok" on completed login, "needs_mfa" when submit_mfa() must follow
        :raises GarminConnectAuthenticationError: on invalid credentials
        """
        with self._lock:
            garmin = self._factory(email=email, password=password, return_on_mfa=True)
            status, _ = garmin.login()

            if status == "needs_mfa":
                self._pending = garmin
                self._pending_email = email

                return "needs_mfa"

            self._finish_login(garmin, email)

            return "ok"

    def submit_mfa(self, code: str) -> str:
        """
        Complete a pending MFA login started by start_login().

        :param code: the MFA code
        :return: "ok"
        :raises LookupError: when no login is pending
        :raises GarminConnectAuthenticationError: on a rejected code
        """
        with self._lock:
            if self._pending is None:
                raise LookupError("No login pending MFA")

            pending, email = self._pending, self._pending_email
            pending.resume_login({}, code)
            self._pending = None
            self._pending_email = None
            self._finish_login(pending, email)

            return "ok"

    def select(self, slug: str) -> str:
        """
        Activate a remembered account from its persisted token.

        The token login loads the user profile over the network, which doubles
        as verification; refreshed tokens are re-dumped so they stay valid.

        :param slug: slug of the remembered account
        :return: "ok" on success, "needs_login" when the slug is unknown or the token expired
        """
        with self._lock:
            accounts = self._load_accounts()
            entry = next((a for a in accounts if a["slug"] == slug), None)

            if entry is None:
                return "needs_login"

            garmin = self._factory()

            try:
                garmin.login(str(self._token_dir(slug)))
            except GarminConnectAuthenticationError:
                return "needs_login"

            garmin.client.dump(str(self._token_dir(slug)))
            entry["last_used"] = _now()
            self._save_accounts(accounts)
            self._active = garmin
            self._active_slug = slug

            return "ok"

    def logout(self, forget: bool = False) -> None:
        """
        Drop the active client; with forget, also delete the remembered account and its tokens.

        :param forget: when True, remove the accounts.json entry and the token directory
        """
        with self._lock:
            slug = self._active_slug
            self._active = None
            self._active_slug = None

            if forget and slug is not None:
                self._delete_account(slug)

    def forget(self, slug: str) -> None:
        """
        Delete a remembered account and its stored tokens, active or not.

        :param slug: slug of the account to delete; unknown slugs are a no-op
        """
        with self._lock:
            if self._active_slug == slug:
                self._active = None
                self._active_slug = None

            self._delete_account(slug)

    def _delete_account(self, slug: str) -> None:
        """Remove a remembered account's accounts.json entry and its token directory."""
        accounts = [a for a in self._load_accounts() if a["slug"] != slug]
        self._save_accounts(accounts)
        shutil.rmtree(self._data_dir() / "accounts" / slug, ignore_errors=True)

    def active(self) -> Garmin | None:
        """
        Return the active Garmin client, or None when no account is active.

        :return: active client or None
        """
        with self._lock:
            return self._active

    def active_slug(self) -> str | None:
        """
        Return the slug of the active account, or None when no account is active.

        :return: active account slug or None
        """
        with self._lock:
            return self._active_slug

    def active_email(self) -> str | None:
        """
        Return the email of the active account, or None when no account is active.

        Falls back to the display name for entries without an email
        (the migrated legacy account).

        :return: active account email or None
        """
        with self._lock:
            if self._active_slug is None:
                return None

            entry = next((a for a in self._load_accounts() if a["slug"] == self._active_slug), None)

            if entry is None:
                return None

            return entry["email"] or entry["display_name"]

    def startup(self) -> None:
        """
        Restore state on server start: first-run migration, then auto-select of the
        most recently used account. Never raises - any failure just means no active
        account and the frontend lands on the login screen.
        """
        with self._lock:
            try:
                if not self._accounts_file().exists():
                    self._migrate_legacy()

                    return

                accounts = self._load_accounts()

                if accounts:
                    latest = max(accounts, key=lambda a: a["last_used"])
                    self.select(latest["slug"])
            except Exception:
                pass

    def _migrate_legacy(self) -> None:
        """
        Import the PoC's ~/.garminconnect token as the first remembered account.

        The email is not recoverable from a token store, so the entry is recorded
        under the fixed slug "legacy" with an empty email; a later credential login
        creates a proper entry and this one can be dropped via logout+forget.
        """
        if not (LEGACY_TOKEN_DIR / "garmin_tokens.json").exists():
            return

        garmin = self._factory()
        garmin.login(str(LEGACY_TOKEN_DIR))
        self._finish_login(garmin, "", slug="legacy")

    def _finish_login(self, garmin: Garmin, email: str, slug: str | None = None) -> None:
        """
        Shared post-login path: persist tokens, upsert the account entry, set active.

        :param garmin: freshly authenticated client
        :param email: account email, empty for the migrated legacy account
        :param slug: explicit slug override, derived from the email when None
        """
        slug = slug or _slugify(email)
        token_dir = self._token_dir(slug)
        token_dir.mkdir(parents=True, exist_ok=True)
        garmin.client.dump(str(token_dir))

        accounts = [a for a in self._load_accounts() if a["slug"] != slug]
        accounts.append(
            {
                "slug": slug,
                "email": email,
                "display_name": garmin.get_full_name(),
                "last_used": _now(),
            }
        )
        self._save_accounts(accounts)
        self._active = garmin
        self._active_slug = slug

    def _data_dir(self) -> Path:
        """Return the storage root, resolving the default lazily to keep the constructor I/O-free."""
        return self._dir if self._dir is not None else paths.data_dir()

    def _accounts_file(self) -> Path:
        return self._data_dir() / "accounts.json"

    def _token_dir(self, slug: str) -> Path:
        return self._data_dir() / "accounts" / slug / "tokens"

    def _load_accounts(self) -> list[dict[str, str | None]]:
        try:
            return json.loads(self._accounts_file().read_text())
        except FileNotFoundError:
            return []

    def _save_accounts(self, accounts: list[dict[str, str | None]]) -> None:
        file = self._accounts_file()
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(accounts, indent=2))


def _slugify(email: str) -> str:
    """
    Derive a filesystem-safe slug from the full email.

    Emails are the natural unique key, so full-email slugs are collision-free
    and a re-login with the same email updates the same entry.

    :param email: account email
    :return: lowercase slug, e.g. john.doe@example.com -> john-doe-example-com
    """
    return re.sub(r"[^a-z0-9]+", "-", email.lower()).strip("-")


def _now() -> str:
    """Return the current local time as a second-resolution ISO string."""
    return datetime.now().isoformat(timespec="seconds")


manager = AccountManager()
