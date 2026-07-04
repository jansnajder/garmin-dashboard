import asyncio
import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import auth as core_auth
from app.core import capture
from app.core.paths import frontend_dir
from app.routers import auth, cache, dashboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Run first-run migration, auto-select the last-used account, and start the
    auto-capture background task; cancel it on shutdown.
    """
    core_auth.manager.startup()
    task = asyncio.create_task(capture.run_forever())

    yield

    # Cancellation lands on capture's awaits; an in-flight Garmin call finishes
    # in its worker thread and may briefly delay interpreter exit.
    task.cancel()

    with contextlib.suppress(asyncio.CancelledError):
        await task


app = FastAPI(lifespan=lifespan)

app.include_router(dashboard.router)
app.include_router(cache.router)
app.include_router(auth.router)

app.frontend("/", directory=frontend_dir())
