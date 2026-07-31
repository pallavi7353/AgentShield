"""
threats.py (router)
----------------------
GET  /threat-history                 - list past threat assessments
POST /threat-history/analyze         - run a prompt through the
                                        detection engine (this is the
                                        integration point for
                                        Member 2's AI/agent module)
POST /threat-history/analyze-response - run an AI agent's outgoing
                                        response through the detection
                                        engine, to catch sensitive data
                                        before it reaches the user

analyze also auto-creates an Alert + AuditLog entry when the prompt
is flagged high-risk, tying the three security tables together.
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.threat_history import ThreatAnalyzeRequest, ThreatHistoryOut, ThreatResponseAnalyzeRequest
from app.models.threat_history import ThreatHistory
from app.services.threat_detection_service import analyze_prompt, analyze_response
from app.services.alert_service import create_alert
from app.services.audit_service import write_audit_log
from app.auth.dependencies import require_permission, get_current_user
from app.config.settings import settings
from app.models.user import User

router = APIRouter(prefix="/threat-history", tags=["Threat Detection"])


@router.get("", response_model=List[ThreatHistoryOut], dependencies=[Depends(require_permission("READ_LOGS"))])
def list_threat_history(db: Session = Depends(get_db)):
    return db.query(ThreatHistory).order_by(ThreatHistory.timestamp.desc()).all()


@router.post(
    "/analyze",
    response_model=ThreatHistoryOut,
    dependencies=[Depends(require_permission("EXECUTE_AI_AGENT"))],
)
def analyze(
    payload: ThreatAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = analyze_prompt(payload.prompt, high_risk_threshold=settings.HIGH_RISK_SCORE_THRESHOLD)

    record = ThreatHistory(
        prompt=payload.prompt,
        attack_type=assessment.attack_type,
        risk_score=assessment.risk_score,
        blocked=assessment.blocked,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    write_audit_log(
        db,
        event_type="AI_REQUEST",
        user_id=current_user.id,
        prompt=payload.prompt,
        threat_level=("high" if assessment.blocked else "none"),
        action_taken=("BLOCKED" if assessment.blocked else "ALLOWED"),
    )

    if assessment.blocked:
        create_alert(
            db,
            title=f"{assessment.attack_type.replace('_', ' ').title()} Detected",
            severity="high",
            description=(
                f"Agent '{payload.agent_name or 'unknown'}' submitted a prompt matching "
                f"pattern for {assessment.attack_type} (risk score {assessment.risk_score})."
            ),
        )

    return record


@router.post(
    "/analyze-response",
    response_model=ThreatHistoryOut,
    dependencies=[Depends(require_permission("EXECUTE_AI_AGENT"))],
)
def analyze_response_endpoint(
    payload: ThreatResponseAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = analyze_response(payload.response_text, high_risk_threshold=settings.HIGH_RISK_SCORE_THRESHOLD)

    record = ThreatHistory(
        prompt=payload.response_text,
        attack_type=assessment.attack_type,
        risk_score=assessment.risk_score,
        blocked=assessment.blocked,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    write_audit_log(
        db,
        event_type="AI_RESPONSE",
        user_id=current_user.id,
        prompt=payload.response_text,
        threat_level=("high" if assessment.blocked else "none"),
        action_taken=("BLOCKED" if assessment.blocked else "ALLOWED"),
    )

    if assessment.blocked:
        create_alert(
            db,
            title=f"{assessment.attack_type.replace('_', ' ').title()} Detected in Response",
            severity="high",
            description=(
                f"Agent '{payload.agent_name or 'unknown'}' response contained a pattern "
                f"matching {assessment.attack_type} (risk score {assessment.risk_score})."
            ),
        )

    return record