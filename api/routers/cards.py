"""Cards router."""

from fastapi import APIRouter

router = APIRouter(prefix="/cards", tags=["cards"])


@router.get("/")
async def list_cards() -> list[dict]:
    """List all tracked cards."""
    raise NotImplementedError
