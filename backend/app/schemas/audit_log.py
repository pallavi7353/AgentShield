"""
Pydantic schemas for AuditLog.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AuditLogOut(BaseModel):
    id: int
    user_id: Optional[int]
    prompt: Optional[str]
    response: Optional[str]
    threat_level: str
    action_taken: Optional[str]
    event_type: str
    timestamp: datetime

    class Config:
        from_attributes = True
