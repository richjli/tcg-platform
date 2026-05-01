"""Tests for the notification service."""

from unittest.mock import MagicMock, patch

import httpx

from notifications.notifier import send_alert, send_stock_alert


def test_send_alert_skips_when_no_webhook(monkeypatch: MagicMock) -> None:
    """send_alert is a no-op when DISCORD_WEBHOOK_URL is not set."""
    monkeypatch.setattr("notifications.notifier._WEBHOOK_URL", "")
    with patch("notifications.notifier.httpx.post") as mock_post:
        send_alert("test message")
        mock_post.assert_not_called()


def test_send_alert_posts_to_webhook(monkeypatch: MagicMock) -> None:
    """send_alert POSTs the message to the configured webhook URL."""
    monkeypatch.setattr(
        "notifications.notifier._WEBHOOK_URL", "https://discord.com/api/webhooks/test"
    )
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    with patch(
        "notifications.notifier.httpx.post", return_value=mock_response
    ) as mock_post:
        send_alert("hello world")
        mock_post.assert_called_once_with(
            "https://discord.com/api/webhooks/test",
            json={"content": "hello world"},
            timeout=10,
        )


def test_send_alert_logs_on_http_error(monkeypatch: MagicMock) -> None:
    """send_alert logs an error and does not raise on HTTP failure."""
    monkeypatch.setattr(
        "notifications.notifier._WEBHOOK_URL", "https://discord.com/api/webhooks/test"
    )
    with patch(
        "notifications.notifier.httpx.post",
        side_effect=httpx.RequestError("timeout"),
    ):
        send_alert("should not raise")  # must not propagate


def test_send_stock_alert_formats_message(monkeypatch: MagicMock) -> None:
    """send_stock_alert builds a message with card name, retailer, price, URL."""
    monkeypatch.setattr(
        "notifications.notifier._WEBHOOK_URL", "https://discord.com/api/webhooks/test"
    )
    captured: list[str] = []

    def _fake_post(url: str, *, json: dict, timeout: int) -> MagicMock:
        captured.append(json["content"])
        m = MagicMock()
        m.raise_for_status = MagicMock()
        return m

    with patch("notifications.notifier.httpx.post", side_effect=_fake_post):
        send_stock_alert(
            card_name="Charizard ex",
            retailer="Target",
            url="https://target.com/p/1234",
            price=34.99,
        )

    assert len(captured) == 1
    msg = captured[0]
    assert "Charizard ex" in msg
    assert "Target" in msg
    assert "34.99" in msg
    assert "https://target.com/p/1234" in msg
