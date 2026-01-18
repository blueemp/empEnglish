"""Database configuration and session management."""

import os
from typing import Generator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Get database URL from environment or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://user:password@localhost/empenglish"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=os.getenv("DEBUG", "false").lower() == "true",
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)
