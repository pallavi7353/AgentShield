"""
audit_service.py
------------------
Central place to write AuditLog entries so every part of the app
logs events consistently (same event_type vocabulary, same shape).
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def write_audit_log(
    db: Session,
    event_type: str,
    user_id: Optional[int] = None,
    prompt: Optional[str] = None,
    response: Optional[str] = None,
    threat_level: str = "none",
    action_taken: Optional[str] = None,
) -> AuditLog:
    log = AuditLog(
        user_id=user_id,
        prompt=prompt,
        response=response,
        threat_level=threat_level,
        action_taken=action_taken,
        event_type=event_type,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
