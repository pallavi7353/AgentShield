"""
ThreatHistory model
---------------------
Record of every prompt run through the threat-detection engine,
its classified attack type, computed risk score, and whether it
was blocked. Powers the dashboard's threat analytics.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func

from app.database.db import Base


class ThreatHistory(Base):
    __tablename__ = "threat_history"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    attack_type = Column(String(50), nullable=True)  # PROMPT_INJECTION | DATA_LEAKAGE | NONE | ...
    risk_score = Column(Integer, default=0)  # 0-100
    blocked = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
