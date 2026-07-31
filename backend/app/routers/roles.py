"""
roles.py (router)
--------------------
GET  /roles
POST /roles
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.role import RoleCreate, RoleOut
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.auth.dependencies import require_permission

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    dependencies=[Depends(require_permission("MANAGE_USERS"))],
)


@router.get("", response_model=List[RoleOut])
def list_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


@router.post("", response_model=RoleOut, status_code=201)
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    role = Role(role_name=payload.role_name)
    db.add(role)
    db.commit()
    db.refresh(role)

    for permission_id in payload.permission_ids or []:
        db.add(RolePermission(role_id=role.id, permission_id=permission_id))
    db.commit()

    return role
