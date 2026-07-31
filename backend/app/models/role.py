"""
Role model
----------
Defines the roles available in the system:
Admin, Security Analyst, Employee, AI Agent.
Each role is linked to a set of Permissions via RolePermission.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False, index=True)

    # One role -> many users
    users = relationship("User", back_populates="role")

    # One role -> many RolePermission link rows -> many permissions
    role_permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
