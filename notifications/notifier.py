"""Stock alert notifier — sends Discord webhook messages."""

import logging
import os

import httpx

logger = logging.getLogger(__name__)

_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")


def send_alert(message: str) -> None:
    """Send a stock alert notification via Discord webhook.

    Silently skips if DISCORD_WEBHOOK_URL is not configured.
    """
    if not _WEBHOOK_URL:
        logger.debug("DISCORD_WEBHOOK_URL not set — skipping notification")
        return

    payload = {"content": message}
    try:
        response = httpx.post(_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error("Failed to send Discord notification: %s", exc)


def send_stock_alert(
    card_name: str,
    retailer: str,
    url: str | None = None,
    price: float | None = None,
) -> None:
    """Format and send a stock-in alert for a specific card."""
    parts = [f"**{card_name}** is in stock at **{retailer}**!"]
    if price is not None:
        parts.append(f"Price: ${price:.2f}")
    if url:
        parts.append(url)
    send_alert("\n".join(parts))
