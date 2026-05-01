"""Tests for the FastAPI backend."""

from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# /cards
# ---------------------------------------------------------------------------


def test_list_cards_empty(client: TestClient) -> None:
    """GET /cards/ returns an empty list when no cards exist."""
    response = client.get("/cards/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_card(client: TestClient) -> None:
    """POST /cards/ creates a card and returns it with an id."""
    payload = {"name": "Charizard ex", "set_name": "Obsidian Flames", "game": "pokemon"}
    response = client.post("/cards/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Charizard ex"
    assert data["set_name"] == "Obsidian Flames"
    assert data["game"] == "pokemon"
    assert data["card_number"] is None


def test_create_card_with_number(client: TestClient) -> None:
    """POST /cards/ stores optional card_number."""
    payload = {
        "name": "Pikachu",
        "set_name": "Base Set",
        "card_number": "58/102",
        "game": "pokemon",
    }
    response = client.post("/cards/", json=payload)
    assert response.status_code == 201
    assert response.json()["card_number"] == "58/102"


def test_list_cards_after_create(client: TestClient) -> None:
    """GET /cards/ returns all created cards."""
    client.post("/cards/", json={"name": "A", "set_name": "S1", "game": "pokemon"})
    client.post("/cards/", json={"name": "B", "set_name": "S1", "game": "riftbound"})
    response = client.get("/cards/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_card(client: TestClient) -> None:
    """GET /cards/{id} returns the card."""
    created = client.post(
        "/cards/", json={"name": "Mewtwo", "set_name": "Base Set", "game": "pokemon"}
    ).json()
    response = client.get(f"/cards/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Mewtwo"


def test_get_card_not_found(client: TestClient) -> None:
    """GET /cards/{id} returns 404 for a missing card."""
    response = client.get("/cards/999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# /prices
# ---------------------------------------------------------------------------


def test_list_prices_empty(client: TestClient) -> None:
    """GET /prices/ returns an empty list when no snapshots exist."""
    response = client.get("/prices/")
    assert response.status_code == 200
    assert response.json() == []


def test_record_price(client: TestClient) -> None:
    """POST /prices/ records a price snapshot for an existing card."""
    card = client.post(
        "/cards/", json={"name": "Charizard", "set_name": "Base Set", "game": "pokemon"}
    ).json()
    payload = {"card_id": card["id"], "source": "tcgplayer", "price": 249.99}
    response = client.post("/prices/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["price"] == 249.99
    assert data["source"] == "tcgplayer"
    assert data["currency"] == "USD"


def test_record_price_card_not_found(client: TestClient) -> None:
    """POST /prices/ returns 404 when the card does not exist."""
    response = client.post(
        "/prices/", json={"card_id": 999, "source": "tcgplayer", "price": 10.0}
    )
    assert response.status_code == 404


def test_list_prices_filter_by_card(client: TestClient) -> None:
    """GET /prices/?card_id=N returns only snapshots for that card."""
    card_a = client.post(
        "/cards/", json={"name": "A", "set_name": "S", "game": "pokemon"}
    ).json()
    card_b = client.post(
        "/cards/", json={"name": "B", "set_name": "S", "game": "pokemon"}
    ).json()
    client.post(
        "/prices/", json={"card_id": card_a["id"], "source": "tcgplayer", "price": 10.0}
    )
    client.post(
        "/prices/", json={"card_id": card_b["id"], "source": "tcgplayer", "price": 20.0}
    )

    response = client.get(f"/prices/?card_id={card_a['id']}")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["card_id"] == card_a["id"]


# ---------------------------------------------------------------------------
# /alerts
# ---------------------------------------------------------------------------


def test_list_alerts_empty(client: TestClient) -> None:
    """GET /alerts/ returns an empty list when no alerts exist."""
    response = client.get("/alerts/")
    assert response.status_code == 200
    assert response.json() == []
