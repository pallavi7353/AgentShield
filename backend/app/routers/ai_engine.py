"""
ai_engine.py (router)
------------------------
Member 1 (AI & Backend Lead) - AI Security Engine.

POST /analyze                - full pipeline: Gemma + rule engine,
                                logs to ThreatHistory + AuditLog,
                                raises an Alert and returns an
                                ALLOW/BLOCK decision.
POST /risk-score              - just the 0-100 risk score for a piece
                                of text (no persistence).
POST /detect-prompt           - prompt-injection-only classification.
POST /detect-sensitive-data   - sensitive-data/PII-only classification.

All four sit alongside Member 3's /threat-history endpoints and
reuse the same ThreatHistory / Alert / AuditLog tables so the
dashboard has one unified data source regardless of which endpoint
a client called.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.config.settings import settings
from app.auth.dependencies import require_permission, get_current_user
from app.models.user import User
from app.models.threat_history import ThreatHistory
from app.services.gemma_service import classify_with_gemma
from app.services.alert_service import create_alert
from app.services.audit_service import write_audit_log
from app.schemas.ai_engine import (
    AnalyzeRequest,
    AnalyzeResponse,
    RiskScoreRequest,
    RiskScoreResponse,
    DetectPromptRequest,
    DetectPromptResponse,
    DetectSensitiveDataRequest,
    DetectSensitiveDataResponse,
)

router = APIRouter(tags=["AI Security Engine"])


def _risk_level(score: int) -> str:
    if score >= 85:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 30:
        return "medium"
    return "low"


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    dependencies=[Depends(require_permission("EXECUTE_AI_AGENT"))],
)
async def analyze(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Full AI Security Engine pipeline: run the text through Gemma
    (with automatic rule-based fallback), decide Allow/Block, and
    persist the result to ThreatHistory/AuditLog/Alerts.
    """
    assessment = await classify_with_gemma(payload.text)
    blocked = assessment.risk_score >= settings.HIGH_RISK_SCORE_THRESHOLD
    decision = "BLOCK" if blocked else "ALLOW"

    record = ThreatHistory(
        prompt=payload.text,
        attack_type=assessment.attack_type,
        risk_score=assessment.risk_score,
        blocked=blocked,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    write_audit_log(
        db,
        event_type="AI_REQUEST" if payload.direction == "inbound" else "AI_RESPONSE",
        user_id=current_user.id,
        prompt=payload.text,
        threat_level=_risk_level(assessment.risk_score),
        action_taken=decision,
    )

    if blocked:
        create_alert(
            db,
            title=f"{assessment.attack_type.replace('_', ' ').title()} Detected (Gemma)",
            severity=_risk_level(assessment.risk_score),
            description=(
                f"Agent '{payload.agent_name or 'unknown'}' {payload.direction} text flagged as "
                f"{assessment.attack_type} (risk {assessment.risk_score}/100, source={assessment.source}). "
                f"{assessment.reasoning}"
            ),
        )

    return AnalyzeResponse(
        attack_type=assessment.attack_type,
        risk_score=assessment.risk_score,
        confidence=assessment.confidence,
        decision=decision,
        reasoning=assessment.reasoning,
        sensitive_data_found=assessment.sensitive_data_found,
        sensitive_data_types=assessment.sensitive_data_types,
        source=assessment.source,
        threat_history_id=record.id,
    )


@router.post(
    "/risk-score",
    response_model=RiskScoreResponse,
    dependencies=[Depends(require_permission("EXECUTE_AI_AGENT"))],
)
async def risk_score(payload: RiskScoreRequest):
    """Lightweight endpoint: just the risk score, no DB writes."""
    assessment = await classify_with_gemma(payload.text)
    return RiskScoreResponse(
        risk_score=assessment.risk_score,
        risk_level=_risk_level(assessment.risk_score),
        confidence=assessment.confidence,
        source=assessment.source,
    )


@router.post(
    "/detect-prompt",
    response_model=DetectPromptResponse,
    dependencies=[Depends(require_permission("EXECUTE_AI_AGENT"))],
)
async def detect_prompt(payload: DetectPromptRequest):
    """Prompt-injection-focused classification."""
    assessment = await classify_with_gemma(payload.text)
    return DetectPromptResponse(
        is_prompt_injection=assessment.attack_type == "PROMPT_INJECTION",
        attack_type=assessment.attack_type,
        risk_score=assessment.risk_score,
        reasoning=assessment.reasoning,
        source=assessment.source,
    )


@router.post(
    "/detect-sensitive-data",
    response_model=DetectSensitiveDataResponse,
    dependencies=[Depends(require_permission("EXECUTE_AI_AGENT"))],
)
async def detect_sensitive_data(payload: DetectSensitiveDataRequest):
    """Sensitive-data / PII-focused classification."""
    assessment = await classify_with_gemma(payload.text)
    return DetectSensitiveDataResponse(
        sensitive_data_found=assessment.sensitive_data_found or assessment.attack_type == "DATA_LEAKAGE",
        sensitive_data_types=assessment.sensitive_data_types,
        risk_score=assessment.risk_score,
        source=assessment.source,
    )
