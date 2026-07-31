"""
Pydantic schemas for Alert.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlertOut(BaseModel):
    id: int
    title: str
    severity: str
    description: Optional[str]
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True


class AlertUpdate(BaseModel):
    status: str  # open | acknowledged | resolved
