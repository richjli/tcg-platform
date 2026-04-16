"""Database connection and session management."""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and close it when done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
