"""
jwt_handler.py
---------------
Creation and validation of JWT access & refresh tokens.

Access tokens: short-lived, sent on every request.
Refresh tokens: long-lived, used only to mint a new access token.
Both are signed with the same secret but carry a "type" claim so
one cannot be used in place of the other.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from app.config.settings import settings


def _create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(subject: str, extra_claims: Optional[dict] = None) -> str:
    data = {"sub": subject}
    if extra_claims:
        data.update(extra_claims)
    return _create_token(
        data,
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(subject: str) -> str:
    data = {"sub": subject}
    return _create_token(
        data,
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
    )


def decode_token(token: str) -> Optional[dict]:
    """
    Returns the decoded payload if the token is valid and not expired,
    otherwise returns None. Callers are responsible for checking the
    'type' claim matches what they expect (access vs refresh).
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
