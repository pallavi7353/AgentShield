"""
AIAgent model
--------------
Registry of autonomous AI agents being monitored by the platform.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.db import Base


class AIAgent(Base):
    __tablename__ = "ai_agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), unique=True, nullable=False)
    status = Column(String(20), default="idle")  # idle | active | suspended
    last_active = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
