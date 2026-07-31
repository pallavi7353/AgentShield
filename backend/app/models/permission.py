"""
Permission model
-----------------
Fine-grained capabilities that can be granted to a role, e.g.
READ_LOGS, VIEW_DASHBOARD, MANAGE_USERS, EXECUTE_AI_AGENT, EXPORT_REPORTS.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String(100), unique=True, nullable=False, index=True)

    role_permissions = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")
