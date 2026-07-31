"""
Pydantic schemas for ThreatHistory, including the request schema
for analyzing a new prompt through the threat-detection engine.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ThreatAnalyzeRequest(BaseModel):
    prompt: str
    agent_name: Optional[str] = None


class ThreatResponseAnalyzeRequest(BaseModel):
    response_text: str
    agent_name: Optional[str] = None


class ThreatHistoryOut(BaseModel):
    id: int
    prompt: str
    attack_type: Optional[str]
    risk_score: int
    blocked: bool
    timestamp: datetime

    class Config:
        from_attributes = True