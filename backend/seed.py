"""
seed.py
--------
Standalone script to initialize the database schema and insert
seed data (roles, permissions, demo users). Run once after setup:

    python seed.py
"""

from app.database.db import Base, engine, SessionLocal
from app.utils.seed_data import seed
from app import models  # noqa: F401  (ensures all models are registered)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
