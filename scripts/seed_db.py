"""Seed the database with initial card data."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.models.card import Card

SEED_CARDS: list[dict[str, str | None]] = [
    # Pokémon — Obsidian Flames
    {
        "name": "Charizard ex",
        "set_name": "Obsidian Flames",
        "card_number": "125/197",
        "game": "pokemon",
    },
    {
        "name": "Tyranitar ex",
        "set_name": "Obsidian Flames",
        "card_number": "121/197",
        "game": "pokemon",
    },
    {
        "name": "Pidgeot ex",
        "set_name": "Obsidian Flames",
        "card_number": "164/197",
        "game": "pokemon",
    },
    # Pokémon — Scarlet & Violet Base
    {
        "name": "Miraidon ex",
        "set_name": "Scarlet & Violet",
        "card_number": "81/198",
        "game": "pokemon",
    },
    {
        "name": "Koraidon ex",
        "set_name": "Scarlet & Violet",
        "card_number": "254/198",
        "game": "pokemon",
    },
    # Pokémon — Paldea Evolved
    {
        "name": "Iono",
        "set_name": "Paldea Evolved",
        "card_number": "185/193",
        "game": "pokemon",
    },
    {
        "name": "Tinkaton ex",
        "set_name": "Paldea Evolved",
        "card_number": "165/193",
        "game": "pokemon",
    },
    # Riftbound
    {
        "name": "Lux",
        "set_name": "Riftbound Core Set",
        "card_number": None,
        "game": "riftbound",
    },
    {
        "name": "Zed",
        "set_name": "Riftbound Core Set",
        "card_number": None,
        "game": "riftbound",
    },
]


def main() -> None:
    """Seed the database with initial card data."""
    database_url = os.environ["DATABASE_URL"]
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        existing = {
            (c.name, c.set_name) for c in session.query(Card.name, Card.set_name).all()
        }
        to_insert = [
            Card(**card)
            for card in SEED_CARDS
            if (card["name"], card["set_name"]) not in existing
        ]
        if not to_insert:
            print("Nothing to seed — all cards already present.")
            return
        session.add_all(to_insert)
        session.commit()
        print(f"Seeded {len(to_insert)} card(s).")


if __name__ == "__main__":
    main()
