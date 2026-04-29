FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency manifests first for layer caching
COPY pyproject.toml uv.lock ./

# Install runtime dependencies only (no dev group)
RUN uv sync --frozen --no-dev

# Copy application source
COPY api/ api/
COPY migrations/ migrations/
COPY alembic.ini ./

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
