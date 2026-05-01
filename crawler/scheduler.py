"""Crawler job scheduler.

Runs price and stock crawlers on a configurable interval and posts
results to the local API.  Start with:

    DATABASE_URL=... uv run python -m crawler.scheduler
"""

import logging
import os

import httpx
from apscheduler.schedulers.blocking import BlockingScheduler

from crawler.spiders import tcgplayer

logger = logging.getLogger(__name__)

_API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000")
_INTERVAL_MINUTES = int(os.environ.get("CRAWLER_INTERVAL_MINUTES", "30"))


def _get_tracked_cards() -> list[dict]:
    """Fetch the current list of tracked cards from the API."""
    response = httpx.get(f"{_API_BASE}/cards/", timeout=10)
    response.raise_for_status()
    return list(response.json())


def _post_price(card_id: int, source: str, price: float) -> None:
    """POST a price snapshot to the API."""
    httpx.post(
        f"{_API_BASE}/prices/",
        json={"card_id": card_id, "source": source, "price": price},
        timeout=10,
    ).raise_for_status()


def run_price_crawl() -> None:
    """Fetch TCGPlayer prices for all tracked cards and persist them."""
    logger.info("Starting TCGPlayer price crawl")
    try:
        cards = _get_tracked_cards()
    except httpx.HTTPError as exc:
        logger.error("Could not fetch cards from API: %s", exc)
        return

    card_map = {c["name"]: c["id"] for c in cards}
    results = tcgplayer.crawl(list(card_map.keys()))

    saved = 0
    for result in results:
        if result.market_price is None:
            continue
        card_id = card_map.get(result.card_name)
        if card_id is None:
            continue
        try:
            _post_price(card_id, "tcgplayer", result.market_price)
            saved += 1
        except httpx.HTTPError as exc:
            logger.error("Failed to save price for %r: %s", result.card_name, exc)

    logger.info("TCGPlayer crawl complete — saved %d price(s)", saved)


def start() -> None:
    """Start the blocking APScheduler that runs crawlers on an interval."""
    logging.basicConfig(level=logging.INFO)
    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_price_crawl,
        trigger="interval",
        minutes=_INTERVAL_MINUTES,
        id="tcgplayer_prices",
        replace_existing=True,
    )
    logger.info(
        "Scheduler started — running price crawl every %d minute(s)",
        _INTERVAL_MINUTES,
    )
    # Run once immediately on startup, then on the interval
    run_price_crawl()
    scheduler.start()


if __name__ == "__main__":
    start()
