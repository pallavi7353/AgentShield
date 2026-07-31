"""
dependencies.py
-----------------
FastAPI dependency-injection helpers for:
- Extracting & validating the current user from a JWT access token
- Enforcing Role-Based Access Control (RBAC) / least privilege
  on individual routes via `require_permission("PERMISSION_NAME")`

Usage in a router:

    @router.get("/auditlogs", dependencies=[Depends(require_permission("READ_LOGS"))])
    def list_logs(...): ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.auth.jwt_handler import decode_token
from app.models.user import User, UserStatus

oauth2_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(credentials.credentials)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    if user.status != UserStatus.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active (inactive or locked).",
        )

    return user


def require_permission(permission_name: str):
    """
    Returns a FastAPI dependency that enforces the current user's role
    has the given permission. This is the core of the least-privilege
    enforcement layer.
    """

    def checker(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
        role = current_user.role
        granted_permission_names = {rp.permission.permission_name for rp in role.role_permissions}

        if permission_name not in granted_permission_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role.role_name}' lacks required permission '{permission_name}'.",
            )
        return current_user

    return checker


def require_role(*allowed_roles: str):
    """
    Alternative to permission-based checks: restrict a route to
    specific role names directly (e.g. Admin-only endpoints).
    """

    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {allowed_roles}",
            )
        return current_user

    return checker
