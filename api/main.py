"""FastAPI application entry point."""

from fastapi import FastAPI

from api.routers import alerts, cards, prices

app = FastAPI(title="TCG Market Analytics API")

app.include_router(cards.router)
app.include_router(prices.router)
app.include_router(alerts.router)
