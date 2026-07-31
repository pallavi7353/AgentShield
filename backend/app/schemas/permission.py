"""
Pydantic schemas for Permission.
"""

from pydantic import BaseModel


class PermissionOut(BaseModel):
    id: int
    permission_name: str

    class Config:
        from_attributes = True
