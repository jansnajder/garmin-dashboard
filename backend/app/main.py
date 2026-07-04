from fastapi import FastAPI

from app.core.paths import frontend_dir
from app.routers import cache, dashboard

app = FastAPI()

app.include_router(dashboard.router)
app.include_router(cache.router)

app.frontend("/", directory=frontend_dir())
