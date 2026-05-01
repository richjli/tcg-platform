"""TCGPlayer price spider.

Fetches market prices for tracked cards via the TCGPlayer Partner API.
Requires TCGPLAYER_PUBLIC_KEY and TCGPLAYER_PRIVATE_KEY env vars.
Apply for access at https://developer.tcgplayer.com/developer-application-form.html
"""

import logging
import os
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

_API_BASE = "https://api.tcgplayer.com"
_TOKEN_URL = f"{_API_BASE}/token"
_CATALOG_URL = f"{_API_BASE}/catalog/products"
_PRICING_URL = f"{_API_BASE}/pricing/product"


@dataclass
class PriceResult:
    """A price observation returned by the spider."""

    card_name: str
    product_id: int
    market_price: float | None
    low_price: float | None
    url: str


def _get_token(public_key: str, private_key: str) -> str:
    """Fetch a short-lived OAuth bearer token from TCGPlayer."""
    data = {
        "grant_type": "client_credentials",
        "client_id": public_key,
        "client_secret": private_key,
    }
    response = httpx.post(_TOKEN_URL, data=data, timeout=15)
    response.raise_for_status()
    return str(response.json()["access_token"])


def _search_products(token: str, card_name: str) -> list[dict]:
    """Return product records matching card_name in the Pokémon category."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "productName": card_name,
        "categoryName": "Pokemon",
        "limit": 5,
    }
    response = httpx.get(_CATALOG_URL, headers=headers, params=params, timeout=15)
    response.raise_for_status()
    return list(response.json().get("results", []))


def _fetch_prices(token: str, product_ids: list[int]) -> dict[int, dict]:
    """Return a mapping of product_id → price data."""
    if not product_ids:
        return {}
    headers = {"Authorization": f"Bearer {token}"}
    ids_param = ",".join(str(i) for i in product_ids)
    response = httpx.get(f"{_PRICING_URL}/{ids_param}", headers=headers, timeout=15)
    response.raise_for_status()
    return {r["productId"]: r for r in response.json().get("results", [])}


def crawl(card_names: list[str]) -> list[PriceResult]:
    """Fetch market prices for the given card names from TCGPlayer.

    Returns an empty list and logs a warning if credentials are missing.
    """
    public_key = os.environ.get("TCGPLAYER_PUBLIC_KEY", "")
    private_key = os.environ.get("TCGPLAYER_PRIVATE_KEY", "")

    if not public_key or not private_key:
        logger.warning(
            "TCGPLAYER_PUBLIC_KEY / TCGPLAYER_PRIVATE_KEY not set — skipping"
        )
        return []

    try:
        token = _get_token(public_key, private_key)
    except httpx.HTTPError as exc:
        logger.error("TCGPlayer auth failed: %s", exc)
        return []

    results: list[PriceResult] = []
    for name in card_names:
        try:
            products = _search_products(token, name)
        except httpx.HTTPError as exc:
            logger.error("TCGPlayer search failed for %r: %s", name, exc)
            continue

        if not products:
            logger.debug("No TCGPlayer products found for %r", name)
            continue

        product = products[0]
        product_id: int = product["productId"]

        try:
            prices = _fetch_prices(token, [product_id])
        except httpx.HTTPError as exc:
            logger.error("TCGPlayer pricing failed for %r: %s", name, exc)
            continue

        price_data = prices.get(product_id, {})
        results.append(
            PriceResult(
                card_name=name,
                product_id=product_id,
                market_price=price_data.get("marketPrice"),
                low_price=price_data.get("lowPrice"),
                url=f"https://www.tcgplayer.com/product/{product_id}",
            )
        )

    return results
