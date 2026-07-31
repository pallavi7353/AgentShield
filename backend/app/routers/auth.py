"""
auth.py (router)
------------------
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest, AccessTokenResponse
from app.schemas.user import UserCreate, UserOut
from app.services import user_service, auth_service
from app.services.audit_service import write_audit_log
from app.auth.jwt_handler import create_access_token, create_refresh_token, decode_token
from app.auth.dependencies import get_current_user
from app.models.user import User
from fastapi import HTTPException, status

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, payload)
    write_audit_log(db, event_type="USER_REGISTERED", user_id=user.id, action_taken="ALLOWED")
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.username, payload.password)

    access_token = create_access_token(subject=user.username, extra_claims={"role": user.role.role_name})
    refresh_token = create_refresh_token(subject=user.username)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    decoded = decode_token(payload.refresh_token)
    if not decoded or decoded.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token.")

    username = decoded.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists.")

    new_access_token = create_access_token(subject=user.username, extra_claims={"role": user.role.role_name})
    return AccessTokenResponse(access_token=new_access_token)


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Stateless JWT: real invalidation requires a token blocklist (see README notes).
    write_audit_log(db, event_type="LOGOUT", user_id=current_user.id, action_taken="ALLOWED")
    return {"detail": "Logged out successfully."}
