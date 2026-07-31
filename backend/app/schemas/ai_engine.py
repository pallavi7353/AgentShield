"""
Pydantic schemas for Member 1's AI Security Engine
(/analyze, /risk-score, /detect-prompt, /detect-sensitive-data).
"""

from typing import List, Optional
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    text: str
    agent_name: Optional[str] = None
    direction: Optional[str] = "inbound"  # "inbound" (prompt) | "outbound" (agent response)


class AnalyzeResponse(BaseModel):
    attack_type: str
    risk_score: int
    confidence: float
    decision: str          # "ALLOW" | "BLOCK"
    reasoning: str
    sensitive_data_found: bool
    sensitive_data_types: List[str] = []
    source: str             # "gemma" | "fallback_rule_engine"
    threat_history_id: Optional[int] = None


class RiskScoreRequest(BaseModel):
    text: str


class RiskScoreResponse(BaseModel):
    risk_score: int
    risk_level: str          # "low" | "medium" | "high" | "critical"
    confidence: float
    source: str


class DetectPromptRequest(BaseModel):
    text: str


class DetectPromptResponse(BaseModel):
    is_prompt_injection: bool
    attack_type: str
    risk_score: int
    reasoning: str
    source: str


class DetectSensitiveDataRequest(BaseModel):
    text: str


class DetectSensitiveDataResponse(BaseModel):
    sensitive_data_found: bool
    sensitive_data_types: List[str] = []
    risk_score: int
    source: str
