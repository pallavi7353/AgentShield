"""
Pydantic schemas for User CRUD.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role_id: int


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None
    status: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
