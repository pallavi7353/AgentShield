"""
audit.py (router)
--------------------
GET /auditlogs

Requires READ_LOGS permission (Admin, Security Analyst by default).
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.audit_log import AuditLogOut
from app.models.audit_log import AuditLog
from app.auth.dependencies import require_permission

router = APIRouter(
    prefix="/auditlogs",
    tags=["Audit Logs"],
    dependencies=[Depends(require_permission("READ_LOGS"))],
)


@router.get("", response_model=List[AuditLogOut])
def list_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
