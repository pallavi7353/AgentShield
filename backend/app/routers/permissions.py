"""
permissions.py (router)
--------------------------
GET /permissions
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.permission import PermissionOut
from app.models.permission import Permission
from app.auth.dependencies import require_permission

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
    dependencies=[Depends(require_permission("MANAGE_USERS"))],
)


@router.get("", response_model=List[PermissionOut])
def list_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()
