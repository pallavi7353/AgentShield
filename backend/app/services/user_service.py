"""
user_service.py
------------------
CRUD business logic for Users, kept separate from the router so
routers stay thin (validation/HTTP concerns only).
"""

from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.auth.hashing import hash_password
from app.schemas.user import UserCreate, UserUpdate


def get_users(db: Session) -> List[User]:
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


def create_user(db: Session, payload: UserCreate) -> User:
    existing = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered.")

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role_id=payload.role_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)

    if payload.email is not None:
        user.email = payload.email
    if payload.role_id is not None:
        user.role_id = payload.role_id
    if payload.status is not None:
        user.status = payload.status

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
