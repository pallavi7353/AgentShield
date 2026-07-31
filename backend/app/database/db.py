"""
db.py
------
SQLAlchemy engine + session setup.
Works with SQLite out of the box; switch DATABASE_URL to a
PostgreSQL DSN (postgresql://user:pass@host/db) for production
with no other code changes.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

# connect_args is only needed for SQLite (disables same-thread check
# so FastAPI's threaded workers can share connections safely)
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency-injected DB session.
    Guarantees the session is closed after each request,
    even if an exception is raised mid-request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
