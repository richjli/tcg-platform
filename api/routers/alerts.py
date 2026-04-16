"""Stock alerts router."""

from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/")
async def list_alerts() -> list[dict]:
    """List active stock alerts."""
    raise NotImplementedError
