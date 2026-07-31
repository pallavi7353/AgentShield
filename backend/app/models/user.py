"""
User model
-----------
Stores human users and service accounts. Passwords are NEVER stored
in plaintext -- only a bcrypt hash. Includes fields to support
session/login-attempt security policies (failed_login_attempts,
locked_until).
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database.db import Base


class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    locked = "locked"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.active, nullable=False)

    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    role = relationship("Role", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")
