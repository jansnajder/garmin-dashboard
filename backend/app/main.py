from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import auth as core_auth
from app.core.paths import frontend_dir
from app.routers import auth, cache, dashboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run first-run migration and auto-select the last-used account before serving."""
    core_auth.manager.startup()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(dashboard.router)
app.include_router(cache.router)
app.include_router(auth.router)

app.frontend("/", directory=frontend_dir())
