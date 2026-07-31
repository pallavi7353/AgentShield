"""
Alert model
------------
Security-team-facing alerts generated when risky behaviour is
detected: high-risk prompts, prompt injection, sensitive data
leakage, unauthorized access, repeated failed logins.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database.db import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    severity = Column(String(20), nullable=False)  # low | medium | high | critical
    description = Column(Text, nullable=True)
    status = Column(String(20), default="open")  # open | acknowledged | resolved
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
