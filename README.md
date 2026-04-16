# TCG Market Analytics Platform

## Overview

A full-stack platform for tracking and analyzing Pokémon and Riftbound trading card market data. The system automatically crawls pricing and stock data from key retailers and marketplaces, stores it in a PostgreSQL database, and surfaces insights through an analytics dashboard. A notification system alerts you when stock drops at major retailers so you can buy at MSRP.

## Core Features

- **Market Data Crawler** — automated scraping of card prices and availability from TCGPlayer, eBay, Amazon, and more
- **Sentiment Analytics** — scrape Reddit discussions, eBay sold listings, and TCGPlayer reviews to score hype and community sentiment per card and Pokémon
- **Stock Alerts** — real-time notifications when cards hit shelves at Target, Walmart, Costco, Amazon, and Pokémon Center
- **Analytics Dashboard** — price trends, population-relative value, and sentiment scores visualized in a web app
- **ETL Pipelines** — scheduled, orchestrated data collection runs stored in PostgreSQL

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | Python, FastAPI |
| **Database** | PostgreSQL |
| **ORM / Migrations** | SQLAlchemy, Alembic |
| **Data Validation** | Pydantic |
| **Web Crawling** | Scrapy + Playwright (for JS-heavy pages) |
| **Task Scheduling** | APScheduler or Celery + Redis |
| **Frontend** | React, Vite, Recharts (price charts) |
| **Notifications** | Twilio (SMS) or Discord webhook |
| **Containerization** | Docker, Docker Compose |
| **Package Management** | uv |
| **Testing** | pytest, anyio |

## Repo Structure

```
tcg-platform/
├── CLAUDE.md                    ← Claude's project bible
├── docs/
│   ├── architecture.md          ← System design decisions
│   ├── data-sources.md          ← URLs, rate limits, site notes
│   ├── tasks.md                 ← Active work checklist
│   └── schema.md                ← DB schema reference
│
├── crawler/                     ← Python scraping service
│   ├── spiders/
│   │   ├── tcgplayer.py
│   │   ├── ebay.py
│   │   ├── pokemon_center.py
│   │   ├── target.py
│   │   ├── walmart.py
│   │   ├── amazon.py
│   │   └── costco.py
│   └── scheduler.py
│
├── api/                         ← FastAPI backend
│   ├── routers/
│   │   ├── cards.py
│   │   ├── prices.py
│   │   └── alerts.py
│   ├── models/                  ← SQLAlchemy models
│   ├── schemas/                 ← Pydantic schemas
│   ├── database.py
│   └── main.py
│
├── frontend/                    ← React analytics UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── PriceChart.jsx
│   │   │   ├── CardSearch.jsx
│   │   │   └── StockAlerts.jsx
│   │   └── pages/
│   └── CLAUDE.md                ← Frontend-specific rules
│
├── migrations/                  ← Alembic DB migrations
├── notifications/               ← Alert service
│   └── notifier.py
├── tests/                       ← pytest test suite
│   ├── test_crawlers.py
│   ├── test_api.py
│   └── test_notifications.py
├── scripts/                     ← One-off utility scripts
│   ├── seed_db.py
│   └── backfill_prices.py
├── docker-compose.yml
└── .env.example
```

## Learning Goals

- Web scraping at scale with rate limiting and anti-bot handling
- Sentiment analysis from unstructured social and marketplace data (Reddit, eBay, TCGPlayer)
- Managing a personal PostgreSQL database
- Building and scheduling ETL pipelines
- Working with a remote server
- Building a full-stack analytics dashboard and web app (React frontend + FastAPI backend)
- MCP (Model Context Protocol) integrations for AI tooling
