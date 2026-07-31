"""
alert_service.py
------------------
Creates Alert records for the security team when something
noteworthy happens: high-risk prompt, prompt injection, data
leakage, unauthorized access, repeated failed logins.
"""

from sqlalchemy.orm import Session

from app.models.alert import Alert


def create_alert(db: Session, title: str, severity: str, description: str = "") -> Alert:
    alert = Alert(title=title, severity=severity, description=description, status="open")
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
