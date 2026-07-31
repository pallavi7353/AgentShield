"""
auth_service.py
------------------
Login business logic: password verification, brute-force lockout
policy (MAX_FAILED_LOGIN_ATTEMPTS), and audit logging of
login/logout/failed-login events.
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserStatus
from app.auth.hashing import verify_password
from app.config.settings import settings
from app.services.audit_service import write_audit_log
from app.services.alert_service import create_alert


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        # Do not reveal whether the username exists
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")

    # Check account lockout
    if user.locked_until and user.locked_until > datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account temporarily locked due to repeated failed login attempts.",
        )

    if not verify_password(password, user.hashed_password):
        user.failed_login_attempts += 1

        if user.failed_login_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
            user.locked_until = datetime.now(timezone.utc) + timedelta(
                minutes=settings.FAILED_LOGIN_LOCK_MINUTES
            )
            user.status = UserStatus.locked
            create_alert(
                db,
                title="Multiple Failed Login Attempts",
                severity="high",
                description=f"User '{username}' exceeded max failed login attempts and was locked.",
            )

        db.commit()
        write_audit_log(db, event_type="LOGIN_FAILED", user_id=user.id, action_taken="DENIED")

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")

    if user.status != UserStatus.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is not active.")

    # Successful login: reset failed-attempt counter
    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()

    write_audit_log(db, event_type="LOGIN_SUCCESS", user_id=user.id, action_taken="ALLOWED")

    return user
