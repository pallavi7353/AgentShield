"""
AuditLog model
---------------
Immutable trail of every AI-agent interaction and security-relevant
event: logins, logouts, AI requests, blocked requests, prompt
injection attempts, data leakage attempts, admin actions.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # nullable: system/agent events

    prompt = Column(Text, nullable=True)
    response = Column(Text, nullable=True)
    threat_level = Column(String(20), default="none")  # none | low | medium | high | critical
    action_taken = Column(String(100), nullable=True)  # e.g. ALLOWED, BLOCKED, FLAGGED

    event_type = Column(String(50), default="AI_REQUEST")  # LOGIN, LOGOUT, AI_REQUEST, ADMIN_ACTION, ...

    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="audit_logs")
