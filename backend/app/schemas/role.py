"""
Pydantic schemas for Role management.
"""

from pydantic import BaseModel
from typing import List, Optional


class RoleCreate(BaseModel):
    role_name: str
    permission_ids: Optional[List[int]] = []


class RoleOut(BaseModel):
    id: int
    role_name: str

    class Config:
        from_attributes = True
