from fastapi import APIRouter, Query

from app.core import deps  # module import keeps deps.cache swappable in tests

router = APIRouter(prefix="/api")


@router.post("/cache/clear")
def clear_cache(scope: str = Query(default="volatile", pattern="^(volatile|all)$")) -> dict[str, bool]:
    """
    Delete SQLite cache entries.

    :param scope: 'volatile' (default) drops only TTL-governed entries, 'all' drops everything
    :return: confirmation dict
    """
    deps.cache.clear(scope)

    return {"cleared": True}
