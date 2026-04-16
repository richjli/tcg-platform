"""Prices router."""

from fastapi import APIRouter

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/")
async def list_prices() -> list[dict]:
    """List price data for tracked cards."""
    raise NotImplementedError
