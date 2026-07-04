from fastapi import APIRouter, HTTPException
from garminconnect import (
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)
from pydantic import BaseModel

# Module import keeps auth.manager swappable in tests.
from app.core import auth

router = APIRouter(prefix="/api")


class LoginRequest(BaseModel):
    """Credentials for POST /api/auth/login; the password is never persisted."""

    email: str
    password: str


class MfaRequest(BaseModel):
    """MFA code for POST /api/auth/mfa."""

    code: str


class SelectRequest(BaseModel):
    """Remembered-account slug for POST /api/auth/select."""

    slug: str


class LogoutRequest(BaseModel):
    """Logout options for POST /api/auth/logout; forget also deletes the remembered account."""

    forget: bool = False


@router.get("/auth/status")
def status() -> dict[str, str | None]:
    """Return the active account's email, or null when nobody is logged in."""
    return {"active": auth.manager.active_email()}


@router.get("/auth/accounts")
def accounts() -> list[dict[str, str]]:
    """Return the remembered accounts."""
    return auth.manager.list_accounts()


@router.post("/auth/login")
def login(body: LoginRequest) -> dict[str, str]:
    """Start a credential login; "needs_mfa" means POST /api/auth/mfa must follow."""
    try:
        return {"status": auth.manager.start_login(body.email, body.password)}
    except GarminConnectTooManyRequestsError:
        raise HTTPException(429, "Garmin rate limit - wait a few minutes")
    except GarminConnectAuthenticationError:
        raise HTTPException(401, "Invalid credentials")


@router.post("/auth/mfa")
def mfa(body: MfaRequest) -> dict[str, str]:
    """Complete a pending MFA login."""
    try:
        return {"status": auth.manager.submit_mfa(body.code)}
    except LookupError:
        raise HTTPException(409, "No login pending MFA")
    except GarminConnectAuthenticationError:
        raise HTTPException(401, "MFA code rejected")


@router.post("/auth/select")
def select(body: SelectRequest) -> dict[str, str]:
    """Activate a remembered account; "needs_login" means a fresh login is required."""
    return {"status": auth.manager.select(body.slug)}


@router.post("/auth/logout")
def logout(body: LogoutRequest) -> dict[str, str]:
    """Log out the active account, optionally forgetting it."""
    auth.manager.logout(body.forget)

    return {"status": "ok"}
