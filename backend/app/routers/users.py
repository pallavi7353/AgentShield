"""
users.py (router)
--------------------
GET    /users
POST   /users
PUT    /users/{id}
DELETE /users/{id}

All endpoints require the MANAGE_USERS permission (Admin role only,
by default seed data).
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services import user_service
from app.auth.dependencies import require_permission

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(require_permission("MANAGE_USERS"))],
)


@router.get("", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)


@router.post("", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, payload)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, payload)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
    return None
