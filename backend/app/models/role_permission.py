"""
RolePermission model
----------------------
Many-to-many junction table linking Roles <-> Permissions.
This is what implements the Least-Privilege model: a role only
has the exact permissions explicitly granted to it here.
"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.db import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)

    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")
