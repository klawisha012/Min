"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import config as conf

DATABASE_URL = conf.DATABASE_URL

# Create sync engine
engine = create_engine(
    DATABASE_URL
)
# Create sync session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    """Base class for all database models"""
    pass


def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
